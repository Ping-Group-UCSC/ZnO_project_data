import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import argparse
import re
from scipy import interpolate


def read_defect_excel(relative_dir):
    cwd = os.getcwd()
    excel_name = relative_dir.split("/")[-1]
    name = excel_name.split(".")[0]
    file_path = os.path.join(cwd, relative_dir) # create excel file path

    data_poor = pd.read_excel(file_path, sheet_name="poor") #, header = [0,1]) # extract data in dataframe
    data_rich = pd.read_excel(file_path, sheet_name="rich")
    # data_partial = pd.read_excel(file_path, sheet_name="partial")

    headers = data_poor.keys().to_list()
    headers[0] = "q"

    data_poor.rename(columns=dict(zip(data_poor.keys().to_list(), headers)), inplace=True)
    data_rich.rename(columns=dict(zip(data_rich.keys().to_list(), headers)), inplace=True)

    return {"poor":data_poor, "rich":data_rich}, name


def charge_transition_levels(charges_values, defect_values, bandgap):
    '''
    Calculate the CTLs for the defect formation energies 
    '''
    transition_levels = []
    q_values = []

    q1 = charges_values[0] #2
    while q1 > charges_values[-1]: #-2

        i = list(charges_values).index(q1)

        transition_levels_q1 = []
        q1pairs = []
        for q2 in charges_values[i+1:]:

            shft1 = defect_values[i]
            j = list(charges_values).index(q2)
            shft2 = defect_values[j]
            
            transition_level = (shft2 - shft1) / (q1 - q2)
            transition_levels_q1.append(transition_level)
            q1pairs.append([q1,q2])
        
        first_transition_level = min(transition_levels_q1)
        position = transition_levels_q1.index(first_transition_level)
        new_charge = charges_values[i+1:][position]
        
        transition_levels.append(first_transition_level)
        q_values.append(q1pairs[position])
    
        q1 = new_charge

    transition_levels.insert(0,0)
    transition_levels.append(bandgap)

    return transition_levels, q_values

def get_intervals(all_intervals, q_values1, bandgap):

    # Filter the transition level values that lie in the bandgap:

    bool_map = (np.array(all_intervals) >= 0) & (np.array(all_intervals) <= bandgap)
    intervals = np.array(all_intervals)[bool_map]

    q_values = np.array(q_values1)[bool_map[1:-1]].flatten()
    q_values_unique = []
    [q_values_unique.append(item) for item in q_values if item not in q_values_unique];

    interval_pairs = np.transpose([intervals[:-1], intervals[1:]])
    fermi_energies = np.linspace(0, bandgap, 4)

    return q_values_unique, intervals, interval_pairs, fermi_energies


def plot_defects_and_intrinsic(data_dictionary, bandgap):

    chem_conditions = list(data_dictionary.keys())
    num_plots = len(chem_conditions)

    title_size = 24
    tick_size = title_size
    font_size = title_size

    plt.rcParams["figure.titlesize"] = title_size
    plt.rcParams["lines.linewidth"] = 1.7
    plt.rcParams["xtick.labelsize"] = tick_size
    plt.rcParams["ytick.labelsize"] = tick_size
    plt.rcParams["font.size"] = font_size
    plt.rcParams["legend.fontsize"] = tick_size

    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = "Arial"
    plt.rcParams["figure.figsize"] = (6*num_plots,8)
    plt.rcParams["figure.dpi"] = 100
    plt.rcParams['mathtext.fontset'] = 'custom'
    plt.rcParams['mathtext.rm'] = 'Bitstream Vera Sans'
    
    ##################################

    fig, ax = plt.subplots(nrows=1, ncols=num_plots)

    colors = ["k", "b", "r"]
    intersects = []
    posy = dict(zip(chem_conditions, np.zeros(len(chem_conditions))))
    for idx, condition in enumerate(chem_conditions):
                
        defects_list = ["Nb","[V]","Ti", "Mo"]
        defects_colors = ['r','g','chocolate',"b"]
        for j, defect_name in enumerate(defects_list):
            
            # Complex vacancy data
            intervals_3 = data_dictionary[condition]['defects'][defect_name+"VO"]['intervals']
            interval_pairs_3 = data_dictionary[condition]['defects'][defect_name+"VO"]['interval_pairs']
            defect_values_3 = np.array(data_dictionary[condition]['defects'][defect_name+"VO"]['defect_values'])
            q_values_3 = np.array(data_dictionary[condition]['defects'][defect_name+"VO"]['q_values_unique'])
            formation_intervals_3 = interval_pairs_3 * q_values_3[:, np.newaxis] + defect_values_3[:, np.newaxis]
            formation_3 = np.append(formation_intervals_3[:,0], formation_intervals_3[-1,-1])
            
            finterp = interpolate.interp1d(intervals_3, formation_3)

            # Plot XznVo
            ax[idx].plot(intervals_3, formation_3, c=defects_colors[j])
            ax[idx].scatter(intervals_3[1:-1], formation_3[1:-1], c=defects_colors[j], s = 15)

            if defect_name == "Nb": 
                if condition == 'poor':
                    posx = 0.9
                    posy = finterp(posx) - 1.2
                elif condition == 'rich': 
                    posx = 1.1
                    posy = finterp(posx) + 4.6
            elif defect_name == "Ti":
                if condition == 'poor':
                    posx = 1.4
                    posy = finterp(posx) - 1
                elif condition == 'rich':
                    posx = 1.7
                    posy = finterp(1.4) + 0.5
                
            elif defect_name == "[V]":
                defect_name = "V"
                
                if condition == 'poor':
                    posx = 0.8
                    posy = finterp(posx) + 3.5
                elif condition == 'rich':
                    posx = 2.6
                    posy = finterp(posx) - 0.8

            elif defect_name == "Mo":
                
                if condition == 'poor':
                    posx = 2.1
                    posy = finterp(posx) - 0.8
                elif condition == 'rich':
                    posx = 0.55
                    posy = finterp(posx) + 3.2
    
            ax[idx].text(posx, posy,
                         f"{defect_name}"+"$\mathrm{_{Zn}}$"+"$\mathrm{v_O}$", fontsize=font_size, c=defects_colors[j])   

        # Oxygen vacancy data
        intervals_2  = data_dictionary[condition]['defects']["Vo"]['intervals']
        interval_pairs_2 = data_dictionary[condition]['defects']["Vo"]['interval_pairs']
        defect_values_2 = np.array(data_dictionary[condition]['defects']["Vo"]['defect_values'])
        q_values_2 = np.array(data_dictionary[condition]['defects']["Vo"]['q_values_unique'])
        formation_intervals_2 = interval_pairs_2 * q_values_2[:, np.newaxis] + defect_values_2[:, np.newaxis]
        formation_2 = np.append(formation_intervals_2[:,0], formation_intervals_2[-1,-1])
        formation_interp_2 = interpolate.interp1d(intervals_2, formation_2)
        
        # Zinc vacancy data
        intervals_4  = data_dictionary[condition]['defects']["Vzn"]['intervals']
        interval_pairs_4 = data_dictionary[condition]['defects']["Vzn"]['interval_pairs']
        defect_values_4 = np.array(data_dictionary[condition]['defects']["Vzn"]['defect_values'])
        q_values_4 = np.array(data_dictionary[condition]['defects']["Vzn"]['q_values_unique'])
        formation_intervals_4 = interval_pairs_4 * q_values_4[:, np.newaxis] + defect_values_4[:, np.newaxis]
        formation_4 = np.append(formation_intervals_4[:,0], formation_intervals_4[-1,-1])
        
        # Plot Vzn:
        vacancy_color = 'grey'
        ax[idx].plot(intervals_4, formation_4, c=vacancy_color, label = "$\mathrm{v_{Zn}}$")
        ax[idx].scatter(intervals_4[1:-1], formation_4[1:-1],s = 15, c=vacancy_color)
        ax[idx].text(intervals_4[0]+0.15, formation_4[0]+1.4, "$\mathrm{v_{Zn}}$", fontsize=font_size, c=vacancy_color)

        # Plot Vo:
        ax[idx].plot(intervals_2, formation_2, c=vacancy_color, label = "$\mathrm{v_O}$")
        ax[idx].scatter(intervals_2[1:-1], formation_2[1:-1],s = 15, c=vacancy_color)
        if condition == "rich":
            ax[idx].text(intervals_2[1]+0.6, formation_2[1]-0.9, "$\mathrm{v_O}$", fontsize=font_size, c=vacancy_color)
        else:
            ax[idx].text(intervals_2[0]+0.15, formation_2[0]+1.2, "$\mathrm{v_O}$", fontsize=font_size, c=vacancy_color)



        ax[idx].text(0.1, 10, f"O-{condition}")
        
        if idx == 0:
            ax[idx].set_ylabel("Formation Energy (eV)")

        ax[idx].set_xlabel("Fermi energy (eV)")
        ax[idx].set_xticks([0,1,2,3,4])
        ax[idx].set_yticks([-6,-4,-2,0,2,4,6,8,10])
        
        ax[idx].set_xlim([0, bandgap])
        ax[idx].set_ylim([-7,11]) #ylim_min, ylim_max])
        
        plt.savefig("formation_energies.png",bbox_inches='tight')

# Read formation energies file, store in dictionary and plot:

bandgap = 3.4281
defect_file_dir = "./formation_energies.xlsx"
data, name = read_defect_excel(defect_file_dir)

data_dictionary={}
data_dictionary = {condition: {"data" : data[condition], "defects" : {}} for condition in data.keys()}
for condition in data.keys():
    data_temp = data_dictionary[condition]["data"]
    all_charges = data_temp["q"].values


    for defect_name in data_temp.keys()[1:]:
        all_defect_values = data_temp[defect_name].values
        index_interesections = np.where(~np.isnan(all_defect_values))[0]
        defect_values = all_defect_values[~np.isnan(all_defect_values)][::-1]

        charges = all_charges[~np.isnan(all_defect_values)][::-1]


        all_intervals, q_values = charge_transition_levels(charges, defect_values, bandgap)
        q_values_unique, intervals, interval_pairs, fermi_energies = get_intervals(all_intervals, q_values, bandgap)
        if defect_name == "HO" or defect_name == "Hi":
            q_values_unique = [1]


        positions = [list(charges).index(elem) for elem in q_values_unique]

        data_dictionary[condition]["defects"][defect_name] = {}
        data_dictionary[condition]["defects"][defect_name]["defect_values"] = defect_values[positions]
        data_dictionary[condition]["defects"][defect_name]["all_intervals"] = all_intervals
        data_dictionary[condition]["defects"][defect_name]["q_values"] = q_values
        data_dictionary[condition]["defects"][defect_name]["q_values_unique"] = q_values_unique
        data_dictionary[condition]["defects"][defect_name]["interval_pairs"] = interval_pairs
        data_dictionary[condition]["defects"][defect_name]["intervals"] = intervals
        data_dictionary[condition]["defects"][defect_name]["fermi_energies"] = fermi_energies


plot_defects_and_intrinsic(data_dictionary, bandgap)


# Plot Sum of Single substitution + Vacancy and Complex:

def plot_defect_sum(defect_name):  

    chem_conditions = list(data_dictionary.keys())
    num_plots = len(chem_conditions)

    title_size = 21
    tick_size = title_size
    font_size = title_size

    plt.rcParams["figure.titlesize"] = title_size
    plt.rcParams["lines.linewidth"] = 1.7
    plt.rcParams["xtick.labelsize"] = tick_size
    plt.rcParams["ytick.labelsize"] = tick_size
    plt.rcParams["font.size"] = font_size
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = "Arial"
    plt.rcParams["legend.fontsize"] = tick_size
    plt.rcParams["figure.figsize"] = (6*num_plots,8)
    plt.rcParams["figure.dpi"] = 100

    plt.rcParams['mathtext.fontset'] = 'custom'
    plt.rcParams['mathtext.rm'] = 'Bitstream Vera Sans'
    
    ##################################

    fig, ax = plt.subplots(nrows=1, ncols=num_plots)

    colors = ["k", "b", "r"]
    intersects = []

    for idx, condition in enumerate(chem_conditions):
    
        # Single dopant data
        intervals_1 = data_dictionary[condition]['defects'][defect_name]['intervals']
        interval_pairs_1 = data_dictionary[condition]['defects'][defect_name]['interval_pairs']
        defect_values_1 = np.array(data_dictionary[condition]['defects'][defect_name]['defect_values'])
        q_values_1 = np.array(data_dictionary[condition]['defects'][defect_name]['q_values_unique'])
        formation_intervals_1 = interval_pairs_1 * q_values_1[:, np.newaxis] + defect_values_1[:, np.newaxis]
        formation_1 = np.append(formation_intervals_1[:,0], formation_intervals_1[-1,-1])
        formation_interp_1 = interpolate.interp1d(intervals_1, formation_1)
        
        # Oxygen vacancy data
        intervals_2  = data_dictionary[condition]['defects']["Vo"]['intervals']
        interval_pairs_2 = data_dictionary[condition]['defects']["Vo"]['interval_pairs']
        defect_values_2 = np.array(data_dictionary[condition]['defects']["Vo"]['defect_values'])
        q_values_2 = np.array(data_dictionary[condition]['defects']["Vo"]['q_values_unique'])
        formation_intervals_2 = interval_pairs_2 * q_values_2[:, np.newaxis] + defect_values_2[:, np.newaxis]
        formation_2 = np.append(formation_intervals_2[:,0], formation_intervals_2[-1,-1])
        formation_interp_2 = interpolate.interp1d(intervals_2, formation_2)

        combined_intervals = np.union1d(intervals_1, intervals_2)
        
        # Complex vacancy data
        intervals_3 = data_dictionary[condition]['defects'][defect_name+"VO"]['intervals']
        interval_pairs_3 = data_dictionary[condition]['defects'][defect_name+"VO"]['interval_pairs']
        defect_values_3 = np.array(data_dictionary[condition]['defects'][defect_name+"VO"]['defect_values'])
        q_values_3 = np.array(data_dictionary[condition]['defects'][defect_name+"VO"]['q_values_unique'])
        formation_intervals_3 = interval_pairs_3 * q_values_3[:, np.newaxis] + defect_values_3[:, np.newaxis]
        formation_3 = np.append(formation_intervals_3[:,0], formation_intervals_3[-1,-1])
        formation_interp_3 = interpolate.interp1d(intervals_3, formation_3)
        
        # Zinc vacancy data
        intervals_4  = data_dictionary[condition]['defects']["Vzn"]['intervals']
        interval_pairs_4 = data_dictionary[condition]['defects']["Vzn"]['interval_pairs']
        defect_values_4 = np.array(data_dictionary[condition]['defects']["Vzn"]['defect_values'])
        q_values_4 = np.array(data_dictionary[condition]['defects']["Vzn"]['q_values_unique'])
        formation_intervals_4 = interval_pairs_4 * q_values_4[:, np.newaxis] + defect_values_4[:, np.newaxis]
        formation_4 = np.append(formation_intervals_4[:,0], formation_intervals_4[-1,-1])
    
        # Plot Vzn:
        ax[idx].plot(intervals_4, formation_4, c='k', label = "$\mathrm{v_{Zn}}$")
        ax[idx].scatter(intervals_4[1:-1], formation_4[1:-1], c='k', s = 15)
        ax[idx].text(intervals_4[0]+0.15, formation_4[0]+1.4, "$\mathrm{v_{Zn}}$", fontsize=font_size, c='k')

        # Plot Vo:
        ax[idx].plot(intervals_2, formation_2, c='k', label = "$\mathrm{v_O}$")
        ax[idx].scatter(intervals_2[1:-1], formation_2[1:-1], c='k', s = 15)
        ax[idx].text(intervals_2[0]+0.15, formation_2[0]+1.2, "$\mathrm{v_O}$", fontsize=font_size, c='k')
        ax[idx].plot(intervals_3, formation_3, c='g')
        ax[idx].scatter(intervals_3[1:-1], formation_3[1:-1], c='g', s = 15)
        
        # Plot Xzn
        ax[idx].plot(intervals_1, formation_1, 'g', alpha = 0.3)
        ax[idx].scatter(intervals_1, formation_1, c='g', s = 15, alpha = 0.3)
        
        if idx == 0:
            fermi_energies = combined_intervals
            complexFE = formation_interp_3(combined_intervals)
            sumFE = formation_interp_2(combined_intervals) + formation_interp_1(combined_intervals)
            
        ax[idx].plot(combined_intervals, 
                     formation_interp_2(combined_intervals) + formation_interp_1(combined_intervals),
                     '--', c='g')

        if defect_name == "Nb": 
            if condition == 'poor':

                posx = 2.
                posy = 3
                ax[idx].text(posx, posy, f"{defect_name}"+"$\mathrm{_{Zn}}$"+"$\mathrm{v_O}$", fontsize=font_size, c='g')

                posx = 1.7
                posy = -5.
                ax[idx].text(posx, posy, f"{defect_name}"+"$\mathrm{_{Zn}}$" + "+" + "$\mathrm{v_O}$", fontsize=font_size, c='g')

                posx = 2.7
                posy = -1.5
                ax[idx].text(posx, posy, f"{defect_name}"+"$\mathrm{_{Zn}}$", fontsize=font_size, c='g',  alpha = 0.3)                
                
            elif condition == 'rich': 
                posx = 1.1
                posy = 1

        elif defect_name == "Ti":
            if condition == 'poor':
                posx = 1.4
                posy = finterp(posx) - 1
            elif condition == 'rich':
                posx = 1.7
                posy = finterp(1.4) + 0.5

        elif defect_name == "[V]":
            
            if condition == 'poor':
                posx = 1.5
                posy = 2.8
                ax[idx].text(posx, posy, "V"+"$\mathrm{_{Zn}}$"+"$\mathrm{v_O}$", fontsize=font_size, c='g')

                posx = 1.2
                posy = -5.
                ax[idx].text(posx, posy, "V"+"$\mathrm{_{Zn}}$" + "+" + "$\mathrm{v_O}$", fontsize=font_size, c='g')

                posx = 2.2
                posy = -1.5
                ax[idx].text(posx, posy, "V"+"$\mathrm{_{Zn}}$", fontsize=font_size, c='g',  alpha = 0.3)                
            
            elif condition == 'rich':
                posy = 1

        elif defect_name == "Mo":
            if condition == 'poor':
            
                posx = 2.1
                posy = 2.6
                ax[idx].text(posx, posy, f"{defect_name}"+"$\mathrm{_{Zn}}$"+"$\mathrm{v_O}$", fontsize=font_size, c='g')

                posx = 1.8
                posy = -5.5
                ax[idx].text(posx, posy, f"{defect_name}"+"$\mathrm{_{Zn}}$" + "+" + "$\mathrm{v_O}$", fontsize=font_size, c='g')

                posx = 2.5
                posy = -2
                ax[idx].text(posx, posy, f"{defect_name}"+"$\mathrm{_{Zn}}$", fontsize=font_size, c='g',  alpha = 0.3)                
                
            elif condition == 'rich':
                posx = 0.55
                posy = 1
    
        if idx == 0:
            ax[idx].set_ylabel("Formation Energy (eV)")
        ax[idx].text(0.1, 10, f"O-{condition}")

        ax[idx].set_xlabel("Fermi energy (eV)")
        ax[idx].set_xticks([0,1,2,3,4])
        
        ax[idx].set_xlim([0, bandgap])
        ax[idx].set_ylim([-7,11]) #ylim_min, ylim_max])
        
    plt.savefig(f"{defect_name}_fe.png",bbox_inches='tight')
    return fermi_energies, complexFE, sumFE
 
Mofermi_en, MocomplexFE, MosumFE = plot_defect_sum('Mo')
Nbfermi_en, NbcomplexFE, NbsumFE = plot_defect_sum('Nb')
Vfermi_en, VcomplexFE, VsumFE = plot_defect_sum('[V]')


####3 Plot Complex vacancy probability:
kBT2eV = 8.61732814974056E-05
def concentration(fe,T):
    return np.exp(-fe/(kBT2eV*T))*100

fig, ax = plt.subplots(figsize=(8,5))

ax.plot(Mofermi_en[3:], concentration(MocomplexFE[3:] - MosumFE[3:], 1200), c='black', label = f"Mo"+"$\mathrm{_{Zn}}$"+"$\mathrm{v_O}$")
ax.plot(Nbfermi_en[1:], concentration(NbcomplexFE[1:] - NbsumFE[1:], 1200), c='blue', label = f"Nb"+"$\mathrm{_{Zn}}$"+"$\mathrm{v_O}$")
ax.plot(Vfermi_en[2:], concentration(VcomplexFE[2:] - VsumFE[2:], 1200), c='red', label = f"V"+"$\mathrm{_{Zn}}$"+"$\mathrm{v_O}$")
ax.set_ylabel("Complex Vacancy\nProbability p(\%)")
ax.set_xlabel("Fermi Energy (eV)")
# ax.set_xlim([1, 3.5])
ax.legend()
plt.savefig("center_population_percent", bbox_inches='tight')

