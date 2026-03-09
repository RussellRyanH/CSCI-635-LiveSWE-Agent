#!/usr/bin/env bash

set -euo pipefail

CSV_FILE="$1"
OUTPUT_DIR="${2:-runs}"

mkdir -p "$OUTPUT_DIR"

echo "Reading instances from: $CSV_FILE"

# Extract instance IDs (skip header), join into comma-separated string
INSTANCE_FILTER=$(tail -n +2 "$CSV_FILE" | cut -d, -f1 | paste -sd "|" -)

echo "Instance filter:"
echo "$INSTANCE_FILTER"
echo

mini-extra swebench  --subset verified --split test --config live-swe-agent/config/livesweagent_swebench.yaml --output "$OUTPUT_DIR" --filter "$INSTANCE_FILTER"  

echo "Run complete."
