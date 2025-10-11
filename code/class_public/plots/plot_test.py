import numpy as np
import matplotlib.pyplot as plt
import os
# Load CLASS output
data = np.loadtxt("../output/base_2018_plikHM_TTTEEE_lowl_lowE_lensing00_cl_lensed.dat")

# Unpack
ell = data[:,0]
cl_tt = data[:,1]
cl_ee = data[:,2]
cl_te = data[:,3]

# Convert Cl's to D_ell = ell(ell+1)/2pi * Cl * 1e12 [μK^2]
factor = ell * (ell + 1) / (2 * np.pi) * 1e12
d_tt = factor * cl_tt
d_ee = factor * cl_ee
d_te = factor * cl_te  # Note: TE can be negative
combined = d_tt + d_ee + d_te

# Plot
plt.figure(figsize=(10,6))
plt.plot(ell, d_tt, label='TT')
plt.plot(ell, d_ee, label='EE')
plt.plot(ell, d_te, label='TE')
plt.plot(ell, combined, label = "Combined")
plt.xlim(2, 2500)
#plt.xticks([2,10,50,500,1000,1500,2000,2500])
#plt.xscale('log')
#plt.yscale('log')
plt.xlabel(r'Multipole $\ell$')
plt.ylabel(r'$D_\ell\ [\mu K^2]$')
plt.title('CMB Angular Power Spectra from CLASS')
plt.legend()
plt.grid(True)
plt.savefig('combined_PS_default.png')
