from __future__ import print_function

from io_package import read_cell_and_pos_auto
from libplot import plot_tot_Q, plot_eig_Q, plot_overlap_Q, plot_cp_T
from libcalc import calc_dQ, calc_freq, calc_wif, calc_phonon_part, calc_cp_T, \
    calc_phonon_part_T0_HR, calc_lifetime_T, calc_dE
from libreadqe import read_pos_and_etot_ratio
import sys
import os
import yaml
import numpy as np
from numpy.linalg import norm
from datetime import datetime
from constant import indent
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
np.seterr(all="log")

# Input description:
# calc_phonon_part(dE, dQ, freqi, freqf, list_T, order_x)


def lifetime_func(x, ZPL_list, lifetime_list):
    return np.interp(x, ZPL_list, lifetime_list)

# 1A1 - 3E
# Test different ZPL and plot the lifetime:
#dQ = 1.19486 # dQ 3E <-> 1A1 in amu^1/2 . Ang
#weff_i = 27.709556721516613 # omega_eff 3E in meV
#weff_f = 29.036434368899307 # omega_eff 1A1 in meV
#temp = 300.4693366708385156 # temperature in K

# 3A2 - 1E
# Test different ZPL and plot the lifetime:
dQ = 0.405588 # dQ 3A2 <-> 1E in amu^1/2 . Ang
weff_i = 15.45 # omega_eff 3E in meV
weff_f = 29.036434368899307 # omega_eff 1A1 in meV
temp = 300.4693366708385156 # temperature in K


# Test different ZPL and plot the lifetime:
ZPL_list = np.linspace(0.5, 1.55, 30) # ZPL values in eV
lifetime_list = []
lambda_perp = 3668 # lambda_perp 3E->1A1: 450 GHz | lambda_perp 1E->3A2: 3668 GHz
for ZPL in ZPL_list:
    list_phonon_part = calc_phonon_part(
                ZPL,
                dQ,
                weff_i,
                weff_f,
                [temp],
                0
            )
    lifetime_list.append(calc_lifetime_T(3, lambda_perp, list_phonon_part, 'isc')[0][1])

lifetime_list = np.array(lifetime_list)*10**6

### Save data in txt file:
np.savetxt('lifetime_data_1E_3A2.txt', np.array([ZPL_list, lifetime_list]).T)


f = lambda x: lifetime_func(x, ZPL_list, lifetime_list) - 0.5
inf_val = fsolve(f, 0.7)[0]

f = lambda x: lifetime_func(x, ZPL_list, lifetime_list) - 10
sup_val = fsolve(f, 0.7)[0]


title_size = 25
tick_size = 20
font_size = 23    
plt.rcParams["figure.titlesize"] = title_size
plt.rcParams["lines.linewidth"] = 1.7
plt.rcParams["xtick.labelsize"] = tick_size
plt.rcParams["ytick.labelsize"] = tick_size
plt.rcParams["font.size"] = font_size
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = "Arial"
plt.rcParams["legend.fontsize"] = 15
plt.rcParams["figure.figsize"] = (7,6)
plt.rcParams["figure.dpi"] = 100

plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = 'Bitstream Vera Sans'

fig, ax = plt.subplots()

ax.plot(ZPL_list, lifetime_list,'-b', linewidth = 1.5)

y1 = 0.5
y2 = 10
ax.plot([ZPL_list[0], ZPL_list[-1]], [0.5, 0.5], '--r', linewidth=1)
ax.plot([ZPL_list[0], ZPL_list[-1]], [10, 10], '--r', linewidth=1)
ax.fill_between(ZPL_list, y1, y2, color='r', alpha=0.2)

ax.plot([inf_val, inf_val],[lifetime_list[0],lifetime_list[-1]], '--r', linewidth=1)
ax.plot([sup_val, sup_val],[lifetime_list[0],lifetime_list[-1]], '--r', linewidth=1)

ax.set_ylabel("ISC lifetime (microsecond)")
ax.set_xlabel("ZPL 1A1 -> 3E in eV")
plt.yscale('log')
plt.show()

