#!/bin/bash

# ------------------------------------------
# submit_all.sh
# Submit both MCMC runs to Condor
#
# Usage:
#   ./submit_all.sh              # submit one chain each
#   ./submit_all.sh 4            # submit 4 chains each (faster convergence)
# ------------------------------------------

cd ~/PlanckData/packages/class_exotic_mcmc

N_CHAINS=${1:-1}

echo "Submitting $N_CHAINS chain(s) per model..."

# Make sure scripts are executable
chmod +x jobs/run_baseline_lcdm.sh
chmod +x jobs/run_exotic_free_n.sh

# Create log and chain directories
mkdir -p logs chains/baseline_lcdm chains/exotic_free_n

for i in $(seq 1 $N_CHAINS); do
  echo "  Submitting baseline LCDM chain $i..."
  condor_submit jobs/baseline_lcdm.sub

  echo "  Submitting exotic fluid chain $i..."
  condor_submit jobs/exotic_free_n.sub
done

echo ""
echo "All jobs submitted. Check status with: condor_q"
echo "Check logs in: logs/"
echo "Chains will appear in: chains/"
