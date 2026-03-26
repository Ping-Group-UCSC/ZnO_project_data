#!/usr/bin/env python3

#charge transition level data: 
ctl_data = {
    "movo": {
        "name": r"$\mathrm{Mo}_{\mathrm{Zn}}\mathrm{v}_\mathrm{O}$",
        "ctl_labels": ["4+/3+" "3+/2+", "2+/1+", "1+/0"],
        "ctl_energies": [0.929, 1.7014, 2.8072, 3.3731]
    },
    "nbvo": {
        "name": r"$\mathrm{Nb}_{\mathrm{Zn}}\mathrm{v}_\mathrm{O}$",
        "ctl_labels": ["5+/3+", "3+/2+", "2+/1+", "1+/0"],
        "ctl_energies": [1.798824, 2.162193, 2.665298, 3.35097]
    },
    "tivo": {
        "name": r"$\mathrm{Ti}_{\mathrm{Zn}}\mathrm{v}_\mathrm{O}$",
        "ctl_labels": ["4+/2+", "2+/1+"],
        "ctl_energies": [2.0485625, 2.237205]
    },
    "vvo": {
        "name": r"$\mathrm{V}_{\mathrm{Zn}}\mathrm{v}_\mathrm{O}$",
        "ctl_labels": ["4+/3+", "3+/1+", "1+/0"],
        "ctl_energies": [1.58810548, 1.79693957, 3.4265]
    },
    "vo": {
        "name": r"$\mathrm{v}_\mathrm{O}$",
        "ctl_labels": ["2+/0"],
        "ctl_energies": [2.2648]
    },
    "vzn": {
        "name": r"$\mathrm{v}_\mathrm{Zn}$",
        "ctl_labels": ["2+/1+", "1+/0", "0/1-", "1-/2-"],
        "ctl_energies": [0.6364, 1.0598, 1.4634, 1.796]
    }
}

n_defects = len(ctl_data) #number of defects
w = 0.2 #width of the CTL
#______________PLOT_____________________
import matplotlib.pyplot as plt
plt.rcParams["figure.titlesize"] = 16
plt.rcParams["lines.linewidth"] = 1.5
plt.rcParams["xtick.labelsize"] = 18
plt.rcParams["ytick.labelsize"] = 18
plt.rcParams["font.size"] = 18
plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.sans-serif"] = "Arial"
plt.rcParams["legend.fontsize"] = 16
plt.rcParams["figure.figsize"] = (8, 4)
plt.rcParams["figure.dpi"] = 100

fig, ax = plt.subplots(nrows=1, ncols=1,sharey=True)



x = 0 #count
my_x_ticks = [] # tick locations
my_x_labels = [] # tick labels
for defect in ctl_data.keys():
    print("plot:",defect)
    ctl_list = ctl_data[defect]["ctl_energies"] 
    for ctl in ctl_list:
        ax.plot([x-w, x+w],[ctl,ctl], color = "black")
    my_x_ticks.append(x)
    my_x_labels.append(ctl_data[defect]["name"])
    x += 1
 
# x-axis ticks and labels
ax.set_xticks(my_x_ticks)  #  tick locations
ax.set_xticklabels(my_x_labels)  #  tick labels
ax.tick_params(axis='x', which='both', bottom=False, top=False)  # removes tick marks
# y-axis ticks
#ax.set_yticks([0.0, 1.0, 2.0, 2.8, 3.4])
#axis:
ax.set_xlim(0-0.5,(n_defects-1)+0.5)
ax.set_ylim(-0.5,4)
#fill VBM and CBM
top = 7.0
gap = 3.4281
bottom = gap - top+2
ax.fill_between(
    ax.get_xlim(), 
    [bottom, bottom], [0, 0], 
    color="forestgreen",#, alpha=0.9,
    edgecolor="none"
)
ax.fill_between(
    ax.get_xlim(), 
    [gap, gap], [top, top], 
    color="grey", alpha=0.6,
    edgecolor="none"
)




#labels
ax.set_ylabel("Fermi energy (eV)", labelpad=4) # increase distance (default is ~4)

plt.tight_layout()  # adjust spacing to fit all elements
fig.savefig("charge_transition_level.png", bbox_inches='tight')
