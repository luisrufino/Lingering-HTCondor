#!/bin/bash

# ------------------------------------------
# run_exotic_perturbed_flat.sh
# Chapter 2 variant: perturbed exotic fluid with Omega_k = 0 fixed.
# Degeneracy diagnostic — compare n_e posterior against the
# curvature-sampled run to test (n_e, Omega_k) entanglement.
# ------------------------------------------

export HOME=/home/lerufino
unset LD_LIBRARY_PATH

source /home/lerufino/miniconda3/etc/profile.d/conda.sh
conda activate

# Same Chapter 2 binary as the curvature-sampled run.
cd ~/PlanckData/packages/class_public_chapter2

YAML_FILE=configs/exotic_perturbed_flat.yaml
OUTPUT_DIR=chains/exotic_perturbed_flat
LOGFILE=logs/exotic_perturbed_flat.out
LOCK_FILE="$OUTPUT_DIR/exotic_perturbed_flat.input.yaml.locked"

mkdir -p "$OUTPUT_DIR" logs

if [ -f "$LOCK_FILE" ]; then
  echo "[INFO] Removing stale lock file at $LOCK_FILE" >> "$LOGFILE"
  rm -f "$LOCK_FILE"
fi

cobaya-run "$YAML_FILE" --packages-path ~/PlanckData/packages --allow-changes --resume > "$LOGFILE" 2>&1
