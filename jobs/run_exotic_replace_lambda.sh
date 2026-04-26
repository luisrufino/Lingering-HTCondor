#!/bin/bash

# ------------------------------------------
# run_exotic_replace_lambda.sh
# Exotic fluid REPLACES Lambda (Omega_Lambda = 0)
# Samples n_e and Omega_k with Planck 2018
# ------------------------------------------

export HOME=/home/lerufino
unset LD_LIBRARY_PATH

source /home/lerufino/miniconda3/etc/profile.d/conda.sh
conda activate

cd ~/PlanckData/packages/class_exotic_mcmc

YAML_FILE=configs/exotic_replace_lambda.yaml
OUTPUT_DIR=chains/exotic_replace_lambda
LOGFILE=logs/exotic_replace_lambda.out
LOCK_FILE="$OUTPUT_DIR/exotic_replace_lambda.input.yaml.locked"

mkdir -p "$OUTPUT_DIR" logs

if [ -f "$LOCK_FILE" ]; then
  echo "[INFO] Removing stale lock file at $LOCK_FILE" >> "$LOGFILE"
  rm -f "$LOCK_FILE"
fi

cobaya-run "$YAML_FILE" --packages-path ~/PlanckData/packages --allow-changes --resume > "$LOGFILE" 2>&1
