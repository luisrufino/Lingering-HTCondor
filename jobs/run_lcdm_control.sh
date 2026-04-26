#!/bin/bash

# ------------------------------------------
# run_lcdm_control.sh
# Standard LCDM with sampled Omega_k.
# Baseline reference for Bayes factor comparison.
# ------------------------------------------

export HOME=/home/lerufino
unset LD_LIBRARY_PATH

source /home/lerufino/miniconda3/etc/profile.d/conda.sh
conda activate

# LCDM does not need the exotic-fluid build; use Chapter 1 dir.
cd ~/PlanckData/packages/class_exotic_mcmc

YAML_FILE=configs/lcdm_control.yaml
OUTPUT_DIR=chains/lcdm_control
LOGFILE=logs/lcdm_control.out
LOCK_FILE="$OUTPUT_DIR/lcdm_control.input.yaml.locked"

mkdir -p "$OUTPUT_DIR" logs

if [ -f "$LOCK_FILE" ]; then
  echo "[INFO] Removing stale lock file at $LOCK_FILE" >> "$LOGFILE"
  rm -f "$LOCK_FILE"
fi

cobaya-run "$YAML_FILE" --packages-path ~/PlanckData/packages --allow-changes --resume > "$LOGFILE" 2>&1
