# Combined PL plot with inset

import numpy as np
import matplotlib.pyplot as plt

#_________INPUT data_______
f_up = "./PL_spinup_FFT/Final_gamma0.005_smear0.003/pl.dat"
zpl = 2.08 #1.986 # change to 2.08 for DLPNO-NEVPT2@CASSCF(4,7) value

#_________Figure Style_______________________
plt.rcParams["figure.titlesize"] = 18
plt.rcParams["lines.linewidth"] = 1.5
plt.rcParams["font.size"] = 16
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = "Arial"
plt.rcParams["legend.fontsize"] = 16
plt.rcParams["figure.figsize"] = (4*1.6, 3*1.6)
plt.rcParams["figure.dpi"] = 200

def read_dat(f_name):
    data = np.loadtxt(f_name)
    return data

# Read data
data = read_dat(f_up)

# Create main plot with inset
fig, ax1 = plt.subplots()

# Main plot
index_peak = np.argmax(data[:,1])
E_peak = data[:,0][index_peak]
#ax1.axvline(E_peak, color='red', linestyle='--', label=f"pl peak={E_peak} eV")
print(f"pl peak={E_peak} eV")
print(f"zpl shift to : {zpl}")

ax1.plot(data[:,0]-1.986+zpl, data[:,1], label=r"spin-maj ($e$->$2a_1$)")

#ax1.plot([zpl, zpl], [0, 0.2], color='black', linestyle='--', label=f"zpl={zpl} eV")
#ax1.plot([zpl, zpl], [0, 0.1], color='black', linestyle='--', label=f"zpl={zpl} eV")
ax1.set_xlim(1.7, 2.2)
ax1.set_ylim(0, 1.3)
ax1.set_xlabel("Energy (eV)")
ax1.set_ylabel("PL intensity (normalized)")
#ax1.legend()

# Add inset
#inset_ax = fig.add_axes([0.58, 0.55, 0.3, 0.3])  # [x, y, width, height] relative to figure
#inset_ax.plot(data[:,0], data[:,1], label=r"spin-maj ($e$->$2a_1$)")
#inset_ax.axvline(zpl, color='black', linestyle='--', label=f"zpl={zpl} eV")
#inset_ax.plot([zpl, zpl], [0, 0.1], color='black', linestyle='--', label=f"zpl={zpl} eV")
#inset_ax.set_xlim(1.95, 2.0)
#inset_ax.set_ylim(0, 1.0)
# Optional: Customize inset ticks/labels
#inset_ax.tick_params(axis='x', labelsize=10)
#inset_ax.tick_params(axis='y', labelsize=10)

# Save combined figure
fig.savefig("PL_spinup_clean_V2.pdf", bbox_inches="tight")

plt.show()
