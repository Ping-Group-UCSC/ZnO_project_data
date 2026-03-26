#!/usr/bin/env python3
"""
This script plot the GW and DFT level single particle diagram from wfreq.json
"""

import json
import matplotlib.pyplot as plt
import numpy as np 

#________INPUT for data saving___________
dir_json = "../pdep_4992.wfreq.save" #name of the wfreq.save directory
Bands = np.arange(1220, 1260+1) #the range of band to output in to table
prefix = 'Mo2+VO_PBE0' #prefix of the table name and plot name

#_______INPUT for ploting_______
BndRange=[1240, 1247] #the range of band to plot
vbm = 0-0.55988680124252  # VBM of bulk- QP correction of VBM
cbm = 3.69-0.55988680124252   # CBM of bulk at PBE0+GW -QP correction of VBM
ylim = [-2, 5]  # plot range
label = "GW@PBE0"
GW_corr = False #add GW correction or not
ivbm=1237 # the index of band in defect system to align with VBM
interface='West'
fig_name="Movo_GW_diagram" #name of the figure
# mark the band of index:
#mark_up=[857,858,859,860,861,862] #band number to mark out
#mark_dn=[856,857,858,860]
mark_up=[]
mark_dn=[]
## ____________Input the GW and DFT band data__________________
#The Readqp method read in the name of the wfreq.json file, and a range of bands,
#return Edft, Eqp, occ

def find_json(directory):
    """
    find the last json file in directory;
    useage: find_json("../west.wfreq.save")
    """
    import glob
    import os
    # Directory containing the files
    #directory = "L_0.16/west.wfreq.save"

    # Pattern to match the files of interest
    pattern = os.path.join(directory, "wfreq_*.json")

    # Find all files matching the pattern
    files = glob.glob(pattern)

    # If no files are found, default to "wfreq.json"
    if not files:
        f_name = os.path.join(directory, "wfreq.json")
    else:
        # Sort the files by the number in their name, assuming the format is "wfreq_NUMBER.json"
        files_sorted = sorted(files, key=lambda x: int(x.split('_')[-1].split('.')[0]))
        # The last file in the sorted list is the one with the largest number
        f_name = files_sorted[-1]
#    print("found json file:",f_name)
    return f_name

def Readqp(f_name, Bands, Verbose=False):
    """
    INPUT
    ________________________
    f_name: string
        name of the json file
    Bands: list 
        A list of bands
    ________________________
    OUTPUT:
        Edft, Eqp
    Edft: numpy list 
        list of dft energy level.
        when nspin=2, Edft[0], Edft[1] for spin up and dn
    Eqp: numpy list
        list of qp correction
        when nspin=2, same as Edft
    Occ: numpy list
        list of occupation
    """
    import numpy as np
    # read data from JSON file
    with open(f_name, 'r') as file:
        data = json.load(file)
    # pretty print the data
    #print(json.dumps(data, indent=2))
    nspin = data["system"]["electron"]["nspin"]
    if nspin == 1:
        #find band index
        bandmap = data['input']['wfreq_control']["qp_bands"][0]
        # extracting energy levels from the data
        y = {}
        y['dft'] = data['output']['Q']['K000001']['eks']
        y['gw']  = data['output']['Q']['K000001']['eqpSec']
        y['qp'] = np.array(y['gw']) - np.array(y['dft'])
        y['occ'] = data['output']['Q']['K000001']['occupation']
        # output the list of data:
        Eqp = np.zeros(len(Bands))
        Edft = np.zeros(len(Bands))
        Occ = np.zeros(len(Bands))
        for i, band in enumerate(Bands):
            i_band = bandmap.index(band) #list index of band
            if Verbose==True:
                print("band : {} ; Index: {}".format(band, i_band))
            Eqp[i] = y['qp'][i_band]
            Edft[i] = y['dft'][i_band]
            Occ[i] = y['occ'][i_band]
        return Edft, Eqp, Occ
    elif nspin == 2:
        #find band index
        bandmap = data['input']['wfreq_control']["qp_bands"][0]
        # extracting energy levels from the data
        y = {}
        y['dft_up'] = data['output']['Q']['K000001']['eks']
        y['dft_dn'] = data['output']['Q']['K000002']['eks']
        y['gw_up']  = data['output']['Q']['K000001']['eqpSec']
        y['gw_dn']  = data['output']['Q']['K000002']['eqpSec']
        y['qp_up'] = np.array(y['gw_up']) - np.array(y['dft_up'])
        y['qp_dn'] = np.array(y['gw_dn']) - np.array(y['dft_dn'])
        y['occ_up'] = data['output']['Q']['K000001']['occupation']
        y['occ_dn'] = data['output']['Q']['K000002']['occupation']
        # output the list of data:
        Eqp = np.zeros((2,len(Bands))) # 2 for spin index
        Edft = np.zeros((2,len(Bands)))
        Occ = np.zeros((2,len(Bands)))
        for i, band in enumerate(Bands):
            i_band = bandmap.index(band) #list index of band
            if Verbose==True:
                print("band : {} ; Index: {}".format(band, i_band))
            Eqp[0,i] = y['qp_up'][i_band]
            Eqp[1,i] = y['qp_dn'][i_band]
            Edft[0,i] = y['dft_up'][i_band]
            Edft[1,i] = y['dft_dn'][i_band]
            Occ[0,i] = y['occ_up'][i_band]
            Occ[1,i] = y['occ_dn'][i_band]
        return Edft, Eqp, Occ
        

##___________________Save the data to table_____________
f_json = find_json(dir_json)
Edft, Eqp, Occ = Readqp(f_json, Bands)
for spin in [0,1]:
    print("spin:",spin)
    #for d, q, o, b in zip(Edft[spin], Eqp[spin], Occ[spin], Bands):
        #print(b, d,q,o)
#save data to a dataframe
import pandas as pd
Datas = {"Band": Bands, "Eqpup": Eqp[0], "Eqpdn":Eqp[1],"Edftup": Edft[0], "Edftdn":Edft[1],"Occup":Occ[0],"Occdn":Occ[1]}

df = pd.DataFrame(Datas)
#df["Band"] = df["Band"].astype('float64')
#df["Eup"] = df["Eup"].astype('float64'); df["Edn"] = df["Edn"].astype('float64')
#df["Occup"] = df["Occup"].astype('float64'); df["Occdn"] = df["Occdn"].astype('float64')
df.to_excel(prefix+"_Energy_out.xlsx")
df.to_csv(prefix+"_Energy_out.csv")


#________________Prepare data for plotting____________
#Input for QE:
#dir_f = "./relax_80Ry/relax.out"
#___________Generate input for the plting method_________________
ws = df[(df["Band"]>=BndRange[0]) & (df["Band"]<=BndRange[1])].\
astype(float).reset_index(drop=True) # Select the index range 
if not GW_corr: #no GW correction, use Edftup at band ivbm as 0 to align with
    vac = ((df[(df['Band']==ivbm)]['Edftup']+df[(df['Band']==ivbm)]['Edftdn'])/2).iloc[0] #vacuum value
else:
    vac = ((df[(df['Band']==ivbm)]['Edftup']+df[(df['Band']==ivbm)]['Edftdn'])/2).iloc[0]
    vac_qp = ((df[(df['Band']==ivbm)]['Eqpup']+df[(df['Band']==ivbm)]['Eqpdn'])/2).iloc[0]
    #align the ivbm at dft level to the 0 ; 0 is also the vbm at dft level. 
    #vac += vac_qp
    

# spin up eigenvalues and occupations
if interface=='qe':
    qe = qe_out(dir_f)
    qe.read_eigenenergies()
    band_index_up = BndRange
    band_index_dn = BndRange
    levels_up = np.arange(band_index_up[0], band_index_up[1])
    e_spinu = qe.eigenE_up[0, band_index_up[0]-1:band_index_up[1]-1] 
    occ_spinu = qe.occ_up[0, band_index_up[0]-1:band_index_up[1]-1]

    # spin down eigenvalues and occupations
    levels_dn = np.arange(band_index_dn[0], band_index_dn[1])
    e_spind = qe.eigenE_dn[0, band_index_dn[0]-1:band_index_dn[1]-1] 
    occ_spind = qe.occ_dn[0, band_index_dn[0]-1:band_index_dn[1]-1]

    #the aligned value use the average of up and dn of aligned band number
    vac = (qe.eigenE_up[0,i_Band_align-1]+qe.eigenE_up[0,i_Band_align-1])/2
elif interface=='west' or interface=="West":
    band_index_up = BndRange
    band_index_dn = BndRange
    levels_up = np.arange(len(ws['Band'])) #the index of spinup eigen velus
    levels_dn = np.arange(len(ws['Band'])) #the index of spindn eigen velus
    occ_spinu = ws['Occup']; occ_spind = ws['Occdn'] #list of occupations
    if not GW_corr:
        e_spinu = ws['Edftup'].to_numpy() ; e_spind = ws['Edftdn'].to_numpy()  #list of eigen values
    else:
        e_spinu = (ws['Edftup']+ws['Eqpup']).to_numpy() # add qp correction
        e_spind = (ws['Edftdn']+ws['Eqpdn']).to_numpy()
    #the aligned value use the average of up and dn of aligned band number
#__________________Plot____________________________________________



#Plot:
plt.rcParams["figure.titlesize"] = 16
plt.rcParams["lines.linewidth"] = 1.2
plt.rcParams["xtick.labelsize"] = 16
plt.rcParams["ytick.labelsize"] = 16
plt.rcParams["font.size"] = 16
plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.sans-serif"] = "Arial"
plt.rcParams["legend.fontsize"] = 16
plt.rcParams["figure.figsize"] = (4, 6)
plt.rcParams["figure.dpi"] = 100

# read data from dafaframe
#vbm = df[df["Band"]==ivbm]["Edftup"].iloc[0] # 1240 spin up band as vbm
if GW_corr:
    l_up = ws["Edftup"]+ws["Eqpup"]
    l_dn = ws["Edftdn"]+ws["Eqpdn"]
else:
    l_up = ws["Edftup"]
    l_dn = ws["Edftdn"]

occ_up = ws["Occup"]
occ_dn = ws["Occdn"]
gap = cbm-vbm

l_up -= vac #align
l_dn -= vac #Align
bands = ws["Band"]


###################PLOT#################
num_l_up = len(l_up)
num_l_dn = len(l_dn)

# Box length = 5
box_length = 5
states_length = box_length/4 # length of the states lines
ups_l_coord = box_length/4 * 2/3 # left coordinate of the up states
middle_space = box_length/4 * 2/3 # length of space between states
dns_l_coord = ups_l_coord + states_length + middle_space # 3.3 left coordinate of the down state


fig, ax = plt.subplots(nrows=1, ncols=1, constrained_layout=True)
#fig, ax = plt.subplots(nrows=1, ncols=1, constrained_layout=False)

# plot VB and CB
top = 7.0
bottom = gap - top+2


ax.fill_between(
    [0, 5],
    [bottom, bottom], [vbm, vbm],
    color="forestgreen"#, alpha=0.9
)
ax.fill_between(
    [0, 5],
    [cbm, cbm], [top, top],
    color="grey", alpha=0.6
)


# # Plot defect levels and labels
for i in range(num_l_up):
    if occ_up[i] == 1 or occ_up[i] == 0.5 :
        ax.plot(
            np.full((num_l_up, 2), [ups_l_coord, ups_l_coord + states_length])[i, :],
            np.stack((l_up, l_up), axis=-1)[i, :],
            color="black"
        )
    elif occ_up[i] == 0:
        ax.plot(
            np.full((num_l_up, 2), [ups_l_coord, ups_l_coord + states_length])[i, :],
            np.stack((l_up, l_up), axis=-1)[i, :], '--',
            color="black"
        )
    if bands[i] in mark_up: #index of spinup
        ax.text(2*ups_l_coord/3, l_up[i], l_up[i].round(2), verticalalignment='center', horizontalalignment = 'center')

for i in range(num_l_dn):
#     if i != 6 and i != 7:
    if occ_dn[i] == 1:
        ax.plot(
            np.full((num_l_dn, 2), [dns_l_coord, dns_l_coord + states_length])[i, :],
            np.stack((l_dn, l_dn), axis=-1)[i, :],
            color="tab:red"
        )
    elif occ_dn[i] == 0:
        ax.plot(
            np.full((num_l_dn, 2), [dns_l_coord, dns_l_coord + states_length])[i, :],
            np.stack((l_dn, l_dn), axis=-1)[i, :], '--',
            color="tab:red"
            )
    if bands[i] in mark_dn: #index of spin dn
         ax.text(dns_l_coord+states_length + 1/3*(ups_l_coord), l_dn[i], l_dn[i].round(2), verticalalignment='center', horizontalalignment='center')

# Plot Arrows:
# Spin up
occ_up_states = l_up[occ_up==1].reset_index(drop=True)
j = 0
arr_length = 0.5
while j <=  len(occ_up_states) - 1:
    try:
        if np.abs(occ_up_states[j] - occ_up_states[j+1]) <= 0.005:
            ax.arrow(ups_l_coord + (1/3)*states_length, occ_up_states[j] - arr_length/2, 0.0, arr_length, fc='black', ec='black', width = 0.05, head_width = 0.12 ,length_includes_head = True)
            ax.arrow(ups_l_coord + (2/3)*states_length, occ_up_states[j+1] - arr_length/2, 0.0, arr_length, fc='black', ec='black', width = 0.05, head_width = 0.12, length_includes_head =True)
            j+=1
        else:
            ax.arrow(ups_l_coord + 0.5*states_length, occ_up_states[j] - arr_length/2, 0.0, arr_length, fc='black', ec='black', width = 0.05, head_width = 0.12, length_includes_head = True)
    except:
        ax.arrow(ups_l_coord + 0.5*states_length, occ_up_states[j] - arr_length/2, 0.0, arr_length, fc='black', ec='black', width = 0.05, head_width = 0.12, length_includes_head = True)
    j+=1

# Spin dn
occ_dn_states = l_dn[occ_dn==1].reset_index(drop=True)
j = 0
while j <=  len(occ_dn_states) - 1:
    try:
        if np.abs(occ_dn_states[j] - occ_dn_states[j+1]) <= 0.005:
            print(occ_dn_states[j], occ_dn_states[j+1],"are same")
            ax.arrow(dns_l_coord + (1/3)*states_length, occ_dn_states[j] + arr_length/2, 0.0, -arr_length, fc='black', ec='black', width = 0.05, head_width = 0.12, length_includes_head = True)
            ax.arrow(dns_l_coord + (2/3)*states_length, occ_dn_states[j+1] + arr_length/2, 0.0, -arr_length, fc='black', ec='black', width = 0.05, head_width = 0.12, length_includes_head =True)
            j+=1
        else:
            ax.arrow(dns_l_coord + 0.5*states_length, occ_dn_states[j] + 0.25, 0.0, -arr_length, fc='black', ec='black', width = 0.05, head_width = 0.12, length_includes_head = True)
    except:
        ax.arrow(dns_l_coord + 0.5*states_length, occ_dn_states[j] + 0.25, 0.0, -arr_length, fc='black', ec='black', width = 0.05, head_width = 0.12, length_includes_head = True)
    j+=1

#half occupation up:
occ_up_states_half = l_up[occ_up==0.5].reset_index(drop=True)
j = 0
arr_length = 0.8
while j <=  len(occ_up_states_half) - 1:
    try:
        if np.abs(occ_up_states_half[j] - occ_up_states_half[j+1]) <= 0.005:
            ax.arrow(ups_l_coord + (1/3)*states_length, occ_up_states_half[j] - arr_length/2, 0.0, arr_length, fc='grey', ec='grey', width = 0.05, head_width = 0.12 ,length_includes_head = True)
            ax.arrow(ups_l_coord + (2/3)*states_length, occ_up_states_half[j+1] - arr_length/2, 0.0, arr_length, fc='grey', ec='grey', width = 0.05, head_width = 0.12, length_includes_head =True)
            j+=1
        else:
            ax.arrow(ups_l_coord + 0.5*states_length, occ_up_states_half[j] - arr_length/2, 0.0, arr_length, fc='grey', ec='grey', width = 0.05, head_width = 0.12, length_includes_head = True)
    except:
        ax.arrow(ups_l_coord + 0.5*states_length, occ_up_states_half[j] - arr_length/2, 0.0, arr_length, fc='grey', ec='grey', width = 0.05, head_width = 0.12, length_includes_head = True)
    j+=1


# ax.text(0.2, l_up[i], l_up[i].round(2), verticalalignment='center')
#ax.text(2*ups_l_coord/3, gap + 0.2, gap.round(2), verticalalignment='center', horizontalalignment = 'center')
ax.text(2.5, bottom/2-0.4, "Valence Band", size=18, c='w',  horizontalalignment='center',
     verticalalignment='center')
ax.text(2.5, (top)-0.7 , "Conduction Band", size = 18, c='w', horizontalalignment='center',
     verticalalignment='center')



ax.set_ylabel('Energy (eV)')
ax.set_yticks([0,1,2,3,4,5,6])
ax.set_ylim(bottom,top) # Set the range of y-axis
ax.set_xlim(0,5)
plt.tick_params(labelbottom = False, bottom = False)

#plt.savefig(os.path.join(cwd, defect_name, defect_name))
#plt.show()
fig.savefig(fig_name)

