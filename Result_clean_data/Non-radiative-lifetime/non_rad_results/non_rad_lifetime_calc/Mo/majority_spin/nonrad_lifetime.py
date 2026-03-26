from __future__ import print_function

import sys
import os
import yaml
import numpy as np
from numpy.linalg import norm
from datetime import datetime

from scipy.optimize import fsolve
import matplotlib.pyplot as plt

code_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../NonRad/code')) 
# Add the directory to sys.path
sys.path.append(code_dir)

from constant import indent
from io_package import read_cell_and_pos_auto
from libplot import plot_tot_Q, plot_eig_Q, plot_overlap_Q, plot_cp_T
from libcalc import calc_dQ, calc_freq, calc_wif, calc_phonon_part, calc_cp_T, \
    calc_phonon_part_T0_HR, calc_lifetime_T, calc_dE
from libreadqe import read_pos_and_etot_ratio

np.seterr(all="log")

# Input description:
# calc_phonon_part(dE, dQ, freqi, freqf, list_T, order_x)


def lifetime_func(x, ZPL_list, lifetime_list):
    return np.interp(x, ZPL_list, lifetime_list)

### Non radiative lifetime for MoVO defect:

# 3A2 - 3E
dQ = 1.19486 # dQ 3E <-> 3A2 in amu^1/2 . Ang
weff_i = 27.709556721516613 # omega_eff 3E in meV
weff_f = 29.036434368899307 # omega_eff 3A2 in meV
temp = 300.4693366708385156 # temperature in K

# Test different ZPL and calculate the lifetime:
ZPL_list = [1.99, 2.08] # ZPL values in eV

wif = 0.0513 # Value I got from our code (in paper), # Value I got from CVW code: 0.05482317861496943 # wif from WSWQ files
g = 1 # Factor for defect symmetry.

lifetime_list = []
xif_list = []

for ZPL in ZPL_list:
    list_phonon_part = calc_phonon_part(ZPL, dQ, weff_i,
                weff_f,
                [temp],
                0
            )
    xif_list.append(list_phonon_part[0][1])
    lifetime_list.append(calc_lifetime_T(g, wif, list_phonon_part, 'nonrad')[0][1])

### Save data in txt file:
np.savetxt('lifetime_data_3E_3A2.txt', np.array([ZPL_list, lifetime_list]).T)
np.savetxt('xif_3E_3A2.txt', np.array([ZPL_list, xif_list]).T)

