#Plot final PL styled

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal

#_________INPUT data_______
f_up="./PL_spindn_fft/Final_gamma0.005_gamma0.003/pl.dat"
zpl = 1.561445
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
#PL peak: renormalize it
index_peaks, properties = scipy.signal.find_peaks(data[:,1])
#index_peak = np.argmax(data[:,1])
print(index_peaks)
for i in index_peaks:
    print(data[:,0][i])
    if data[:,0][i]<zpl:
        E_peak = data[:,0][i]
        Peak_intensity = data[:,1][i] #the FFT period range is too small so we got 1 at boundary
        #here i need to renormalize the intensty to make the real peak intensity=1
        break
data[:,1] = data[:,1]/Peak_intensity

ax1.plot(data[:,0], data[:,1])
#plot zpl
ax1.axvline(zpl,color='black', linestyle='--', label=f"ZPL={round(zpl,2)} eV")


#E_peak = data[:,0][index_peak]
ax1.axvline(E_peak,color='red', linestyle='--', label=f"PL peak={round(E_peak,2)} eV")

ax1.set_xlim(0.2,1.7)
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
ax2.axvline(zpl,color='black', linestyle='--', label=f"zpl={round(zpl,3)} eV")
ax2.set_xlim(1.50,1.60)
#ax2.set_xlabel("Energy (eV)")
#ax2.set_ylabel("Im[$\epsilon$]")
#ax.axes.yaxis.set_visible(False)
ax2.set_ylim(0,0.03)
#ax2.legend()
fig2.savefig("PL_spindn_final_inset.pdf",bbox_inches = "tight")