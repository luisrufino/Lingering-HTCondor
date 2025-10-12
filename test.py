from classy import Class

cosmo = Class()
cosmo.set({
    "output": "tCl",
    "Omega_e": 0.05,
    "n_e": 1.0,
    "m_s": 3.0,
    "a_star": 1e-15,
    "Delta_e": 0.1,
    "Delta_s": 0.01,
    "Delta_rho_s": 0.01,
    "H0": 67,
    "omega_b": 0.0224,
    "omega_cdm": 0.12,
    "background_verbose": 3,
})
cosmo.compute()
