from classy import Class
cosmo = Class()
cosmo.set({
    'H0': 67.4,
    'omega_b': 0.0224,
    'omega_cdm': 0.12,
    'A_s': 2.1e-9,
    'n_s': 0.965,
    'tau_reio': 0.055,
    'Omega_k': -0.005,
    'Omega_Lambda': 0,
    'n_e': 0.5,
    'output': 'tCl, lCl, pCl',
    'lensing': 'yes',
    'background_verbose': 2,
})
cosmo.compute()
print("h          =", cosmo.h())
print("Omega_m    =", cosmo.Omega_m())
print("Omega_b    =", cosmo.Omega_b())
print("Omega_Lambda =", cosmo.Omega_Lambda())
ba = cosmo.get_background()
print("rho_tot/rho_crit at a=1:", ba['(.)rho_tot'][-1] / ba['(.)rho_crit'][-1])
