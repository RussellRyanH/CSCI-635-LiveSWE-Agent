# File generated with the help of ChatGPT
#
# Usage: python3 get_model_stats.py PATH_TO_DIRECTORY_CONTAINING_RUN_INFORMATION
#
# The script will recursively find all of the log files for the agent and aggregate
# cost and API call information for the benchmark run. It will save the results as a
# CSV file in the directory given as input and print averages to the command line

import argparse
import csv
import json
from pathlib import Path


def find_traj_files(root: Path):
    """Recursively find all files matching *.traj.json under root."""
    return root.rglob("*.traj.json")


def extract_stats(file_path: Path):
    """
    Extract:
      - name: everything before '.traj.json'
      - instance_cost
      - api_calls
    Returns a dict or None if parsing fails / fields are missing.
    """
    try:
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        model_stats = data["info"]["model_stats"]

        return {
            "name": file_path.name[:-len(".traj.json")],
            "instance_cost": model_stats["instance_cost"],
            "api_calls": model_stats["api_calls"],
        }
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"Skipping {file_path}: could not extract stats ({e})")
        return None


def write_csv(output_path: Path, rows):
    """Write aggregated rows to CSV."""
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["name", "instance_cost", "api_calls"]
        )
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(
        description="Aggregate model_stats from *.traj.json files into a CSV."
    )
    parser.add_argument(
        "directory",
        help="Root directory to search recursively"
    )
    args = parser.parse_args()

    root = Path(args.directory).resolve()

    if not root.is_dir():
        print(f"Error: '{root}' is not a valid directory.")
        return 1

    rows = []
    total_cost = 0.0
    total_api_calls = 0

    for file_path in find_traj_files(root):
        stats = extract_stats(file_path)
        if stats is None:
            continue

        rows.append(stats)
        total_cost += float(stats["instance_cost"])
        total_api_calls += int(stats["api_calls"])

    output_csv = root / "aggregated_model_stats.csv"
    write_csv(output_csv, rows)

    count = len(rows)
    avg_cost = total_cost / count if count else 0.0
    avg_api_calls = total_api_calls / count if count else 0.0

    print(f"Processed {count} file(s)")
    print(f"CSV written to: {output_csv}")
    print(f"Total cost: {total_cost}")
    print(f"Total api calls: {total_api_calls}")
    print(f"Average cost: {avg_cost}")
    print(f"Average api_calls: {avg_api_calls}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
