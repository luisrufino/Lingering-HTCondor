#!/bin/bash

# ------------------------------------------
# run_baseline_lcdm.sh
# Baseline ΛCDM MCMC with Planck 2018
# ------------------------------------------

export HOME=/home/lerufino
unset LD_LIBRARY_PATH

source /home/lerufino/miniconda3/etc/profile.d/conda.sh
conda activate

cd ~/PlanckData/packages/class_exotic_mcmc

YAML_FILE=configs/baseline_lcdm.yaml
OUTPUT_DIR=chains/baseline_lcdm
LOGFILE=logs/baseline_lcdm.out
LOCK_FILE="$OUTPUT_DIR/baseline_lcdm.input.yaml.locked"

mkdir -p "$OUTPUT_DIR" logs

if [ -f "$LOCK_FILE" ]; then
  echo "[INFO] Removing stale lock file at $LOCK_FILE" >> "$LOGFILE"
  rm -f "$LOCK_FILE"
fi

cobaya-run "$YAML_FILE" --packages-path ~/PlanckData/packages --allow-changes --resume > "$LOGFILE" 2>&1
