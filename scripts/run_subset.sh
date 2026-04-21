#!/usr/bin/env bash

set -euo pipefail

CONFIG_FILE="$1"
CSV_FILE="$2"
OUTPUT_DIR="${3:-runs}"
REDO_FLAG="${4:-}"

mkdir -p "$OUTPUT_DIR"

echo "Reading instances from: $CSV_FILE"
echo "Using config: $CONFIG_FILE"

# Extract instance IDs (skip header), join into comma-separated string
INSTANCE_FILTER=$(tail -n +2 "$CSV_FILE" | cut -d, -f1 | paste -sd "|" -)

echo "Instance filter:"
echo "$INSTANCE_FILTER"
echo

# Build optional args
EXTRA_ARGS=()
if [[ "$REDO_FLAG" == "redo" ]]; then
    EXTRA_ARGS+=(--redo-existing)
fi

mini-extra swebench  --subset verified --split test --config "$CONFIG_FILE" --output "$OUTPUT_DIR" --filter "$INSTANCE_FILTER" "${EXTRA_ARGS[@]}"  

echo "Run complete."
