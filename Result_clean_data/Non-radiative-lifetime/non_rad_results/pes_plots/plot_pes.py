import numpy as np
from numpy import sqrt, exp, pi, cos, sin
from math import pi
import math

import matplotlib.pyplot as plt
import os

from scipy import constants
from numpy import linalg as LA
from scipy import interpolate

AMU2kg = 1.66053904E-27
Ang2m = 1e-10
h_Js = 6.626070040e-34
hbar_Js = h_Js / 2 / pi
J2eV = 6.242e+21 #meV
eV2GHz = 241.79893e3 # eV to GHz

def omega_effective(Q_vec, E_vec):
    ''' We fit the model E(Q) = 1/2 * omega_eff^2 * Q^2  '''

    # Fit a 2nd order polynomial
    coefficients = np.polyfit(Q_vec, E_vec, 2)
    omega = sqrt(2 * coefficients[0])
    beta = coefficients[0]*0
    return omega, beta

def omega_effective2(h, k, x0, y0):
    coeff = (y0 - k)/(x0 - h)**2
    print(coeff)
    return sqrt(2 * coeff)

def Sk(wk, qk):
    """
    calc sk = wk*qk^2/(2*hbar)
    sk is unitless: [wk] = Hz, [qk] = kg^(1/2)*m, [hbar] = J*s
    returns array of sk's
    """
    sk = wk * qk ** 2 / (2 * hbar_Js)
    return sk


def plot_potential_energy_surface(gs_data, es_data, gs_curve, es_curve, dQ, minmax_x, minmax_y, defect_name, plot_name):
    
    title_size = 20
    tick_size = 20
    font_size = 20

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
    
    ax.plot(gs_curve[0], gs_curve[1], color='red', linewidth = 1)
    ax.plot(es_curve[0], es_curve[1], color='blue', linewidth = 1)
    ax.scatter(gs_data[0], gs_data[1], marker='o', facecolors='white', edgecolor='red', s = 50.0, zorder=3)
    ax.scatter(es_data[0], es_data[1], marker='o', facecolors='white', edgecolor='blue', s = 50.0, zorder=3)

    ax.plot([minmax_x[0], minmax_x[1]], [0,0], '-k', linewidth = 0.8)
    ax.plot([0,0], [minmax_y[0], minmax_y[1]], '-k', linewidth = 0.8)

     # Draw a dashed arrow
    ax.annotate('', xy=(dQ, min(es_data[1])), xytext=(0, 0),
            arrowprops=dict(arrowstyle='<->', linestyle=(5, (10, 3)), linewidth=0.8, color='k',
                            mutation_scale=20))

    if defect_name == "Mo maj Main":
        # Plot ZPL label
        ax.text(-3.5, 1, f"ZPL = {min(es_data[1]).round(2)} eV", fontsize = font_size, color = 'k')
    else:
        # Plot ZPL label
        ax.text(max(gs_data[0])/5 - 0.1, min(es_data[1])/5, f"ZPL = {min(es_data[1]).round(2)} eV", fontsize = font_size,
            color = 'k', rotation = np.arctan(min(es_data[1])/max(gs_data[0]))*180/np.pi, rotation_mode='anchor',
           transform_rotates_text=True)
    
    # Plot Transition labels
    if defect_name == "Nb min":
        ax.text(6.2, 1.2, "$\mathrm{^3A_2}$", verticalalignment='center', 
                horizontalalignment = 'center', fontsize = font_size, color='red')
        ax.text(-1.5, 2.5, "$\mathrm{^3A_2^'}$", verticalalignment='center', 
                horizontalalignment = 'center', fontsize = font_size, color='blue')
    elif defect_name == "Nb maj":
        ax.text(2.6, 0.8, "$\mathrm{^3A_2}$", verticalalignment='center', 
                horizontalalignment = 'center', fontsize = font_size, color='red')
        ax.text(-0.8, 1.75, "$\mathrm{^3E}$", verticalalignment='center', 
                horizontalalignment = 'center', fontsize = font_size, color='blue')

    elif defect_name == "Mo maj" or defect_name == "Mo maj Main":
        ax.text(3.6, 0.7, "$\mathrm{^3A_2}$", verticalalignment='center', 
                horizontalalignment = 'center', fontsize = font_size, color='red')
        ax.text(-0.8, 2.0, "$\mathrm{^3E}$", verticalalignment='center', 
                horizontalalignment = 'center', fontsize = font_size, color='blue')

    # Plot Higher PES name
    elif defect_name == "Mo min":
        ax.text(7.3, 1, "$\mathrm{^3A_2}$", verticalalignment='center', 
                horizontalalignment = 'center', fontsize = font_size, color='red')
        ax.text(-1.4, 2.5, "$\mathrm{^3A_2^'}$", verticalalignment='center', 
                horizontalalignment = 'center', fontsize = font_size, color='blue')


    ax.set_xlabel("Q ($\mathrm{amu}^{1/2}$ $\mathrm{\AA}$)")
    ax.set_ylabel("Energy (eV)")
    ax.set_xlim(minmax_x)
    ax.set_ylim(minmax_y)
    plt.savefig(plot_name+".png", bbox_inches='tight')
    plt.show()


def generate_report(gsPES, esPES, dQ, minmax_x, minmax_y, defect_name, plot_name):
        
    minEs = min(esPES[:,1])
    minGs = min(gsPES[:,1])
    
    ZPL = minEs - minGs
    
    omega_gs,beta_gs = omega_effective(gsPES.T[0], gsPES.T[1])
    omega_es,beta_es = omega_effective(esPES.T[0], esPES.T[1])

    q_coords = np.linspace(minmax_x[0], minmax_x[1], 50)
    gs_curve = 1/2 * omega_gs**2 * q_coords**2 + beta_gs * q_coords**3
    es_curve = 1/2 * omega_es**2 * (q_coords-dQ)**2 + beta_es * (q_coords-dQ)**3 + ZPL
    
    num_phonons = ZPL / (omega_es * 9.82269475 * 10**13 * hbar_Js * J2eV * 1e-3)
    
    print("##################")
    print(f"PES Data for {defect_name}")
    print("##################")

    print(f"dQ: {dQ} Ang.amu^1/2")
    print(f"ZPL: {ZPL} eV")
    
    print("gs curve: ")
    print(f"omega_eff: {omega_gs * 9.82269475 * 10**13 * hbar_Js * J2eV} meV" ) # Convert to Hz and then to meV ) 
    print("Huang-Rhys: ", Sk(omega_gs * 9.82269475 * 10**13, dQ * sqrt(AMU2kg) * Ang2m))
    print(" ")
    print("es curve: ")
    print(f"omega_eff: {omega_es * 9.82269475 * 10**13 * hbar_Js * J2eV} meV" ) # Convert to Hz and then to meV ) 
    print("Huang-Rhys: ", Sk(omega_es * 9.82269475 * 10**13, dQ * sqrt(AMU2kg) * Ang2m))
    
    print("Number of phonons: ", int(num_phonons))
    print("")
    print("")
    
    plot_potential_energy_surface(gsPES.T, esPES.T,[q_coords, gs_curve], [q_coords, es_curve],
                                  dQ, minmax_x, minmax_y, defect_name, plot_name)


# NbVO+ Minority Spin:

gsPES = np.genfromtxt("Nb/minority_spin/gsPES.txt", delimiter=' ',dtype=float)
esPES = np.genfromtxt("Nb/minority_spin/esPES.txt", delimiter=' ',dtype=float)
dQ = 3.83629
plot_name = "PES_nb_min"
defect_name = "Nb min"

generate_report(gsPES, esPES, dQ, [-5.5 , 8.5], [-0.2, 3.5], defect_name, plot_name)


# NbVO+ Majority Spin:

gsPES = np.genfromtxt("Nb/majority_spin/gsPES.txt", delimiter=' ',dtype=float)
esPES = np.genfromtxt("Nb/majority_spin/esPES.txt", delimiter=' ',dtype=float)
dQ = 1.80
plot_name = "PES_nb_maj"
defect_name = "Nb maj"

generate_report(gsPES, esPES, dQ, [-2 , 3.5], [-0.2, 2.5], defect_name, plot_name)


# MoVO Minority Spin:

gsPES = np.genfromtxt("Mo/minority_spin/gsPES.txt", delimiter=' ',dtype=float)
esPES = np.genfromtxt("Mo/minority_spin/esPES.txt", delimiter=' ',dtype=float)
dQ = 5.04901
plot_name = "PES_mo_min"
defect_name = "Mo min"

generate_report(gsPES, esPES, dQ, [-6.5, 10], [-0.2, 3.5], defect_name, plot_name)


# MoVO Majority Spin:

gsPES = np.genfromtxt("Mo/majority_spin/gsPES.txt", delimiter=' ',dtype=float)
esPES = np.genfromtxt("Mo/majority_spin/esPES.txt", delimiter=' ',dtype=float)
dQ = 1.19486
plot_name = "PES_mo_maj"
defect_name = "Mo maj"

generate_report(gsPES, esPES, dQ, [-2, 5.5], [-0.2, 3.7], defect_name, plot_name)





