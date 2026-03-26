import json
import numpy as np
import pandas as pd
from westpy.qdet import QDETResult

#######################Solve QDET#######################
"""
#__________Build symmetry group________________(Need to edit)_
origin = 120 * np.array([0.65843, 0.49176, 0.49176])
from westpy.qdet.symm import PointGroup, PointGroupOperation, PointGroupRotation
from westpy.qdet.symm import PointGroupReflection
from westpy import VData
sq3 = np.sqrt(3)
point_group = PointGroup(
    name="C3v",
    operations={
        "E": PointGroupOperation(T=np.eye(4)),
        "C3_1": PointGroupRotation(rotvec=2 * np.pi / 3 * np.array([1/sq3, 1/sq3, 1/sq3]),
                                   origin=origin),
        "C3_2": PointGroupRotation(rotvec=4 * np.pi / 3 * np.array([1/sq3, 1/sq3, 1/sq3]),
                                   origin=origin),
        "Cv_1": PointGroupReflection(normal=(1, -1, 0), origin=origin),
        "Cv_2": PointGroupReflection(normal=(0, -1, 1), origin=origin),
        "Cv_3": PointGroupReflection(normal=(-1, 0, 1), origin=origin)
    },
    ctable={
        "A1": [1, 1, 1, 1, 1, 1],
        "A2": [1, 1, 1, -1, -1, -1],
        "E": [2, -1, -1, 0, 0, 0]})
#__________Add a list of wfc files for symmetry_________________(change the wfc_path)
effective_hamiltonian = QDETResult(filename='../west.wfreq.save/wfreq.json')
bands=effective_hamiltonian.__dict__['basis'] # a list of bands
print(f"basis set is {bands}")
wfc_path = "/pscratch/sd/s/szhan213/QDET/NV-/PWSCF/pw_unpol/wfc"
wfct_filenames=[]
for b in bands:
    #her gives the formatting, to let band shows in 3 integer and wiht 0 in front
    #f_name = ''.join(['{}'.format(wfc_path),'/Bandup','{:03}'.format(b),'.cube'])
    f_name = ''.join(['{}'.format(wfc_path),'/Bandup{}'.format(int(b)),'.cube'])
    wfct_filenames.append(f_name)
"""
#__________Solve the QDET____________________________
#______(Quote out the above part is symmetry is not desired),rremove point_group and wfc_filenames in input)
# construct object for effective Hamiltonian

effective_hamiltonian = QDETResult(filename='../pdep_4992.wfreq.save/wfreq.json')
#let M=0
occ=effective_hamiltonian.__dict__['occupation']
nelec = (int(occ.sum()/2),int(occ.sum()/2))
# diagonalize Hamiltonian
solution = effective_hamiltonian.solve(nroots = 50, nelec=nelec)


#_______________Save the QDET_____________________
#Here only write the Energy, Spin and symmetry. If no symmetry, remove the 'Sym' and 'Sym_component'
#Write the solution into dataframe
import pandas as pd
print()
Out_dict={'Energy': solution['evs'],
             'Spin': solution['mults']}

df = pd.DataFrame.from_dict(Out_dict)
df.to_csv('QDET_output.csv',sep=',',index=False)
#To read dataframe use df=pd.read_csv('QDET_output.csv')

##############################################################################
#______________________Print the Slater determinant___________________________
#############################################################################
from Plot_Slater import *
#___________________1.Print out to file___________________
#required input: sffective hamiltonian and solution from last section
#output file is can be edited
get_slater_determinant(effective_hamiltonian, solution,f_out='QDET_Slater.txt')


"""
#Plot part has been moved to a new script: QDET_Slater_visulaze.py
#____________________2.Plot the slater determinant____________
#The slater determinant info come from 'QDET_Slater.txt' in last part
#also require a label mapping for spin up and spindn channel:
#format of f_character_up is a df with df['Band'], df["Irred(up)"]
#format of f_character_dn is a df with df['Band'], df["Irred(dn)"]
#1.use parse_results(file_name) to read-in the data. format of data see help(parse_results)
res, basis_bands = parse_results("QDET_Slater.txt")
res.head()
#2.Read in the orbital chracter from an excel file, format see help(Read_orbiatal_name)
f_character_up='Spinup_chra.xlsx'
f_character_dn='Spindn_chra.xlsx'
dict_orbital_up=Read_orbiatal_name(f_character_up)
dict_orbital_dn=Read_orbiatal_name(f_character_up) #output a dictionary for band-->character
#3.Build the mapping relation between the Fock basis and hole notation:
my_mapping_up=Map_fock_to_holenotation(res,basis_bands,dict_orbital_up)
my_mapping_dn=Map_fock_to_holenotation(res,basis_bands,dict_orbital_dn)
print(my_mapping_up)
my_mapping=(my_mapping_up,my_mapping_dn)
#4.Construct a label column in dataframe:
res_noted=Cal_hole_notation_label(res,my_mapping,spin=1)
#5 (Option), put the threshold, filter out slater determinant with small weight
new_res=Filter_threshod(res_noted,thro=0.05)
#5.Plotting:
#           You can change the dirname: the name of the output directory to contain the pictures
import os
plt.rcParams["figure.titlesize"] = 8
plt.rcParams["lines.linewidth"] = 0.5
plt.rcParams["xtick.labelsize"] = 10
plt.rcParams["ytick.labelsize"] = 10
plt.rcParams["font.size"] = 14
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = "Arial"
plt.rcParams["legend.fontsize"] = 14
plt.rcParams["figure.figsize"] = (6,2)
plt.rcParams["figure.dpi"] = 100


#Slater_Plot(ax[0],new_res,0)
#Slater_Plot(ax[1],new_res,1)
#Slater_Plot(ax[2],new_res,2)
#Slater_Plot(ax[3],new_res,3)
#read in the qdet result
qdet_out=pd.read_csv('QDET_output.csv')
Index=qdet_out.index.tolist()
E=[qdet_out['Energy'][i] for i in Index]
dirname = 'Slaterplots'
if not os.path.exists(f'./{dirname}'):
    os.mkdir(dirname)
for i,e in zip(Index,E): #i for axis index, d for energy index
    fig, ax = plt.subplots(nrows=1, ncols=1)#, constrained_layout=True) #for 6x6
    Slater_Plot(ax,new_res,i)
    ax.set_xlim(0,9)
    #ax[i].set_title(f"i={i},E={E[i]}",size=10,loc='right',y=0.75,)
    ax.text((ax.get_xlim()[1]-1.8),0.8,f"i={i},E={round(e,2)}",size=10)
    fig_name=f"{dirname}/Plot_Slat_E_{i}.png"
    plt.savefig(fig_name,facecolor="w",bbox_inches='tight') #the facecolor problem is the jupyter thing
    plt.close()
"""
