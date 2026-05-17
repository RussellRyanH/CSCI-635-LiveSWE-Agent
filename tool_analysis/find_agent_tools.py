#!/usr/bin/env python3
# File created with assistance from ChatGPT
"""
find_agent_tools.py

Extract Python scripts/tools created by an agent in a mini-SWE-agent / Live-SWE-agent
trajectory JSON file.

This script treats each *definition* of a created file as a separate record.

That means:
  - If the agent writes `tool.py` at step 5, that is `tool.py#v1`.
  - If it later overwrites `tool.py` at step 9, that is `tool.py#v2`.
  - `tool.py#v2` is marked as superseding `tool.py#v1`.
  - `tool.py#v1` is marked as killed/overwritten by `tool.py#v2`.

The script detects created-file definitions from:
  1. assistant bash code blocks such as:
       cat <<'EOF' > tool.py
       ...
       EOF
     or:
       cat > tool.py <<'EOF'
       ...
       EOF
     or:
       tee tool.py >/dev/null <<'EOF'
       ...
       EOF

  2. final git diff / submission text containing "new file mode" entries.
     Diff-derived entries are used as a fallback for files that were not directly
     reconstructed from assistant commands. They do not create additional versions
     when command-derived definitions already exist.

By default, it reports Python files only, since Live-SWE-agent's tool-creation
instructions ask agents to create Python tools. Use --all-created to include
non-Python files too.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Optional


DEFAULT_ACTION_REGEX = r"```bash\s*\n(.*?)\n```"


@dataclass
class ToolDefinition:
    path: str
    version: int
    definition_id: str
    source: str                    # "command" or "submission_diff"
    step: Optional[int] = None     # assistant action step number, if known
    method: Optional[str] = None
    write_mode: Optional[str] = None   # "overwrite", "append", or "unknown"
    content: Optional[str] = None
    command: Optional[str] = None
    used_steps: Optional[list[int]] = None
    same_step_use_steps: Optional[list[int]] = None
    definition_end_offset: Optional[int] = None

    # Version lineage
    supersedes: Optional[str] = None
    killed_by: Optional[str] = None
    lifecycle_status: str = "active"   # "active", "overwritten", "appended_to"

    @property
    def suffix(self) -> str:
        return Path(self.path).suffix.lower()

    @property
    def looks_like_repro_or_test(self) -> bool:
        name = Path(self.path).name.lower()
        return (
            name.startswith("test_")
            or name.startswith("repro")
            or name in {"reproduce.py", "reproduction.py"}
        )


def load_json(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise SystemExit(f"Could not parse JSON in {path}: {e}") from e


def get_action_regex(traj: dict) -> re.Pattern[str]:
    pattern = (
        traj.get("info", {})
            .get("config", {})
            .get("agent", {})
            .get("action_regex")
        or DEFAULT_ACTION_REGEX
    )
    return re.compile(pattern, re.DOTALL)


def iter_assistant_commands(traj: dict) -> Iterable[tuple[int, str, str]]:
    """
    Yield (step_number, command, full_assistant_message_content).

    Step numbers count assistant messages that contain a bash action.
    """
    action_re = get_action_regex(traj)
    step = 0

    for msg in traj.get("messages", []):
        if msg.get("role") != "assistant":
            continue

        content = msg.get("content") or ""
        matches = action_re.findall(content)
        if not matches:
            continue

        # mini-SWE-agent should have exactly one action, but we tolerate multiple.
        for match in matches:
            step += 1
            command = match.strip() if isinstance(match, str) else match[0].strip()
            yield step, command, content


def _normalize_redirect_path(path: str) -> str:
    # Strip common shell quoting and trailing punctuation introduced by simple matching.
    return path.strip().strip("'\"").rstrip(";")


def _redir_to_mode(redir: str) -> str:
    return "append" if redir == ">>" else "overwrite"


def extract_heredoc_writes(command: str, step: int) -> list[ToolDefinition]:
    """
    Extract files created or rewritten with common heredoc patterns:
      cat <<'EOF' > file.py
      cat > file.py <<'EOF'
      tee file.py >/dev/null <<'EOF'
      tee -a file.py >/dev/null <<'EOF'
    """
    found: list[ToolDefinition] = []

    patterns = [
        # cat <<'EOF' > file.py / >>
        re.compile(
            r"""(?mxs)
            (?P<method>cat)\s+
            <<\s*['\"]?(?P<tag>[A-Za-z_][A-Za-z0-9_]*)['\"]?\s*
            (?P<redir>>>|>)\s*(?P<path>[^\s;&|]+)
            \s*\n
            (?P<body>.*?)
            ^(?P=tag)\s*$
            """
        ),
        # cat > file.py <<'EOF' / >>
        re.compile(
            r"""(?mxs)
            (?P<method>cat)\s+
            (?P<redir>>>|>)\s*(?P<path>[^\s;&|]+)\s*
            <<\s*['\"]?(?P<tag>[A-Za-z_][A-Za-z0-9_]*)['\"]?
            \s*\n
            (?P<body>.*?)
            ^(?P=tag)\s*$
            """
        ),
        # tee file.py >/dev/null <<'EOF'
        # tee overwrites by default; tee -a appends.
        re.compile(
            r"""(?mxs)
            (?P<method>tee)
            (?P<append>\s+-a)?
            \s+(?P<path>[^\s;&|]+)
            (?:\s+>\s*/dev/null)?
            \s*<<\s*['\"]?(?P<tag>[A-Za-z_][A-Za-z0-9_]*)['\"]?
            \s*\n
            (?P<body>.*?)
            ^(?P=tag)\s*$
            """
        ),
    ]

    for pattern in patterns:
        for m in pattern.finditer(command):
            method = m.group("method")
            if method == "tee":
                write_mode = "append" if m.groupdict().get("append") else "overwrite"
            else:
                write_mode = _redir_to_mode(m.group("redir"))

            found.append(
                ToolDefinition(
                    path=_normalize_redirect_path(m.group("path")),
                    version=0,  # assigned later
                    definition_id="",
                    source="command",
                    step=step,
                    method=method,
                    write_mode=write_mode,
                    content=m.group("body"),
                    command=command,
                    definition_end_offset=m.end(),
                )
            )

    return found


def extract_simple_redirect_writes(command: str, step: int) -> list[ToolDefinition]:
    """
    Catch simpler writes such as:
      echo '...' > file.py
      printf '...' > file.py
      echo '...' >> file.py

    Content extraction here is intentionally conservative.
    """
    found: list[ToolDefinition] = []
    pattern = re.compile(
        r"""(?mx)
        \b(?P<method>echo|printf)\b
        .*?
        (?P<redir>>>|>)\s*(?P<path>[^\s;&|]+)
        """
    )

    for m in pattern.finditer(command):
        found.append(
            ToolDefinition(
                path=_normalize_redirect_path(m.group("path")),
                version=0,
                definition_id="",
                source="command",
                step=step,
                method=m.group("method"),
                write_mode=_redir_to_mode(m.group("redir")),
                content=None,
                command=command,
                definition_end_offset=m.end(),
            )
        )

    return found


def parse_new_files_from_diff(diff_text: str) -> list[ToolDefinition]:
    """
    Parse final git diff text and extract new files and their added content.

    These entries are fallback-only. They represent the final file state, not
    a reconstructable chronological command-time definition.
    """
    if not diff_text:
        return []

    files: list[ToolDefinition] = []
    sections = re.split(r"(?=^diff --git a/.*? b/)", diff_text, flags=re.MULTILINE)

    for section in sections:
        if not section.startswith("diff --git"):
            continue
        if "new file mode" not in section:
            continue

        header = section.splitlines()[0]
        m = re.match(r"diff --git a/(.*?) b/(.*)", header)
        if not m:
            continue

        path = m.group(2)
        added_lines: list[str] = []
        in_hunk = False

        for line in section.splitlines():
            if line.startswith("@@"):
                in_hunk = True
                continue
            if not in_hunk:
                continue
            if line.startswith("+++") or line.startswith("---"):
                continue
            if line.startswith("+"):
                added_lines.append(line[1:])

        files.append(
            ToolDefinition(
                path=path,
                version=0,
                definition_id="",
                source="submission_diff",
                method="git_diff_new_file",
                write_mode="unknown",
                content="\n".join(added_lines) if added_lines else None,
            )
        )

    return files


def assign_versions_and_lineage(
    command_defs: list[ToolDefinition],
    diff_defs: list[ToolDefinition],
) -> list[ToolDefinition]:
    """
    Assign path-local versions and build overwrite lineage.

    Rules:
      - Every command-derived write becomes its own definition version.
      - Overwrite writes "kill" the previously active definition for that path.
      - Append writes create a new version but mark the prior version as appended_to,
        not killed, because append modifies/extends rather than replaces.
      - Diff-derived entries are included only for paths with no command-derived
        definition at all.
    """
    output: list[ToolDefinition] = []
    latest_by_path: dict[str, ToolDefinition] = {}
    version_counter: dict[str, int] = {}

    for definition in sorted(command_defs, key=lambda d: (d.step or 10**9, d.path)):
        version_counter[definition.path] = version_counter.get(definition.path, 0) + 1
        definition.version = version_counter[definition.path]
        definition.definition_id = f"{definition.path}#v{definition.version}"

        previous = latest_by_path.get(definition.path)
        if previous is not None:
            definition.supersedes = previous.definition_id
            if definition.write_mode == "append":
                previous.lifecycle_status = "appended_to"
                previous.killed_by = definition.definition_id
            else:
                previous.lifecycle_status = "overwritten"
                previous.killed_by = definition.definition_id

        latest_by_path[definition.path] = definition
        output.append(definition)

    command_paths = {d.path for d in command_defs}
    for definition in sorted(diff_defs, key=lambda d: d.path):
        if definition.path in command_paths:
            continue
        version_counter[definition.path] = version_counter.get(definition.path, 0) + 1
        definition.version = version_counter[definition.path]
        definition.definition_id = f"{definition.path}#v{definition.version}"
        output.append(definition)

    return output


def find_usage_steps(definitions: list[ToolDefinition], commands: list[tuple[int, str, str]]) -> None:
    """
    Identify command steps that reference each defined path.

    Uses are assigned to the definition active at that time:
      - Same-step uses are counted only when they occur *after* the write that
        defines the tool, e.g. `cat <<'EOF' > tool.py ... EOF && python tool.py`.
      - Later-step uses are counted after the definition step and before the next
        redefinition of the same path.
    """
    defs_by_path: dict[str, list[ToolDefinition]] = {}
    command_by_step = {step: command for step, command, _ in commands}

    for definition in definitions:
        defs_by_path.setdefault(definition.path, []).append(definition)

    for path, defs in defs_by_path.items():
        defs.sort(key=lambda d: d.step or 10**9)
        escaped_path = re.escape(path)
        escaped_base = re.escape(Path(path).name)
        path_re = re.compile(
            rf"(^|[\s'\"])(?:\./)?(?:{escaped_path}|{escaped_base})(?=$|[\s'\";&|])"
        )

        for i, definition in enumerate(defs):
            start_step = definition.step or -1
            next_step = defs[i + 1].step if i + 1 < len(defs) else None
            used: list[int] = []
            same_step_used: list[int] = []

            # Detect use later in the same bash action, but only after the
            # file-writing construct itself has ended.
            if definition.step is not None and definition.definition_end_offset is not None:
                same_command = command_by_step.get(definition.step, "")
                suffix_after_definition = same_command[definition.definition_end_offset:]
                if path_re.search(suffix_after_definition):
                    same_step_used.append(definition.step)

            for step, command, _ in commands:
                if step == definition.step:
                    continue
                if step <= start_step:
                    continue
                if next_step is not None and step >= next_step:
                    continue
                if path_re.search(command):
                    used.append(step)

            definition.same_step_use_steps = same_step_used
            definition.used_steps = used


def extract_tool_definitions(traj: dict, include_diff: bool = True) -> list[ToolDefinition]:
    commands = list(iter_assistant_commands(traj))
    command_defs: list[ToolDefinition] = []

    for step, command, _ in commands:
        command_defs.extend(extract_heredoc_writes(command, step))
        command_defs.extend(extract_simple_redirect_writes(command, step))

    diff_defs = parse_new_files_from_diff(traj.get("info", {}).get("submission", "")) if include_diff else []
    definitions = assign_versions_and_lineage(command_defs, diff_defs)
    find_usage_steps(definitions, commands)
    return definitions


def filter_definitions(
    definitions: list[ToolDefinition],
    *,
    all_created: bool,
    exclude_repro_tests: bool,
) -> list[ToolDefinition]:
    out = definitions

    if not all_created:
        out = [d for d in out if d.suffix == ".py"]

    if exclude_repro_tests:
        out = [d for d in out if not d.looks_like_repro_or_test]

    return out


def indent_block(text: str, prefix: str) -> str:
    if not text:
        return prefix + "<empty>"
    return "\n".join(prefix + line for line in text.splitlines())


def print_text_report(definitions: list[ToolDefinition], include_contents: bool) -> None:
    if not definitions:
        print("No created files matched the requested filters.")
        return

    for i, d in enumerate(definitions, start=1):
        print(f"{i}. {d.definition_id}")
        print(f"   path: {d.path}")
        print(f"   source: {d.source}")
        if d.step is not None:
            print(f"   defined at assistant step: {d.step}")
        if d.method:
            print(f"   detected by: {d.method}")
        if d.write_mode:
            print(f"   write mode: {d.write_mode}")
        print(f"   lifecycle: {d.lifecycle_status}")

        if d.supersedes:
            if d.write_mode == "append":
                print(f"   extends prior definition: {d.supersedes}")
            else:
                print(f"   kills prior definition: {d.supersedes}")

        if d.killed_by:
            if d.lifecycle_status == "appended_to":
                print(f"   later extended by: {d.killed_by}")
            else:
                print(f"   killed by: {d.killed_by}")

        if d.same_step_use_steps:
            print(f"   used in same creation step after definition: {', '.join(map(str, d.same_step_use_steps))}")
        else:
            print("   used in same creation step after definition: none detected")

        if d.used_steps:
            print(f"   used in later step(s) before next redefinition: {', '.join(map(str, d.used_steps))}")
        else:
            print("   used in later step(s) before next redefinition: none detected")

        if include_contents and d.content is not None:
            print("   content:")
            print(indent_block(d.content.rstrip(), prefix="      "))
        elif include_contents:
            print("   content: <not available from trajectory>")

        print()


def process_one(path: Path, args: argparse.Namespace) -> list[dict]:
    traj = load_json(path)
    definitions = extract_tool_definitions(traj, include_diff=not args.no_diff)
    definitions = filter_definitions(
        definitions,
        all_created=args.all_created,
        exclude_repro_tests=args.exclude_repro_tests,
    )

    records = []
    for d in definitions:
        record = asdict(d)
        record["trajectory"] = str(path)
        record["instance_id"] = traj.get("instance_id")
        if not args.contents:
            record.pop("content", None)
            record.pop("command", None)
        records.append(record)

    return records


def iter_input_paths(input_path: Path, recursive: bool) -> Iterable[Path]:
    if input_path.is_file():
        yield input_path
        return

    if not input_path.is_dir():
        raise SystemExit(f"Input path does not exist: {input_path}")

    pattern = "**/*.traj.json" if recursive else "*.traj.json"
    yield from sorted(input_path.glob(pattern))


def _trajectory_json_output_name(path: Path) -> str:
    """
    Convert a trajectory filename into a JSON report filename.

    Examples:
      django__django-11163.traj.json -> django__django-11163.tools.json
      trajectory.json                -> trajectory.tools.json
    """
    name = path.name
    if name.endswith(".traj.json"):
        return name[:-len(".traj.json")] + ".tools.json"
    if name.endswith(".json"):
        return name[:-len(".json")] + ".tools.json"
    return name + ".tools.json"


def aggregate_json_output_path(input_path: Path) -> Path:
    """
    Output path for non-recursive --json mode.

    - File input: write <trajectory>.tools.json in the current working directory.
    - Directory input: write <directory-name>.tools.json in the current working directory.
    """
    cwd = Path.cwd()
    if input_path.is_file():
        return cwd / _trajectory_json_output_name(input_path)

    directory_name = input_path.resolve().name or "trajectories"
    return cwd / f"{directory_name}.tools.json"


def per_trajectory_json_output_path(path: Path) -> Path:
    """
    Output path for recursive --json mode: place a JSON report beside the
    source trajectory.
    """
    return path.parent / _trajectory_json_output_name(path)


def write_json_report(path: Path, records: list[dict]) -> None:
    path.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Find tool/script definitions created by a Live-SWE-agent trajectory."
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Path to a .traj.json file, or a directory containing trajectories.",
    )
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="Recursively search a directory for *.traj.json files.",
    )
    parser.add_argument(
        "--all-created",
        action="store_true",
        help="Include all created files, not just .py files.",
    )
    parser.add_argument(
        "--exclude-repro-tests",
        action="store_true",
        help="Exclude files that look like reproduction or test scripts.",
    )
    parser.add_argument(
        "--contents",
        action="store_true",
        help="Include extracted file contents in the output.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help=(
            "Write JSON output to disk instead of printing a text report. "
            "Without --recursive, writes one aggregate JSON file in the current "
            "working directory. With --recursive, writes one JSON file beside "
            "each .traj.json file."
        ),
    )
    parser.add_argument(
        "--no-diff",
        action="store_true",
        help="Do not use final submission/git diff as a fallback source.",
    )
    args = parser.parse_args()

    input_paths = list(iter_input_paths(args.input, args.recursive))

    if args.json:
        if args.recursive:
            if not input_paths:
                print("No .traj.json files found.")
                return 0

            for path in input_paths:
                records = process_one(path, args)
                output_path = per_trajectory_json_output_path(path)
                write_json_report(output_path, records)
                print(f"Wrote {output_path} ({len(records)} record(s))")
            return 0

        all_records: list[dict] = []
        for path in input_paths:
            all_records.extend(process_one(path, args))

        output_path = aggregate_json_output_path(args.input)
        write_json_report(output_path, all_records)
        print(f"Wrote {output_path} ({len(all_records)} record(s))")
        return 0

    all_records: list[dict] = []
    for path in input_paths:
        all_records.extend(process_one(path, args))

    if not all_records:
        print("No created files matched the requested filters.")
        return 0

    # Group text output by trajectory for readability.
    by_traj: dict[str, list[ToolDefinition]] = {}
    for record in all_records:
        traj_path = record.pop("trajectory")
        fields = {k: v for k, v in record.items() if k in ToolDefinition.__dataclass_fields__}
        by_traj.setdefault(traj_path, []).append(ToolDefinition(**fields))

    for traj_path, definitions in by_traj.items():
        print(f"Trajectory: {traj_path}")
        print_text_report(definitions, include_contents=args.contents)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
