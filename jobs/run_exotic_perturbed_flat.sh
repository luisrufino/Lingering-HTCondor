#!/bin/bash

# 2026-04-26: per-chain subdirectories so 4 Condor processes don't collide.

export HOME=/home/lerufino
unset LD_LIBRARY_PATH

source /home/lerufino/miniconda3/etc/profile.d/conda.sh
conda activate

cd ~/PlanckData/packages/class_public_chapter2

PROCESS=$1
if [ -z "$PROCESS" ]; then
  echo "[ERROR] No process number passed."
  exit 1
fi

YAML_FILE=configs/exotic_perturbed_flat.yaml
CHAIN_DIR=chains/exotic_perturbed_flat/chain_${PROCESS}
LOGFILE=logs/exotic_perturbed_flat_chain_${PROCESS}.out
LOCK_FILE="$CHAIN_DIR/exotic_perturbed_flat.input.yaml.locked"

mkdir -p "$CHAIN_DIR" logs

PER_CHAIN_YAML=$CHAIN_DIR/exotic_perturbed_flat_${PROCESS}.yaml
sed "s|^output:.*|output: ${CHAIN_DIR}/exotic_perturbed_flat_${PROCESS}|" \
    "$YAML_FILE" > "$PER_CHAIN_YAML"

if [ -f "$LOCK_FILE" ]; then
  echo "[INFO] Removing stale lock file at $LOCK_FILE" >> "$LOGFILE"
  rm -f "$LOCK_FILE"
fi

cobaya-run "$PER_CHAIN_YAML" --packages-path ~/PlanckData/packages --allow-changes --resume > "$LOGFILE" 2>&1
