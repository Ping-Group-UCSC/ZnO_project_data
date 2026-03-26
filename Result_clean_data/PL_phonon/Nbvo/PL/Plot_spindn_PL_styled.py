#Plot final PL styled

import numpy as np
import matplotlib.pyplot as plt

#_________INPUT data_______
f_up="./PL_spindn_fft/Final_gamma0.005_smear0.003/pl.dat"
zpl = 1.722
#_________Figure Style_______________________
plt.rcParams["figure.titlesize"] = 18
plt.rcParams["lines.linewidth"] = 2
#plt.rcParams["xtick.labelsize"] = 10
#plt.rcParams["ytick.labelsize"] = 10
plt.rcParams["font.size"] = 16
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = "Arial"
plt.rcParams["legend.fontsize"] = 14
plt.rcParams["figure.figsize"] = (4*1.2, 3*1.2)
plt.rcParams["figure.dpi"] = 200

def read_dat(f_name):
    data = np.loadtxt(f_name)
    return data
    
#____________Plot: PL_______________________
fig1,ax1 = plt.subplots(1,1,sharex=True, gridspec_kw={"hspace":0.1})
data = read_dat(f_up)
ax1.plot(data[:,0], data[:,1])
#plot zpl
ax1.axvline(zpl,color='black', linestyle='--', label=f"ZPL={round(zpl,2)} eV")
#PL peak
index_peak = np.argmax(data[:,1])
E_peak = data[:,0][index_peak]
ax1.axvline(E_peak,color='red', linestyle='--', label=f"PL peak={round(E_peak,2)} eV")

ax1.set_xlim(0.3,2.3)
ax1.set_xlabel("Energy (eV)")
ax1.set_ylabel("Im[$\epsilon$]")
#ax.axes.yaxis.set_visible(False)
ax1.set_ylim(0,1.1)
ax1.legend(loc="upper right")
fig1.savefig("PL_spindn_final.pdf",bbox_inches = "tight")

#Plot PL inset
plt.rcParams["figure.figsize"] = (4*1.2/1.3, 3*1.2/1.3)
plt.rcParams["figure.dpi"] = 100
fig2, ax2 = plt.subplots(1,1,sharex=True, gridspec_kw={"hspace":0.1})
data = read_dat(f_up)
ax2.plot(data[:,0], data[:,1])
#ZPL
ax2.axvline(zpl,color='black', linestyle='--', label=f"ZPL={round(zpl,2)} eV")
ax2.set_xlim(1.68,1.75)
#ax2.set_xlabel("Energy (eV)")
#ax2.set_ylabel("Im[$\epsilon$]")
#ax.axes.yaxis.set_visible(False)
ax2.set_ylim(0,0.025)
#ax2.legend()
fig2.savefig("PL_spindn_final_inset.pdf",bbox_inches = "tight")