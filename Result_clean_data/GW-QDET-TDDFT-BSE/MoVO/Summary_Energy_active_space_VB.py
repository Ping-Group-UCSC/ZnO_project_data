import matplotlib.pyplot as plt

plt.rcParams["lines.linewidth"] = 2
plt.rcParams["xtick.labelsize"] = 15
plt.rcParams["ytick.labelsize"] = 15
plt.rcParams["font.size"] = 15
#plt.rcParams["font.family"] = "sans-serif"
#plt.rcParams["font.sans-serif"] = "Arial"
plt.rcParams["axes.titlesize"] = 15
#plt.rcParams["legend.fontsize"] = 16
#plt.rcParams["figure.figsize"] = (12,5.5)
plt.rcParams["figure.figsize"] = (5.5,3)
plt.rcParams["figure.dpi"] = 150

# Data
#x_labels = [ "(4e,4o)", "(4e,7o)", "(4e,9o)","(8e,11o)","(14e,14o)"]
x_labels = ["(4e,9o)","(8e,11o)","(14e,14o)"]
x = list(range(len(x_labels)))
#y1 = [0.0, 0.0,0,0,0.0]     # 3A2
y1 = [0.0,0.0,0.0]
y2 = [1.6, 1.9,2.06]
#y2 = [0.22, 1.37, 1.6, 1.9,2.06] # ^4E

# Plot
fig, ax = plt.subplots()

ax.plot(x, y1, 'o-', color='blue', label=r"$^3E$")
ax.plot(x, y2, 'v-', color='red', label=r"$^3A_2$")

# Annotate near the leftmost point
#ax.text(x[0]-0.3, y1[0]+0.02, r"$^6A_1$", color="blue", fontsize=12)
#ax.text(x[0]-0.3, y2[0]+0.02, r"$^4E$", color="red", fontsize=12)

# Axis formatting
ax.set_xticks(x)
ax.set_xticklabels(x_labels)
ax.set_xlabel("Active Space")
ax.set_ylabel("Excitation Energy (eV)")
ax.set_ylim(-0.5, 3)
#ax.spines['top'].set_visible(False)
#ax.spines['right'].set_visible(False)
plt.legend()
plt.tight_layout()
plt.savefig("excitation_energy_vs_active_space_addVB.png")
plt.show()

