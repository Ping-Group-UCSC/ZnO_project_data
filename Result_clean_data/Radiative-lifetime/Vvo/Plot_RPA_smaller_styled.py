 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 19 12:08:54 2022

@author: miaz
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
#___________Data____________________
cwd=os.getcwd()
print(cwd)
File_to_plot_1 = ["o-30Ry_x.eps_q1_diago_bse","o-30Ry_y.eps_q1_diago_bse", "o-30Ry_z.eps_q1_diago_bse"]
File_to_plot_1 = [f"{cwd}/RPA/{f_name}" for f_name in File_to_plot_1]
Label30 = ["x", "y", "z"]
Color = ["C0","C1","C2"]
Datas_30 = [np.loadtxt(f) for f in File_to_plot_1]

#_________Figure Style_______________________
plt.rcParams["figure.titlesize"] = 18
plt.rcParams["lines.linewidth"] = 2
#plt.rcParams["xtick.labelsize"] = 10
#plt.rcParams["ytick.labelsize"] = 10
plt.rcParams["font.size"] = 16
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = "Arial"
plt.rcParams["legend.fontsize"] = 10
plt.rcParams["figure.figsize"] = (4*1.2, 3*1.2)
plt.rcParams["figure.dpi"] = 200


#____________Plot: CBCN monolayer_______________________
fig1,ax1 = plt.subplots(1,1,sharex=True, gridspec_kw={"hspace":0.1})

for i in range(len(Datas_30)):
    data = Datas_30[i]; label = Label30[i]
    ax1.plot(data[:,0], data[:,1], label=label,color=Color[i])
ax1.set_xlim(0,4)
ax1.set_xlabel("Energy (eV)")
ax1.set_ylabel("Im[$\epsilon$]")
#ax.axes.yaxis.set_visible(False)
ax1.set_ylim(0,1)
ax1.legend()
fig1.savefig("V_VO_Spectrum_RPA_lowenergy_styled.pdf",bbox_inches = "tight")

