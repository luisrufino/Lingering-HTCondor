#!/usr/bin/env python3
# run_lingering_mcmc.py

from cobaya.model import get_model
from classy import Class
import numpy as np

# ===============================================================
# 1. Define a safe wrapper around CLASS (one instance per call)
# ===============================================================

def run_class_point(params):
    """
    Creates a new Class() instance for every point — avoids
    Cobaya-CLASS shared memory problems.
    """
    cosmo = Class()

    # Map YAML parameters to CLASS names
    class_params = {
        "output": "tCl",
        "format": "camb",
        "omega_b": params["omega_b"],
        "omega_cdm": params["omega_cdm"],
        "H0": params["H0"],
        "Omega_k": params["Omega_k"],
        "tau_reio": params["tau_reio"],
        "n_s": params["n_s"],
        "A_s": params["A_s"],

        # Lingering universe parameters
        "Omega_e": params["Omega_e"],
        "n_e": params["n_e"],
        "m_s": params["m_s"],
        "a_star": params["a_star"],
        "Delta_e": params["Delta_e"],
        "Delta_s": params["Delta_s"],
        "Delta_rho_s": params["Delta_rho_s"],
        "exact_lingering": True
    }

    try:
        cosmo.set(class_params)
        cosmo.compute()

        # Example observable — modify as needed
        age = cosmo.age()  # Gyr
        return age

    except Exception as e:
        print("[CLASS failure]", e)
        return np.nan
    finally:
        cosmo.struct_cleanup()
        cosmo.empty()

# ===============================================================
# 2. Define a simple likelihood using CLASS output
# ===============================================================

def lingering_likelihood(**params):
    age = run_class_point(params)

    # Example: Gaussian likelihood on age around 13.8 Gyr
    if not np.isfinite(age):
        return -np.inf
    chi2 = (age - 13.8)**2 / (0.5**2)
    return -0.5 * chi2


# ===============================================================
# 3. Cobaya model definition (translated from YAML)
# ===============================================================

info = {
    "likelihood": {
        "lingering_like": {
            "external": lingering_likelihood,
            # 👇 Tell Cobaya to pass these parameters to your likelihood
            "input_params": [
                "Omega_e", "n_s", "a_star", "Omega_k", "omega_cdm",
                "Delta_rho_s", "Delta_s", "Delta_e", "omega_b", "n_e",
                "H0", "tau_reio", "m_s", "A_s"
            ],
        }
    },

    "params": {
        # Lingering parameters
        "Omega_e": {"prior": {"min": 0.001, "max": 0.25}, "proposal": 0.005},
        "a_star": {"value": 1e-15},
        "n_e": {"value": 1.0},
        "m_s": {"value": 3.0},
        "Delta_e": {"prior": {"min": 1e-3, "max": 0.24}, "proposal": 0.005},
        "Delta_s": {"prior": {"min": 1e-4, "max": 0.05}, "proposal": 0.001},
        "Delta_rho_s": {"prior": {"min": 1e-4, "max": 0.05}, "proposal": 0.001},

        # Primordial
        "logA": {"prior": {"min": 1.61, "max": 3.91}, "proposal": 0.001, "drop": True},
        "A_s": {"value": lambda logA: 1e-10 * np.exp(logA)},

        # Geometry and matter
        "Omega_k": {"prior": {"min": 0.0, "max": 0.3}, "proposal": 0.001},
        "H0": {"prior": {"min": 30, "max": 90}, "proposal": 0.5},
        "omega_b": {"prior": {"min": 0.005, "max": 0.1}, "proposal": 0.0001},
        "omega_cdm": {"prior": {"min": 0.001, "max": 0.99}, "proposal": 0.0005},
        "tau_reio": {"prior": {"min": 0.01, "max": 0.8}, "proposal": 0.003},
        "n_s": {"prior": {"min": 0.8, "max": 1.2}, "proposal": 0.002},
    },

    "sampler": {
        "mcmc": {
            "drag": False,
            "oversample_power": 0.4,
            "proposal_scale": 1.9,
            "covmat": "auto",
            "Rminus1_stop": 0.01,
            "Rminus1_cl_stop": 0.2
        }
    },

    "output": "output/test0/"
}

from cobaya.run import run
# ===============================================================
# 4. Run MCMC
# ===============================================================

if __name__ == "__main__":
    updated_info = run(info)
