#!/bin/bash

# ------------------------------------------
# run_lingering.sh
# Script to run or resume a Cobaya MCMC job
# ------------------------------------------

export HOME=/home/lerufino  # Required so Cobaya can find ~/.cobaya/packages
unset LD_LIBRARY_PATH

# Load Conda so `conda activate` works
source /home/lerufino/miniconda3/etc/profile.d/conda.sh

# Activate your Cobaya environment
conda activate

# Move to your working directory
cd ~/PlanckData/lingering_sims/background_runs

# Set variables
YAML_FILE=yamls/test0.yaml                     # YAML config file for Cobaya

LOGFILE=output/test0/logs/test0.out                 # Where all output is logged

OUTPUT_DIR=output/test0

LOCK_FILE="$OUTPUT_DIR/input.yaml.locked"

LOGFILE="$OUTPUT_DIR/logs/test0.out"

# Create output directories if they don't exist
mkdir -p "$OUTPUT_DIR/logs"

# Remove lock file if it exists — we assume manual resume
if [ -f "$LOCK_FILE" ]; then
  echo "[INFO] Removing stale lock file at $LOCK_FILE" >> "$LOGFILE"
  rm -f "$LOCK_FILE"
fi

# Always resume using --allow-changes, if --allow-changes doesnt work, it will try --resume
cobaya-run "$YAML_FILE" --allow-changes > "$LOGFILE" 2>&1
