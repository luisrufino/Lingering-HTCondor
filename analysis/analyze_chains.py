"""
Basic analysis script for comparing baseline LCDM vs exotic fluid chains.
Run this after both MCMCs have converged.

Usage:
    python analyze_chains.py
"""

import numpy as np
import matplotlib.pyplot as plt

try:
    from getdist import MCSamples, plots
    HAS_GETDIST = True
except ImportError:
    print("getdist not installed. Run: pip install getdist")
    HAS_GETDIST = False

# --- Configuration ---
BASELINE_ROOT = "../chains/baseline_lcdm/baseline_lcdm"
EXOTIC_ROOT = "../chains/exotic_free_n/exotic_free_n"
PLOT_DIR = "../plots/"

# Standard LCDM parameters
LCDM_PARAMS = ["H0", "omega_b", "omega_cdm", "tau_reio", "logA", "n_s"]

# New parameters in the exotic model
EXOTIC_PARAMS = ["Omega_e", "n_e", "Omega_k"]

# All parameters for the exotic model
ALL_EXOTIC = LCDM_PARAMS + EXOTIC_PARAMS


def load_chains():
    """Load MCMC chains using getdist."""
    baseline = MCSamples(
        BASELINE_ROOT,
        name_tag="baseline",
        settings={"ignore_rows": 0.3}  # burn-in: discard first 30%
    )

    exotic = MCSamples(
        EXOTIC_ROOT,
        name_tag="exotic",
        settings={"ignore_rows": 0.3}
    )

    return baseline, exotic


def print_summary(baseline, exotic):
    """Print parameter constraints for both models."""

    print("=" * 60)
    print("BASELINE ΛCDM")
    print("=" * 60)
    for p in LCDM_PARAMS:
        try:
            stats = baseline.getInlineLatex(p, limit=1)
            print(f"  {p:15s} = {stats}")
        except:
            pass

    print()
    print("=" * 60)
    print("EXOTIC FLUID MODEL")
    print("=" * 60)
    for p in ALL_EXOTIC:
        try:
            stats = exotic.getInlineLatex(p, limit=1)
            print(f"  {p:15s} = {stats}")
        except:
            pass

    # Best-fit chi2 comparison
    print()
    print("=" * 60)
    print("MODEL COMPARISON")
    print("=" * 60)
    try:
        bl_bestfit = -2 * baseline.getLikeStats().logLike_best
        ex_bestfit = -2 * exotic.getLikeStats().logLike_best
        delta_chi2 = bl_bestfit - ex_bestfit
        print(f"  Baseline best chi2:  {bl_bestfit:.2f}")
        print(f"  Exotic best chi2:    {ex_bestfit:.2f}")
        print(f"  Delta chi2:          {delta_chi2:.2f}")
        print(f"  Extra parameters:    3 (Omega_e, n_e, Omega_k)")
        print(f"  -> Positive = exotic model fits better")
    except:
        print("  (Could not compute best-fit stats - chains may not have converged)")


def plot_exotic_triangle(exotic):
    """Triangle plot for the exotic fluid parameters."""
    g = plots.get_subplot_plotter()
    g.triangle_plot(exotic, EXOTIC_PARAMS, filled=True)
    plt.savefig(PLOT_DIR + "exotic_triangle.pdf", bbox_inches="tight")
    plt.close()
    print(f"Saved: {PLOT_DIR}exotic_triangle.pdf")


def plot_comparison_1d(baseline, exotic):
    """1D posterior comparison for shared parameters."""
    g = plots.get_subplot_plotter(width_inch=12)
    g.plots_1d(
        [baseline, exotic],
        params=LCDM_PARAMS,
        legend_labels=["ΛCDM", "Exotic Fluid"],
        nx=3
    )
    plt.savefig(PLOT_DIR + "lcdm_comparison_1d.pdf", bbox_inches="tight")
    plt.close()
    print(f"Saved: {PLOT_DIR}lcdm_comparison_1d.pdf")


def plot_omega_e_vs_omega_k(exotic):
    """2D posterior: Omega_e vs Omega_k — the key correlation."""
    g = plots.get_single_plotter()
    g.plot_2d(exotic, "Omega_e", "Omega_k", filled=True)
    plt.axhline(0, color="gray", ls="--", alpha=0.5, label="flat")
    plt.axvline(0, color="gray", ls=":", alpha=0.5, label="no exotic")
    plt.legend()
    plt.savefig(PLOT_DIR + "omega_e_vs_omega_k.pdf", bbox_inches="tight")
    plt.close()
    print(f"Saved: {PLOT_DIR}omega_e_vs_omega_k.pdf")


def main():
    if not HAS_GETDIST:
        return

    print("Loading chains...")
    baseline, exotic = load_chains()

    print_summary(baseline, exotic)

    print("\nMaking plots...")
    plot_exotic_triangle(exotic)
    plot_comparison_1d(baseline, exotic)
    plot_omega_e_vs_omega_k(exotic)

    print("\nDone!")


if __name__ == "__main__":
    main()
