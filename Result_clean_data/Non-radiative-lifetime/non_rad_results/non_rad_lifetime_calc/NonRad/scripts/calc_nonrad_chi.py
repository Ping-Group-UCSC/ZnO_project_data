#!/usr/bin/env python3
import numpy as np
import sys

if len(sys.argv) < 2:
    print("Usage: python calc_nonrad_chi.py <your_input>")
    sys.exit(1)

chi_atomic_unit = float(sys.argv[1])

hbar = 6.582119569e-16 # unit: eV*s
AMU2me = 1822.89 # atomic mass unit to mass of electron
bohr2ang = 0.529177 # bohr to angstrom
Ha2eV = 27.2 # Ha to eV
eV2GHz = 241.79893e3 # eV to GHz

def tau(g, wif_square, xif):
    # calculate nonradiative lifetime in the unit of ps
    rate = 2 * np.pi / hbar * g * wif_square * xif
    lifetime = 1.0 / rate * 10**12
    return lifetime

def gamma_isc(g, _lambda, xif):
    # calculate ISC rate in the unit of MHz
    _lambda /= eV2GHz
    rate = 2 * np.pi / hbar * g * _lambda**2 * xif * 1e-6
    return rate

g = 1 # degeneracy

wif_square = np.array([0.05]) # in the unit of eV^2/amu/A^2

xif = np.array([chi_atomic_unit]) # in the unit of me*Bohr^2/Ha

lifetime1 = tau(g, wif_square, xif)
print("lifetime before unit conversion:", lifetime1, "ps")

x_if = xif / AMU2me * bohr2ang**2 / Ha2eV # in the unit of amu*A^2/eV
print("Xif:", chi_atomic_unit, "m_e*Bohr^2/Ha")
print("Xif:", x_if, "amu*A^2/eV")
lifetime2 = tau(g, wif_square, x_if)
print("lifetime after unit conversion:", lifetime2, "ps")

x_bar_if = xif / Ha2eV # in the unit of 1/eV
_lambda = 9.62 # GHz
rate = gamma_isc(g, _lambda, x_bar_if)
print("X_bar_if:", chi_atomic_unit, "1/Ha")
print("X_bar_if:", x_bar_if, "1/eV")
print("ISC rate after unit conversion:", rate, "MHz")
