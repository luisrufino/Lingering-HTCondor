from classy import Class
from math import pi
import matplotlib.pyplot as plt

# Base cosmological settings (fixed for both runs)
common_settings = {# LambdaCDM parameters
                   'h':0.67810,
                   'omega_b':0.02238280,
                   'omega_cdm':0.1201075,
                   'A_s':2.100549e-09,
                   'n_s':0.9660499,
                   'tau_reio':0.05430842 ,
                   # output and precision parameters
                   'output':'tCl,pCl,lCl',
                   'lensing':'yes',
                   'l_max_scalars':5000
                    }

# Exotic fluid parameters
Omega_enum = 0.1
n_e = 3
exotic_params = {
                'Omega_e': Omega_enum,
                'n_e': n_e,
                'a_star': 1e-3,
                #'exact_lingering': 'no'
                }
#exotic_common_settings = common_settings | exotic_params ## This merges the two dictionaries

def compute_cls(exotic = False):
    '''
    Computes the power spectrum from CLASS
    :param cosmology: Requires a dictinoary with all inputs
    :param exotic: Boolean for exotic matter
    :return: Power spectrum
    '''
    M = Class()
    settings = common_settings.copy()
    if exotic:
        settings |= exotic_params
        print(f"Running exotic cosmology")
    else:
        print(f"Running standard cosmology")

    M.set(settings)
    M.compute()
    cl_tot = M.raw_cl(3000)
    cl_lensed = M.lensed_cl(3000)
    M.empty()  # reset input
    #
    M.set(settings)  # new input
    M.set({'temperature contributions': 'tsw'})
    M.compute()
    cl_tsw = M.raw_cl(3000)
    M.empty()
    #
    M.set(settings)
    M.set({'temperature contributions': 'eisw'})
    M.compute()
    cl_eisw = M.raw_cl(3000)
    M.empty()
    #
    M.set(settings)
    M.set({'temperature contributions': 'lisw'})
    M.compute()
    cl_lisw = M.raw_cl(3000)
    M.empty()
    #
    M.set(settings)
    M.set({'temperature contributions': 'dop'})
    M.compute()
    cl_dop = M.raw_cl(3000)
    M.empty()
    return [cl_tot, cl_lensed, cl_tsw, cl_eisw, cl_lisw, cl_dop]



plt.xlim([2,3000])
plt.xlabel(r'Multipole $\ell$')
plt.ylabel(r'$\ell(\ell+1)C_\ell^{TT}/2\pi\ [\mu K^2]$')
plt.grid()

std_cosmo = compute_cls(False)
ell = std_cosmo[0]['ell']
T_CMB_muK = 2.7255e6
factor = (ell*(ell + 1))/(2 * pi) * T_CMB_muK**2

#plt.semilogx(ell,factor * std_cosmo[2]['tt'],'c-',label=r'$\mathrm{T+SW}$ Standard')
#plt.semilogx(ell,factor * std_cosmo[3]['tt'],'r-',label=r'$\mathrm{early-ISW}$ Standard')
#plt.semilogx(ell,factor * std_cosmo[4]['tt'],'y-',label=r'$\mathrm{late-ISW}$ Standard')
#plt.semilogx(ell,factor * std_cosmo[5]['tt'],'g-',label=r'$\mathrm{Doppler}$ Standard')
plt.semilogx(ell,factor * std_cosmo[0]['tt'],'r-',label=r'$\mathrm{total}$ Standard')
#plt.semilogx(ell,factor * std_cosmo[1]['tt'],'k-',label=r'$\mathrm{lensed}$ Standard')


exotic_cosmo = compute_cls(True)
#plt.semilogx(ell,factor * exotic_cosmo[2]['tt'],'c--',label=r'$\mathrm{T+SW}$ Exotic')
#plt.semilogx(ell,factor * exotic_cosmo[3]['tt'],'r--',label=r'$\mathrm{early-ISW}$ Exotic')
#plt.semilogx(ell,factor * exotic_cosmo[4]['tt'],'y--',label=r'$\mathrm{late-ISW}$ Exotic')
#plt.semilogx(ell,factor * exotic_cosmo[5]['tt'],'g--',label=r'$\mathrm{Doppler}$ Exotic')
plt.semilogx(ell,factor * exotic_cosmo[0]['tt'],'b--',label=r'$\mathrm{total}$ Exotic')
#plt.semilogx(ell,factor * exotic_cosmo[1]['tt'],'k--',label=r'$\mathrm{lensed}$ Exotic')
#
plt.legend(loc='right',bbox_to_anchor=(1.4, 0.5))

ome = str(Omega_enum)
frac_Ome = ome.replace(".","p")
plt.savefig(f'cltt_combined_Omega_e__{Omega_enum}_n_e__{n_e}.png',bbox_inches='tight')
