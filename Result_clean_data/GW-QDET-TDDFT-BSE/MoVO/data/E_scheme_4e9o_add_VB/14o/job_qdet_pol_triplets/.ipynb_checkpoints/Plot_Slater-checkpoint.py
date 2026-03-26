"""
This is the package to extract the Slated determinant, transfer the notation, and plot it
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy as np

def get_slater_determinant(effective_hamiltonian, solution,f_out='QDET_Slater.txt'):
    """
    return the slater determinant, with threshold = 10**(-1)
    f_name is the address of wfrq.json; f_out is the output file name
    solution: solution is the solution object obtained by 
    solution = effective_hamiltonian.solve(nroots = 50)
    ________
    Usage:
    # construct object for effective Hamiltonian
    effective_hamiltonian = QDETResult(filename='west.wfreq.save/wfreq.json')

    # diagonalize Hamiltonian
    solution = effective_hamiltonian.solve(nroots = 50)
    get_slater_determinant(effective_hamiltonian, solution,f_out='QDET_Slater.txt')
    """
    #effective_hamiltonian, solution = get_solution(f_name)
    from westpy.qdet import visualize_correlated_state
    basis=effective_hamiltonian.__dict__['basis'].tolist()
    basis_s=str(basis).replace(',',' ')#here we fromat the basis output in ot [1 2 3]
    f = open(f_out,'w')
    f.write(f"The basis bands are {basis_s}\n")
    for i, state in enumerate(solution['evcs']):
        en = solution['evs'][i]
        f.write(f'i= {i}, en [eV]={en} Deter')
        f.write(visualize_correlated_state(state, solution['norb'], solution['nelec'], cutoff=10 **(-1)))
        f.write('\n')
    f.close()

'''
The following result are used to read the output file from get_slater_determinant and plot it
'''
def parse_results(file_name):
    """
    read the slater determinant output data file.
    requre a "Deter" before each slated determinant, space between Deter and energy number
    require i= ... at the begining of line, all the rest is only one line
    INPUT:
    file_name: name of the data file, str
    _____
    OUTPUT:
    all_results: a dataframe 
    basis_bands: a list of basis band
    
    """
    #df = pd.read_csv(file_name, header=None, sep='\n')
    df = pd.read_fwf(file_name, header=None)
    basis_band_str = df[0][0] + df[0][1]
    basis_bands = basis_band_str.replace("The basis bands are ", "").split("[")[1].split("]")[0].replace("  ", " ").split(" ")
    #basis_bands.pop(0);
    basis_bands = pd.Series(basis_bands)
    basis_bands = basis_bands[::-1].reset_index(drop=True)
    energy = df[0].str.findall("(?s)(?<=eV]=).*?(?=Deter)").explode() #requre a "Deter" before each slated determinant
    index = df[0].str.findall("(?s)(?<=i=).*?(?=,)").explode()
    energy.pop(0); index.pop(0);
    energy.reset_index(inplace=True, drop=True)
    index.reset_index(inplace=True, drop=True)
    
    result = df.drop([0], axis = 0)
    #print("results is ",result)
    result['energy'] = energy
    result['i'] = index
    remainder = df[0].str.findall("(?<=Deter).*").explode()
    #print(remainder)
    remainder.pop(0); remainder = pd.Series(remainder).reset_index(drop=True)
    total = remainder.str.split('|')
    #print(total)
    total[0] = [np.nan, np.nan]
    total = total.apply(lambda x: x[0])
    result['total'] = total
    #for lower version of pandas: (1.5)
    #remainder_splitted = remainder.str.replace('|', ',',regex=True).str.replace('>', ',',regex=True).str.split(',').apply(lambda x: [y for y in x if y])
    #for higher version of pandas: (2.0)
    remainder_splitted = remainder.str.replace('|', ',').str.replace('>', ',').str.split(',').apply(lambda x: [y for y in x if y])
    all_results = []
    
    for i in range(len(remainder_splitted)):
        vvv = remainder_splitted[i]
        results_i = []
        for j in range(len(vvv)):
            if (j + 1) % 3 == 1:
                output_value = vvv[j]
            elif (j+1) % 3 == 2:
                my_x = vvv[j]
            else:
                my_y = vvv[j]
                results_i.append({'value': output_value,
                                 'Fock_up': my_x,
                                 'Fock_dn': my_y,
                                 'energy': energy[i],
                                 'index': index[i]})
        all_results += results_i

    all_results = pd.DataFrame(all_results)
    all_results['value'] = all_results['value'].astype(float)
    all_results['energy'] = all_results['energy'].astype(float)
    all_results['index'] = all_results['index'].astype(int)
    return all_results, basis_bands


def Map_fock_to_holeBand(list_input_strings, basis_bands):
    """
    Generate a Dictionary for the mapping relation
    Map fock basis into a band number
    ___INPUT___
    list_input_strings: list
        a list consist of fock basis string
    basis_bands: list
        a list consist of basis band
    The index of them should be corresponded
    """
    output = {}
    for i in list_input_strings:
        output[str(i)] = int(basis_bands[i.rfind('0')])
    return output


def Map_fock_to_holenotation(res,basis_bands,orbital_name):
    """
    Generate a Dictionary for the mapping relation
    
    Map fock basis into a hole notation. if the band number is not included in orbital_name dictionary,
    then still use band number to label the state
    ___INPUT___
    res: Dataframe
        Dataframe read by parse_results(filename)
    basis_bands: list
        a list consist of basis band
    orbital_name: dictionary
        orbital_name['bandnumber']='orbital name'; here the band number should be an integer
    For each fock basis string, the index of its fock basis and basis_bands should be corresponded
    ___OUTPUT__
    * output2: a dictionary to map fock basis into hole notation
    """
    possible_values = list(set(res['Fock_up']) | set(res['Fock_dn'])) # all the possible fock basis in data frame
    list_input_strings=possible_values
    output = {}
    output2= {}
    for i in list_input_strings:
        L=list(str(i))
        match = [i for i,x in enumerate(L) if x == '0']
        output[str(i)] = [int(basis_bands[ind]) for ind in match]
        output2[str(i)]=''
        for name in output[str(i)]:
            if name in orbital_name.keys():
                #print(name,'is in orbital list',orbital_name[name])
                output2[str(i)]= output2[str(i)]+"|"+str(orbital_name[name])+">"
            else:
                output2[str(i)]= output2[str(i)]+"|"+str(name)+">"
        output2[str(i)] = output2[str(i)].replace(">|",",")
    print("Mapping relation:",output2)
    return output2

def Read_orbiatal_name(f_name):
    """
    f_name: an excel file name
        first column should be the band number: int
        second column should be the corresponded state: str
    """
    df_orbital=pd.read_excel(f_name)
    dict_orbital=pd.Series(df_orbital.iloc[:,1].values,index=df_orbital.iloc[:,0]).to_dict()
    return dict_orbital


def Cal_hole_notation_label(res,my_mapping,spin=0):
    """
    INPUT:
    * res: result dataframe ouputed by parse_results(filename)
    * spin: 0 for spin unpolarized calculation, 1 for spin-polarized calculation
        if spin==0:
            * my_mapping: a dictionary, map a string of fock basis into a string of name
        if spin==1:
            * my_mapping: a list of dictionary. 
                my_mapping[0] is the mapping dictionary for spin up channel
                my_mapping[1] is the mapping dictionary for spin dn channel
    _______
    OUTPUT:
    res: a renewed dataframe
        the new dataframe are same as input, except there's a new colume name ref['label'],
        which gives the new label of each fock basis
    
    """
    if spin==0:
        res['label'] = '|'+res['Fock_up'].map(my_mapping)+','+res['Fock_dn'].map(my_mapping)+'>'
    elif spin==1:
        res['label'] = '|'+res['Fock_up'].map(my_mapping[0])+','+res['Fock_dn'].map(my_mapping[1])+'>'
    else:
        print("spin parameter incorrect")
    return res

def multiline_labels(label, char_limit):
    """
    Asistant method for Slater_Plot. This method will make the label string multiline with given line width
    INPUT:
        label : a string. The fock basis label
        char_limit: the maximum width of one line
    """
    return '\n'.join([label[i:i+char_limit] for i in range(0, len(label), char_limit)])

def Slater_Plot(ax,df_w_label,index,y_value=True,textpos=(0.20,0.005),loose=1.5,label_width=10):
    """
    plot the State at cetrain index
    __INPUT___
    * ax: matplotlib axis object
    * df_w_label: dataframe with valid df_w_label['label']
    * index: integer
        The index of solution, index=0 means ground state
    * y_value: if y_value=True, then show the value of value
    * textpos: adjust text position
    * loose = 1; used to adjust how loose are the bars
    * label_width: int; 
        the maximum length of a multiline table
    """
    df=df_w_label[df_w_label['index'] == index]#select cetain index
    X=[0.5+i*loose for i in range(0,len(df))]
    Y=df['value']**2
    Labels = [multiline_labels(lab, label_width) for lab in df['label']]
    ax.bar(X,Y,width=0.5,tick_label=Labels,color='C0')
    for i, v in enumerate(Y.tolist()):
        ax.text(X[i] - textpos[0], v + textpos[1], str(round(v,2)),size=8)
    ax.set_xlim(0,9)
    ax.set_ylim(0,1)
    Energy=df['energy'].max(); Energy=round(Energy,3)
    print(f'State at E={Energy}, at index={index}')
    print(f"Number of basis: {len(df)}, where the nonzero terms are:\n {df['label']}")
    #ax.set_title('E: ' + str(df_w_label['energy'].max()))



def Filter_threshod(res, thro=0.05):
    """
    INPUT: 
    * res: dataframe read from parse_results. 
        requrement: res['value'] exist
    * thro: float:
        the filter threshod, when slater determinant parameter < 0.05, remove the term
    OUTPUT:
    * res_filtered:
        the new dataframe, where all the data point with value<thro were deleted
    """
    res_filtered = res[res['value']**2 > thro]
    return res_filtered

def Write_slater_hole(res_noted, fout="Slater_hole.txt"):
    """
    write the hole notation slater determinant into a file
    INPUT:
        res_noted: the dataframe with df["label"] being label, 'index' being index, and "energy" being energy;
                    'value' being the Fock basis parameters
                    value	Fock_up	Fock_dn	energy	index	label
                0	0.707	001111111111	010111111111	0.000000	0	||2a1'',ex'>,|2\na1'',ey'>>
                1	-0.707	010111111111	001111111111	0.000000	0	||2a1'',ey'>,|2\na1'',ex'>>
        fout: name of the output file
    """
    f = open(fout, 'w', encoding='utf-8')
    for i in res_noted["index"].unique():
        #here i don't use zip(df[index], df[energy]), this is to avoid the rear case when two energy are exactly generated
        dfe = res_noted[res_noted["index"]==i] #This used to select the unit energy 
        e = dfe['energy'].iloc[0] #This gives the enrgy of index i
        dfi = res_noted[res_noted['index']==i]
        value = dfi["value"].tolist()
        fock = dfi["label"].tolist()
        outi = ''
        for v, ff in zip(value,fock): #parameter value and fock basis name
            outi = outi + str(v) + str(ff)
        headline = "i = {} , E = {}\n".format(i,e)
        #print(headline)
        f.write(headline)
        #print(outi)
        f.write(outi+"\n")
