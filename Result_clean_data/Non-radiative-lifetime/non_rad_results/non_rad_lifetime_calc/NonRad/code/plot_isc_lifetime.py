import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# Open txt file
#file = open("lifetime_data_3E_1A1.txt", "r")
file = open("lifetime_data_1E_3A2.txt", "r")

ZPL_list = []
lifetime_list = []
for line in file.readlines():
    zpl_val = float(line.split(" ")[0])
    ZPL_list.append(zpl_val)
    lifetime_val = float(line.split(" ")[1])
    lifetime_list.append(lifetime_val)
file.close()

def lifetime_func(x, ZPL_list, lifetime_list):
    return np.interp(x, ZPL_list, lifetime_list)

f = lambda x: lifetime_func(x, ZPL_list, lifetime_list) - 0.5
inf_val = fsolve(f, 0.7)[0]

f = lambda x: lifetime_func(x, ZPL_list, lifetime_list) - 10
sup_val = fsolve(f, 0.7)[0]

title_size = 25
tick_size = 20
font_size = 23    
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

ax.plot(ZPL_list, lifetime_list,'-b', linewidth = 1.5)

y1 = 0.5
y2 = 10
ax.plot([ZPL_list[0], ZPL_list[-1]], [0.5, 0.5], '--r', linewidth=1)
ax.plot([ZPL_list[0], ZPL_list[-1]], [10, 10], '--r', linewidth=1)
ax.fill_between(ZPL_list, y1, y2, color='r', alpha=0.2)

ax.plot([inf_val, inf_val],[lifetime_list[0],lifetime_list[-1]], '--r', linewidth=1)
ax.plot([sup_val, sup_val],[lifetime_list[0],lifetime_list[-1]], '--r', linewidth=1)

ax.set_ylabel("ISC lifetime (microsecond)")
ax.set_xlabel("ZPL 1E -> 3A2 in eV")
plt.yscale('log')
plt.show()
