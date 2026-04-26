#!/bin/bash

# ------------------------------------------
# run_exotic_perturbed.sh
# Chapter 2: exotic fluid REPLACES Lambda (Omega_Lambda = 0)
# WITH consistent first-order perturbations, cs2_e = 1.0.
# Samples n_e and Omega_k with Planck 2018.
# ------------------------------------------

export HOME=/home/lerufino
unset LD_LIBRARY_PATH

source /home/lerufino/miniconda3/etc/profile.d/conda.sh
conda activate

# Chapter 2 binary lives in the perturbed-build directory.
cd ~/PlanckData/packages/class_public_chapter2

YAML_FILE=configs/exotic_perturbed.yaml
OUTPUT_DIR=chains/exotic_perturbed
LOGFILE=logs/exotic_perturbed.out
LOCK_FILE="$OUTPUT_DIR/exotic_perturbed.input.yaml.locked"

mkdir -p "$OUTPUT_DIR" logs

if [ -f "$LOCK_FILE" ]; then
  echo "[INFO] Removing stale lock file at $LOCK_FILE" >> "$LOGFILE"
  rm -f "$LOCK_FILE"
fi

cobaya-run "$YAML_FILE" --packages-path ~/PlanckData/packages --allow-changes --resume > "$LOGFILE" 2>&1
