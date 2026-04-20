#!/bin/bash

# ------------------------------------------
# run_exotic_replace_lambda_multi.sh
# Runs one independent chain. Chain ID passed as argument.
# Each chain writes to its own output directory.
# ------------------------------------------

CHAIN_ID=$1

export HOME=/home/lerufino
unset LD_LIBRARY_PATH

source /home/lerufino/miniconda3/etc/profile.d/conda.sh
conda activate

cd ~/PlanckData/packages/class_exotic_mcmc

YAML_FILE=configs/exotic_replace_lambda.yaml
OUTPUT_DIR=chains/exotic_replace_lambda/chain_${CHAIN_ID}
LOGFILE=logs/exotic_replace_lambda_chain_${CHAIN_ID}.out

mkdir -p "$OUTPUT_DIR" logs

# Remove stale lock file if present
LOCK_FILE="$OUTPUT_DIR/exotic_replace_lambda_${CHAIN_ID}.input.yaml.locked"
if [ -f "$LOCK_FILE" ]; then
  echo "[INFO] Removing stale lock file" >> "$LOGFILE"
  rm -f "$LOCK_FILE"
fi

# Run Cobaya with a chain-specific output path
# The -o flag overrides the output path in the yaml
cobaya-run "$YAML_FILE" \
  --packages-path ~/PlanckData/packages \
  -o "$OUTPUT_DIR/exotic_replace_lambda_${CHAIN_ID}" \
  --allow-changes --resume > "$LOGFILE" 2>&1
