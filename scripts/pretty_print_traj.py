#!/usr/bin/env python3
# File created with the help of ChatGPT
"""
pretty_print_traj.py

Convert mini-swe-agent / Live-SWE-Agent trajectory JSON files into
human-readable Markdown files with collapsible sections for each LLM step.

Single-file usage:
    python pretty_print_traj.py path/to/example.traj.json -o readable.md

Recursive batch usage:
    python pretty_print_traj.py -r path/to/runs

In recursive mode, the input must be a directory. The script walks through that
directory and, for every .traj.json file it finds, creates a Markdown file in
the same directory named <instance_name>.md, where <instance_name> is the name
of the directory containing the trajectory file.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_message_content(message: Dict[str, Any]) -> str:
    content = message.get("content")
    if isinstance(content, str):
        return content

    try:
        nested = message["extra"]["response"]["choices"][0]["message"]["content"]
        if isinstance(nested, str):
            return nested
    except (KeyError, IndexError, TypeError):
        pass

    return ""


def normalize_text(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def fence_text(text: str, language: str = "text") -> str:
    """
    Safely wrap text in a Markdown code fence.

    If the text itself contains triple backticks, use a longer fence.
    """
    text = normalize_text(text)
    fence = "```"

    while fence in text:
        fence += "`"

    return f"{fence}{language}\n{text}\n{fence}"


def format_prompt_previous(messages: List[Dict[str, Any]], assistant_index: int) -> str:
    """
    Use the immediately preceding message as the prompt for this assistant step.
    """
    if assistant_index == 0:
        return ""

    previous = messages[assistant_index - 1]
    role = previous.get("role", "unknown")
    content = normalize_text(get_message_content(previous))

    return f"[{role}]\n{content}"


def format_prompt_full(messages: List[Dict[str, Any]], assistant_index: int) -> str:
    """
    Print the full conversation context visible before this assistant response.
    This is much longer, but closer to the full chat prompt sent to the model.
    """
    chunks: List[str] = []

    for i, message in enumerate(messages[:assistant_index], start=1):
        role = message.get("role", "unknown")
        content = normalize_text(get_message_content(message))
        chunks.append(f"Context message {i}: {role}\n\n{content}")

    return ("\n\n" + "-" * 80 + "\n\n").join(chunks)


def trajectory_to_markdown(
    trajectory: Dict[str, Any],
    title: str = "Trajectory",
    prompt_mode: str = "previous",
    include_system: bool = False,
) -> str:
    messages = trajectory.get("messages")

    if not isinstance(messages, list):
        raise ValueError("Trajectory JSON does not contain a top-level 'messages' list.")

    output: List[str] = []

    instance_id = trajectory.get("instance_id") or title
    output.append(f"# {instance_id}")
    output.append("")

    info = trajectory.get("info")
    if isinstance(info, dict):
        exit_status = info.get("exit_status")
        if exit_status is not None:
            output.append(f"**Exit status:** `{exit_status}`")
            output.append("")

        model_stats = info.get("model_stats")
        if isinstance(model_stats, dict):
            instance_cost = model_stats.get("instance_cost")
            api_calls = model_stats.get("api_calls")

            output.append("## Model stats")
            output.append("")
            if instance_cost is not None:
                output.append(f"- **Instance cost:** `{instance_cost}`")
            if api_calls is not None:
                output.append(f"- **API calls:** `{api_calls}`")
            output.append("")
        
        prompt_evolution_stats = info.get("prompt_evo_info")
        if isinstance(prompt_evolution_stats, dict):
            n_task_description_edits = prompt_evolution_stats.get("n_task_description_edits")
            n_reflection_prompt_edits = prompt_evolution_stats.get("n_reflection_prompt_edits")

            output.append("## Prompt evolution stats")
            output.append("")
            if n_task_description_edits is not None:
                output.append(f"- **Task description edits:** `{n_task_description_edits}`")
            if n_reflection_prompt_edits is not None:
                output.append(f"- **Reflection prompt edits:** `{n_reflection_prompt_edits}`")
            output.append("")

    if include_system:
        system_messages = [m for m in messages if m.get("role") == "system"]
        for i, system_message in enumerate(system_messages, start=1):
            output.append("<details>")
            output.append(f"<summary>System Message {i}</summary>")
            output.append("")
            output.append(fence_text(get_message_content(system_message)))
            output.append("")
            output.append("</details>")
            output.append("")

    step_number = 1

    for i, message in enumerate(messages):
        if message.get("role") != "assistant":
            continue

        if prompt_mode == "previous":
            prompt = format_prompt_previous(messages, i)
        elif prompt_mode == "full":
            prompt = format_prompt_full(messages, i)
        else:
            raise ValueError(f"Unknown prompt mode: {prompt_mode}")

        response = normalize_text(get_message_content(message))

        output.append("<details>")
        output.append(f"<summary><strong>Step {step_number}</strong></summary>")
        output.append("")
        output.append("## Prompt sent to LLM")
        output.append("")
        output.append(fence_text(prompt))
        output.append("")
        output.append("## LLM response")
        output.append("")
        output.append(fence_text(response))
        output.append("")
        output.append("</details>")
        output.append("")

        step_number += 1

    if step_number == 1:
        output.append("_No assistant messages were found in this trajectory._")

    return "\n".join(output)


def convert_one_file(
    trajectory_path: Path,
    output_path: Path,
    prompt_mode: str,
    include_system: bool,
) -> None:
    trajectory = load_json(trajectory_path)
    markdown = trajectory_to_markdown(
        trajectory,
        title=trajectory_path.stem,
        prompt_mode=prompt_mode,
        include_system=include_system,
    )
    output_path.write_text(markdown, encoding="utf-8")


def output_path_for_recursive_trajectory(trajectory_path: Path) -> Path:
    """
    In recursive mode, write <instance_name>.md in the same directory as the
    .traj.json file.

    Example:
        runs/astropy__astropy-13033/something.traj.json
        -> runs/astropy__astropy-13033/astropy__astropy-13033.md
    """
    instance_name = trajectory_path.parent.name
    return trajectory_path.parent / f"{instance_name}.md"


def convert_recursive(
    runs_dir: Path,
    prompt_mode: str,
    include_system: bool,
    overwrite: bool,
) -> None:
    if not runs_dir.is_dir():
        raise ValueError(f"Recursive mode expects a directory, but got: {runs_dir}")

    trajectory_paths = sorted(runs_dir.rglob("*.traj.json"))

    if not trajectory_paths:
        print(f"No .traj.json files found under {runs_dir}")
        return

    converted = 0
    skipped = 0
    failed = 0

    for trajectory_path in trajectory_paths:
        output_path = output_path_for_recursive_trajectory(trajectory_path)

        if output_path.exists() and not overwrite:
            print(f"Skipping existing file: {output_path}")
            skipped += 1
            continue

        try:
            convert_one_file(
                trajectory_path=trajectory_path,
                output_path=output_path,
                prompt_mode=prompt_mode,
                include_system=include_system,
            )
            print(f"Converted: {trajectory_path} -> {output_path}")
            converted += 1
        except Exception as exc:
            print(f"Failed: {trajectory_path} ({type(exc).__name__}: {exc})")
            failed += 1

    print("")
    print("Batch conversion complete.")
    print(f"Converted: {converted}")
    print(f"Skipped:   {skipped}")
    print(f"Failed:    {failed}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert trajectory JSON files to collapsible Markdown."
    )
    parser.add_argument(
        "input_path",
        type=Path,
        help=(
            "Path to a .traj.json file, or to a runs directory when using "
            "-r / --recursive."
        ),
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help=(
            "Path to write the Markdown output in single-file mode. "
            "Not used in recursive mode."
        ),
    )
    parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        help=(
            "Treat input_path as a directory and recursively convert every "
            ".traj.json file found under it."
        ),
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="In recursive mode, overwrite existing Markdown files.",
    )
    parser.add_argument(
        "--prompt-mode",
        choices=["previous", "full"],
        default="previous",
        help=(
            "Use 'previous' to show only the immediately preceding prompt/observation, "
            "or 'full' to show all prior context before each LLM response."
        ),
    )
    parser.add_argument(
        "--include-system",
        action="store_true",
        help="Include collapsible system message sections.",
    )

    args = parser.parse_args()

    if args.recursive:
        if args.output is not None:
            raise ValueError("--output / -o should not be used with --recursive / -r")

        convert_recursive(
            runs_dir=args.input_path,
            prompt_mode=args.prompt_mode,
            include_system=args.include_system,
            overwrite=args.overwrite,
        )
    else:
        if args.output is None:
            raise ValueError("--output / -o is required in single-file mode")

        convert_one_file(
            trajectory_path=args.input_path,
            output_path=args.output,
            prompt_mode=args.prompt_mode,
            include_system=args.include_system,
        )


if __name__ == "__main__":
    main()