#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./collect_tool_and_model_stats.sh PATH_TO_RUN_DIRECTORY
#
# Expected companion scripts:
#   - find_agent_tools_json_files.py
#   - get_model_stats_with_unique_tools.py
#
# By default, this script expects those Python scripts to be in the same
# directory as this shell script. You may also override their paths with:
#   TOOL_STATS_SCRIPT=/path/to/find_agent_tools_json_files.py \
#   MODEL_STATS_SCRIPT=/path/to/get_model_stats_with_unique_tools.py \
#   ./collect_tool_and_model_stats.sh /path/to/runs

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 PATH_TO_RUN_DIRECTORY" >&2
    exit 1
fi

RUN_DIR="$1"

if [[ ! -d "$RUN_DIR" ]]; then
    echo "Error: '$RUN_DIR' is not a valid directory." >&2
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

TOOL_STATS_SCRIPT="${TOOL_STATS_SCRIPT:-$SCRIPT_DIR/find_agent_tools.py}"
MODEL_STATS_SCRIPT="${MODEL_STATS_SCRIPT:-$SCRIPT_DIR/get_model_stats_with_unique_tools.py}"

if [[ ! -f "$TOOL_STATS_SCRIPT" ]]; then
    echo "Error: tool stats script not found at '$TOOL_STATS_SCRIPT'." >&2
    exit 1
fi

if [[ ! -f "$MODEL_STATS_SCRIPT" ]]; then
    echo "Error: aggregated model stats script not found at '$MODEL_STATS_SCRIPT'." >&2
    exit 1
fi

RUN_DIR_ABS="$(cd "$RUN_DIR" && pwd)"
SUMMARY_FILE="$RUN_DIR_ABS/aggregated_model_stats_summary.txt"

echo "Generating per-trajectory tool JSON files..."
python3 "$TOOL_STATS_SCRIPT" "$RUN_DIR_ABS" --json --recursive --no-diff

echo
echo "Aggregating model and tool statistics..."
python3 "$MODEL_STATS_SCRIPT" "$RUN_DIR_ABS" | tee "$SUMMARY_FILE"

echo
echo "Summary output written to:"
echo "$SUMMARY_FILE"
