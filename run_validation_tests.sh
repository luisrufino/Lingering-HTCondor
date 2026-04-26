#!/bin/bash

# ============================================================
# run_validation_tests.sh   (v2 — 2026-04-26)
# Chapter 2 perturbation validation for CLASS.
#
# Changes from v1:
#   - Test 2 now uses n_e=0.1 / w_fld=-0.96666 instead of n_e=0 / w=-1,
#     because exact w=-1 hits a 1/(1+w) singularity in both the exotic
#     code and stock CLASS fld (CLASS-shipped behavior, not a bug).
#   - All .ini files use `overwrite_root = yes` so CLASS doesn't append
#     _NN_ to filenames and the python collector finds them.
#
# Run from ~/PlanckData/packages/class_public_chapter2/
# ============================================================

set -e

mkdir -p validation_inis
mkdir -p output
mkdir -p validation_logs

# ---------- Test 1: LCDM regression ----------
cat > validation_inis/test_t1_lcdm.ini << 'EOF'
h = 0.674
omega_b = 0.0224
omega_cdm = 0.12
A_s = 2.1e-9
n_s = 0.965
tau_reio = 0.055
output = tCl, lCl, pCl
lensing = yes
l_max_scalars = 2500
root = output/test_t1_lcdm_
background_verbose = 1
overwrite_root = yes
EOF

# ---------- Test 2a: Exotic n_e = 0.1  (w_e = -0.96667) ----------
cat > validation_inis/test_t2a_exotic.ini << 'EOF'
h = 0.674
omega_b = 0.0224
omega_cdm = 0.12
A_s = 2.1e-9
n_s = 0.965
tau_reio = 0.055
Omega_e = 0.685
n_e = 0.1
cs2_e = 1.0
output = tCl, lCl, pCl
lensing = yes
l_max_scalars = 2500
root = output/test_t2a_exotic_
background_verbose = 1
overwrite_root = yes
EOF

# ---------- Test 2b: fld w0 = -0.96667 ----------
cat > validation_inis/test_t2b_fld.ini << 'EOF'
h = 0.674
omega_b = 0.0224
omega_cdm = 0.12
A_s = 2.1e-9
n_s = 0.965
tau_reio = 0.055
Omega_fld = 0.685
w0_fld = -0.96666666666666667
wa_fld = 0.0
cs2_fld = 1.0
use_ppf = no
output = tCl, lCl, pCl
lensing = yes
l_max_scalars = 2500
root = output/test_t2b_fld_
background_verbose = 1
overwrite_root = yes
EOF

# ---------- Test 3a: Exotic n_e = 1 ----------
cat > validation_inis/test_t3a_exotic.ini << 'EOF'
h = 0.674
omega_b = 0.0224
omega_cdm = 0.12
A_s = 2.1e-9
n_s = 0.965
tau_reio = 0.055
Omega_e = 0.685
n_e = 1.0
cs2_e = 1.0
output = tCl, lCl, pCl
lensing = yes
l_max_scalars = 2500
root = output/test_t3a_exotic_
background_verbose = 1
overwrite_root = yes
EOF

# ---------- Test 3b: fld w0 = -2/3 ----------
cat > validation_inis/test_t3b_fld.ini << 'EOF'
h = 0.674
omega_b = 0.0224
omega_cdm = 0.12
A_s = 2.1e-9
n_s = 0.965
tau_reio = 0.055
Omega_fld = 0.685
w0_fld = -0.66666666666666667
wa_fld = 0.0
cs2_fld = 1.0
use_ppf = no
output = tCl, lCl, pCl
lensing = yes
l_max_scalars = 2500
root = output/test_t3b_fld_
background_verbose = 1
overwrite_root = yes
EOF

# ---------- Test 4: boundary n_e = 2 ----------
cat > validation_inis/test_t4_boundary.ini << 'EOF'
h = 0.674
omega_b = 0.0224
omega_cdm = 0.12
A_s = 2.1e-9
n_s = 0.965
tau_reio = 0.055
Omega_e = 0.005
n_e = 2.0
cs2_e = 1.0
output = tCl, lCl, pCl
lensing = yes
l_max_scalars = 2500
root = output/test_t4_boundary_
background_verbose = 1
overwrite_root = yes
EOF

# Wipe any prior outputs so CLASS doesn't fall back to auto-incrementing
rm -f output/test_t1_lcdm_*  output/test_t2a_exotic_*  output/test_t2b_fld_*
rm -f output/test_t3a_exotic_*  output/test_t3b_fld_*  output/test_t4_boundary_*

# ============================================================
# Run each test
# ============================================================

for tag in t1_lcdm t2a_exotic t2b_fld t3a_exotic t3b_fld t4_boundary ; do
  echo ">>> Running test: $tag"
  if ./class validation_inis/test_${tag}.ini > validation_logs/${tag}.log 2>&1 ; then
    echo "    ./class exited 0"
  else
    echo "    ./class FAILED — see validation_logs/${tag}.log"
  fi
done

echo ""
echo "All tests attempted."
echo "Now run: python collect_validation_report.py"
