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

np.seterr(all="log")

# def calc_phonon_part(dE, dQ, freqi, freqf, list_T, order_x):

# list_phonon_part = calc_phonon_part(
#             1.0746,
#             1.8,
#             34.3199370545441,
#             39.640855073772514,
#             [300.4693366708385156],
#             1
#         )

# print("NbVO majority: ", list_phonon_part)

# list_phonon_part = calc_phonon_part(
#             1.7229,
#             3.83629,
#             20.290425079508736,
#             20.264982849908154,
#             [300.4693366708385156],
#             1
#         )
# print("NbVO minority: ", list_phonon_part)
# print("NbVO minority lifetime: ", calc_lifetime_T(3, 0.0462, list_phonon_part, 'nonrad'))

# list_phonon_part = calc_phonon_part(
#             1.56144,
#             5.04901,
#             17.125441014641346,
#             16.609131582307704,
#             [300.4693366708385156],
#             1
#         )
# print("MoVO minority: ", list_phonon_part)
# print("MoVO minority lifetime: ", calc_lifetime_T(3, 0.0375, list_phonon_part, 'nonrad'))


# list_phonon_part = calc_phonon_part(
#             1.98601,
#             1.19486,
#             27.709556721516613,
#             29.036434368899307,
#             [300.4693366708385156],
#             1
#         )
# print("MoVO majority: ", list_phonon_part)

# list_phonon_part = calc_phonon_part(
#             0.834,
#             0.405588,
#             15.44973078041893,
#             29.036434368899307,
#             [300.4693366708385156],
#             0
#         )
# print("MoVO majority ISC: ", list_phonon_part)
# print("MoVO majority ISC lifetime lambda perp: ", calc_lifetime_T(3, 3668, list_phonon_part, 'isc'))
# print("MoVO majority ISC lifetime lambda z: ", calc_lifetime_T(3, 1E-10, list_phonon_part, 'isc'))

# 3A2 - 1E
# list_phonon_part = calc_phonon_part(
#             0.834,
#             0.405588,
#             15.44973078041893,
#             29.036434368899307,
#             [300.4693366708385156],
#             0
# )
# print("MoVO majority ISC: ", list_phonon_part)
# print("MoVO majority ISC lifetime lambda perp: ", calc_lifetime_T(3, 3668, list_phonon_part, 'isc'))
# print("MoVO majority ISC lifetime lambda z: ", calc_lifetime_T(3, 0.015, list_phonon_part, 'isc'))

# Test different ZPL and plot the lifetime:
ZPL_list = np.linspace(0.5, 1.6, 20)
lifetime_list = []
for ZPL in ZPL_list:

    list_phonon_part = calc_phonon_part(
                ZPL,
                0.405588,
                15.44973078041893,
                29.036434368899307,
                [300.4693366708385156],
                0
    )
    lifetime_list.append(calc_lifetime_T(3, 3668, list_phonon_part, 'isc')[0][1])
print("lifetime_list: ", lifetime_list)


# 3E - 1A1
# print("GW BSE")
# list_phonon_part = calc_phonon_part(
#             0.313,
#             1.19486,
#             27.709556721516613,
#             29.036434368899307,
#             [300.4693366708385156],
#             0
#         )
# print("MoVO majority ISC: ", list_phonon_part)
# print("MoVO majority ISC lifetime lambda perp: ", calc_lifetime_T(3, 450, list_phonon_part, 'isc'))
# print("MoVO majority ISC lifetime lambda z: ", calc_lifetime_T(3, 0.015, list_phonon_part, 'isc'))


# 3E - 1A1
# list_phonon_part = calc_phonon_part(
#             0.22,
#             1.19486,
#             27.709556721516613,
#             29.036434368899307,
#             [300.4693366708385156],
#             0
#         )
# print("TDDFT: ")
# print("MoVO majority ISC: ", list_phonon_part)
# print("MoVO majority ISC lifetime lambda perp: ", calc_lifetime_T(3, 450, list_phonon_part, 'isc'))
# print("MoVO majority ISC lifetime lambda z: ", calc_lifetime_T(3, 0.015, list_phonon_part, 'isc'))


# 3E - 1A1
# list_phonon_part = calc_phonon_part(
#             0.256,
#             1.19486,
#             27.709556721516613,
#             29.036434368899307,
#             [300.4693366708385156],
#             0
#         )
# print("New val ZPL 1.411: ")
# print("MoVO majority ISC: ", list_phonon_part)
# print("MoVO majority ISC lifetime lambda perp: ", calc_lifetime_T(3, 450, list_phonon_part, 'isc'))
# print("MoVO majority ISC lifetime lambda z: ", calc_lifetime_T(3, 1E-12, list_phonon_part, 'isc'))

Test different ZPL and plot the lifetime:
ZPL_list = np.linspace(0.22, 0.91, 20)
lifetime_list = []
for ZPL in ZPL_list:

    list_phonon_part = calc_phonon_part(
                ZPL,
                1.19486,
                27.709556721516613,
                29.036434368899307,
                [300.4693366708385156],
                0
            )
    
#     print("MoVO majority ISC: ", list_phonon_part)
#     print("MoVO majority ISC lifetime lambda perp: ", calc_lifetime_T(3, 450, list_phonon_part, 'isc'))
#     print("MoVO majority ISC lifetime lambda z: ", calc_lifetime_T(3, 0.00015, list_phonon_part, 'isc'))

    lifetime_list.append(calc_lifetime_T(3, 450, list_phonon_part, 'isc')[0][1])

print("lifetime_list: ", lifetime_list)]


# Example NV-center

# list_phonon_part = calc_phonon_part(
#             0.5,
#             0.4634318505672413,
#             75.32539159354354,
#             71.13420217890697,
#             [300.0],
#             0
#         )

# print("New val ZPL 1.411: ")
# print("MoVO majority ISC: ", list_phonon_part)
# print("MoVO majority ISC lifetime lambda perp: ", calc_lifetime_T(1, 44.97, list_phonon_part, 'isc'))
# print("MoVO majority ISC lifetime lambda z: ", calc_lifetime_T(1, 1E-12, list_phonon_part, 'isc'))
