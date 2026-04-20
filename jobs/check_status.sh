#!/bin/bash

# ------------------------------------------
# check_status.sh
# Quick status check for all MCMC runs
# ------------------------------------------

cd ~/PlanckData/packages/class_exotic_mcmc

echo "========================================"
echo "  MCMC Status Check — $(date)"
echo "========================================"

echo ""
echo "--- 1. Job Status (condor_q) ---"
echo ""
condor_q

echo ""
echo "--- 2. Chain Sample Counts ---"
echo ""
echo "Exotic fluid chains:"
wc -l chains/exotic_replace_lambda/chain_*/*.txt 2>/dev/null || echo "  No exotic chain files found"
echo ""
echo "Baseline LCDM:"
wc -l chains/baseline_lcdm/*.txt 2>/dev/null || echo "  No baseline chain files found"
echo ""
echo "Exotic + Lambda (old run, if present):"
wc -l chains/exotic_free_n/*.txt 2>/dev/null || echo "  No exotic+Lambda chain files found"

echo ""
echo "--- 3. Recent Log Output ---"
echo ""
echo ">> Exotic chain 0 (last 3 lines):"
tail -3 logs/exotic_replace_lambda_chain_0.out 2>/dev/null || echo "  No log found"
echo ""
echo ">> Exotic chain 1 (last 3 lines):"
tail -3 logs/exotic_replace_lambda_chain_1.out 2>/dev/null || echo "  No log found"
echo ""
echo ">> Exotic chain 2 (last 3 lines):"
tail -3 logs/exotic_replace_lambda_chain_2.out 2>/dev/null || echo "  No log found"
echo ""
echo ">> Exotic chain 3 (last 3 lines):"
tail -3 logs/exotic_replace_lambda_chain_3.out 2>/dev/null || echo "  No log found"
echo ""
echo ">> Baseline LCDM (last 3 lines):"
tail -3 logs/baseline_lcdm.out 2>/dev/null || echo "  No log found"

echo ""
echo "--- 4. Convergence (R-1 values) ---"
echo ""
echo "Baseline LCDM:"
grep "R-1" logs/baseline_lcdm.out 2>/dev/null | tail -3 || echo "  No R-1 values yet"
echo ""
echo "Exotic chain 0:"
grep "Convergence" logs/exotic_replace_lambda_chain_0.out 2>/dev/null | tail -3 || echo "  No R-1 values yet"
echo ""
echo "Exotic chain 1:"
grep "Convergence" logs/exotic_replace_lambda_chain_1.out 2>/dev/null | tail -3 || echo "  No R-1 values yet"
echo ""
echo "Exotic chain 2:"
grep "Convergence" logs/exotic_replace_lambda_chain_2.out 2>/dev/null | tail -3 || echo "  No R-1 values yet"
echo ""
echo "Exotic chain 3:"
grep "Convergence" logs/exotic_replace_lambda_chain_3.out 2>/dev/null | tail -3 || echo "  No R-1 values yet"

echo ""
echo "--- 5. Any Errors? ---"
echo ""
for f in logs/exotic_replace_lambda_chain_*.out logs/baseline_lcdm.out; do
  ERRORS=$(grep -ci "error" "$f" 2>/dev/null)
  if [ "$ERRORS" -gt 0 ] 2>/dev/null; then
    echo "  WARNING: $f has $ERRORS error lines"
  fi
done
echo "  (No output above = no errors found)"

echo ""
echo "========================================"
echo "  Done."
echo "========================================"
