#!/usr/bin/env python
"""
collect_validation_report.py   (v3 — 2026-04-26)

v3 fix: CLASS appends `_cl_lensed.dat` (with a leading underscore)
to roots when overwrite_root=yes, producing files like
    test_t1_lcdm__cl_lensed.dat   (note: two underscores total)
The collector now searches for that variant in addition to the
older auto-numbered NN_ form.
"""

import os
import glob
import numpy as np

REPORT_PATH = "validation_report.txt"

COMPARISONS = [
    ("Test 2 (n_e=0.1 vs fld w0=-0.967)", "output/test_t2a_exotic_", "output/test_t2b_fld_", 5e-3),
    ("Test 3 (n_e=1.0 vs fld w0=-2/3)",   "output/test_t3a_exotic_", "output/test_t3b_fld_", 5e-3),
]

SINGLE_RUNS = [
    ("Test 1 (LCDM regression)",  "output/test_t1_lcdm_",     "validation_logs/t1_lcdm.log"),
    ("Test 2a (Exotic n_e=0.1)",  "output/test_t2a_exotic_",  "validation_logs/t2a_exotic.log"),
    ("Test 2b (fld w0=-0.967)",   "output/test_t2b_fld_",     "validation_logs/t2b_fld.log"),
    ("Test 3a (Exotic n_e=1)",    "output/test_t3a_exotic_",  "validation_logs/t3a_exotic.log"),
    ("Test 3b (fld w0=-2/3)",     "output/test_t3b_fld_",     "validation_logs/t3b_fld.log"),
    ("Test 4 (boundary n_e=2)",   "output/test_t4_boundary_", "validation_logs/t4_boundary.log"),
]


def find_cl_lensed(root):
    """
    Try every plausible CLASS naming convention for the lensed Cl file.
    Returns the path of whichever exists, or None.
    """
    candidates = [
        root + "cl_lensed.dat",       # bare append
        root + "_cl_lensed.dat",      # CLASS adds leading underscore (overwrite_root=yes case)
        root + "00_cl_lensed.dat",    # CLASS auto-numbered (no overwrite_root)
    ]
    candidates += sorted(glob.glob(root + "??_cl_lensed.dat"))
    candidates += sorted(glob.glob(root + "*cl_lensed.dat"))  # last-resort wildcard
    seen = set()
    for path in candidates:
        if path in seen:
            continue
        seen.add(path)
        if os.path.exists(path):
            return path
    return None


def tail_log(path, n=15):
    if not os.path.exists(path):
        return f"  (log file {path} not found)\n"
    with open(path) as f:
        lines = f.readlines()
    return "".join(lines[-n:]) if lines else "  (empty log)\n"


def grep_log(path, patterns):
    if not os.path.exists(path):
        return ""
    matches = []
    with open(path) as f:
        for line in f:
            if any(p in line for p in patterns):
                matches.append(line.rstrip())
    return "\n".join(matches)


def compare_cls(file_a, file_b, threshold):
    if not (file_a and file_b and os.path.exists(file_a) and os.path.exists(file_b)):
        return {"error": f"missing file(s): a={file_a} b={file_b}"}
    a = np.loadtxt(file_a)
    b = np.loadtxt(file_b)
    n = min(len(a), len(b))
    a = a[:n]
    b = b[:n]
    l = a[:, 0]
    tt_a = a[:, 1]
    tt_b = b[:, 1]
    mask = (l >= 10) & (l <= 2000) & (tt_b != 0)
    if mask.sum() == 0:
        return {"error": "no overlapping ell range"}
    rel = np.abs(tt_a[mask] - tt_b[mask]) / np.abs(tt_b[mask])
    l_subset = l[mask]
    idx_max = rel.argmax()
    return {
        "max_rel_diff_TT": float(rel.max()),
        "at_ell": float(l_subset[idx_max]),
        "median_rel_diff_TT": float(np.median(rel)),
        "n_ell_compared": int(mask.sum()),
        "threshold": threshold,
    }


def main():
    out = []
    out.append("=" * 70)
    out.append("CHAPTER 2 PERTURBATION VALIDATION REPORT (v3)")
    out.append("Generated: 2026-04-26")
    out.append("=" * 70)
    out.append("")

    out.append("-" * 70)
    out.append("SECTION 1: Run completion + exotic-fluid activation check")
    out.append("-" * 70)
    out.append("")
    for label, root, log in SINGLE_RUNS:
        out.append(f"### {label}")
        cl_file = find_cl_lensed(root)
        if cl_file:
            arr = np.loadtxt(cl_file)
            out.append(f"  Cl file: {cl_file}")
            out.append(f"  N_lines = {len(arr)}, l_max = {int(arr[-1, 0])}")
        else:
            out.append(f"  *** Cl file MISSING for root: {root}")
        budget = grep_log(log, ["matched budget", "Exotic Fluid", "Exotic lingering fluid"])
        if budget.strip():
            out.append("  Budget/exotic prints:")
            for line in budget.split("\n"):
                out.append(f"    {line}")
        else:
            out.append("  (no budget/exotic prints in log)")
        out.append("  Tail of log:")
        for line in tail_log(log, n=8).rstrip().split("\n"):
            out.append(f"    {line}")
        out.append("")

    out.append("-" * 70)
    out.append("SECTION 2: Cl comparisons (exotic vs fld)")
    out.append("-" * 70)
    out.append("")
    for label, root_a, root_b, thresh in COMPARISONS:
        file_a = find_cl_lensed(root_a)
        file_b = find_cl_lensed(root_b)
        out.append(f"### {label}")
        out.append(f"  exotic file: {file_a}")
        out.append(f"  fld file:    {file_b}")
        out.append(f"  pass threshold: max_rel_diff_TT < {thresh:.0e}")
        result = compare_cls(file_a, file_b, thresh)
        if "error" in result:
            out.append(f"  ERROR: {result['error']}")
        else:
            verdict = "PASS" if result["max_rel_diff_TT"] < thresh else "FAIL"
            out.append(f"  max relative TT difference: {result['max_rel_diff_TT']:.3e}")
            out.append(f"  at ell = {result['at_ell']:.0f}")
            out.append(f"  median relative TT difference: {result['median_rel_diff_TT']:.3e}")
            out.append(f"  N ells compared: {result['n_ell_compared']}")
            out.append(f"  VERDICT: {verdict}")
        out.append("")

    out.append("-" * 70)
    out.append("SECTION 3: Error scan (any 'Error', 'ERROR', 'failed' in any log)")
    out.append("-" * 70)
    out.append("")
    found_any = False
    for label, _, log in SINGLE_RUNS:
        errors = grep_log(log, ["Error", "ERROR", "failed", "FAILED", "abort"])
        if errors.strip():
            found_any = True
            out.append(f"### {label}")
            for line in errors.split("\n"):
                out.append(f"  {line}")
            out.append("")
    if not found_any:
        out.append("  (no error patterns found in any log)")
        out.append("")

    out.append("=" * 70)
    out.append("END OF REPORT")
    out.append("=" * 70)

    text = "\n".join(out)
    with open(REPORT_PATH, "w") as f:
        f.write(text + "\n")

    print(text)
    print(f"\nReport saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
