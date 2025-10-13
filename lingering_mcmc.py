#!/usr/bin/env python3
# run_lingering_mcmc.py

from cobaya.run import run

info = {
    "theory": {
        "classy": {
            "path": "/home/lerufino/PlanckData/lingering_sims/background_runs/code/class_public",
            "extra_args": {
                "output": "tCl",
                "format": "camb",
                "background_verbose": 3,
            }
        }
    },

    "likelihood": {
        "planck_2018_lowl.TT": None
    },

    "params": {
        # Lingering Universe parameters
        "Omega_e": {"prior": {"min": 0.001, "max": 0.25}, "proposal": 0.005},
        "a_star": {"value": 1e-15},
        "n_e": {"value": 1.0},
        "m_s": {"value": 3.0},
        "bg_regime": {"value": 1},
        "Delta_e": {"prior": {"min": 1e-3, "max": 0.24}, "proposal": 0.01},
        "Delta_s": {"prior": {"min": 1e-4, "max": 0.05}, "proposal": 0.001},
        "Delta_rho_s": {"prior": {"min": 1e-4, "max": 0.05}, "proposal": 0.001},

        # Primordial spectrum
        "logA": {
            "prior": {"min": 1.61, "max": 3.91},
            "ref": {"dist": "norm", "loc": 3.05, "scale": 0.001},
            "proposal": 0.001,
            "drop": True
        },
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

    "output": "output/test0",
}

if __name__ == "__main__":
    from cobaya.run import run
    import numpy as np
    info["allow_changing_params"] = True
    info["force"] = True
    updated_info = run(info)
