#!/bin/bash

# ------------------------------------------
# submit_all_chapter2.sh
# Submit the three Chapter-2-era MCMC runs to Condor:
#   1. LCDM control (baseline for Bayes factor)
#   2. Exotic fluid perturbed (Chapter 2 main result)
#   3. Exotic fluid perturbed, flat (degeneracy diagnostic)
#
# The number of chains per run is controlled by the `queue N`
# line inside each .sub file (currently set to 4).
#
# Usage:
#   ./submit_all_chapter2.sh
# ------------------------------------------

# Note: this script lives in the directory that contains the
# `jobs/` and `configs/` folders. Adjust if your layout differs.
cd ~/PlanckData/packages/class_public_chapter2

# Make sure run scripts are executable
chmod +x jobs/run_lcdm_control.sh
chmod +x jobs/run_exotic_perturbed.sh
chmod +x jobs/run_exotic_perturbed_flat.sh

# Create log and chain directories
mkdir -p logs \
         chains/lcdm_control \
         chains/exotic_perturbed \
         chains/exotic_perturbed_flat

echo "Submitting Chapter 2 runs..."

echo "  -> LCDM control"
condor_submit jobs/lcdm_control_multi.sub

echo "  -> Exotic fluid (perturbed, curvature sampled)"
condor_submit jobs/exotic_perturbed_multi.sub

echo "  -> Exotic fluid (perturbed, Omega_k = 0)"
condor_submit jobs/exotic_perturbed_flat_multi.sub

echo ""
echo "All jobs submitted."
echo "  Check status:  condor_q"
echo "  Logs:          logs/"
echo "  Chains:        chains/{lcdm_control, exotic_perturbed, exotic_perturbed_flat}"
