import matplotlib.pyplot as plt
import numpy as np

f_up="./PL_spinup_FFT/Final_gamma0.005_smear0.003/S_hw.dat"
f_peak="hw_peak.txt"
def read_dat(f_name):
    data = np.loadtxt(f_name)
    return data


#_________Figure Style_______________________
plt.rcParams["figure.titlesize"] = 18
plt.rcParams["lines.linewidth"] = 1.5
#plt.rcParams["xtick.labelsize"] = 10
#plt.rcParams["ytick.labelsize"] = 10
plt.rcParams["font.size"] = 16
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = "Arial"
plt.rcParams["legend.fontsize"] = 16
plt.rcParams["figure.figsize"] = (1.5*1.6, 3*1.6)
plt.rcParams["figure.dpi"] = 200



fig, ax = plt.subplots(nrows=1, ncols=1,sharey=True)
data = np.loadtxt(f_up)
ax.plot(data[:,0], data[:,1])
ax.set_xlim(0,100)
ax.set_ylabel(r"$S_{\hbar\omega}(1/meV)$")
ax.set_xlabel(r"$\hbar\omega(meV)$")

#plt.title("S_hw")
fig.subplots_adjust(wspace=0)
#plt.legend()
plt.savefig("S_hw_final_styled_spinup_clean.pdf",bbox_inches = "tight")

#Find peak:
import scipy
peaks, properties=scipy.signal.find_peaks(data[:,1])
with open(f_peak,'w') as f:
    f.write("peak, intensity\n")
    for p in peaks:
        print(data[p,0], data[p,1])
        f.write("{}   , {}\n".format(data[p,0], data[p,1]))