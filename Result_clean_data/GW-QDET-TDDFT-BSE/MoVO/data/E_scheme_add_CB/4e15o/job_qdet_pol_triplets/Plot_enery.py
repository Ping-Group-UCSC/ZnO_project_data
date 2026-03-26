import matplotlib.pyplot as plt
import numpy as np
import os
import sys
def Plot_Energy(ax,df,ylim=(-0.2,5),i_mark=[],i_label=[],i_color='black'):
    """
    df dataframe by Read_qdet
    i_mark: a list of index, to mark the Ei in this list
    i_label: the label of the marked energy
    i_color: if it is a string, all the marked E are colored as it
             if it is a list, it should have len of len(i_mark), gives the color of all marked bands
    """
    E = df['Energy'].tolist()
    x = [0.23,0.37]
    if len(i_mark):    
        if isinstance(i_color, str):
            i_color = [i_color]*len(i_mark) # it the color is str, then all label have same color
        for index, i in enumerate(i_mark):#index is the index of element, i is the elment number
            y=[E[i], E[i]]
            ax.plot(x, y, color=i_color[index])
            if y[0]<=ylim[1]: #add the text to the marked band
                ax.text(0.18,E[i],i_label[index],fontsize=15,color=i_color[index])
                ax.text(0.27,y[0]+0.05,round(E[i],2),fontsize=15,color=i_color[index])
    for i in range(0,len(E)):
        if i not in i_mark:
            y=[E[i], E[i]]
            ax.plot(x, y, color='black')
    ax.set_ylim(ylim)
    ax.set_xlim(0.1, 0.5)
    ax.set_xticks([])
    ax.set_xticklabels([])

def Plot_Energy_withS(ax,df,ylim=(-0.2,5),i_mark=[],i_label=[],i_color='black'):
    """
    df dataframe by Read_qdet
    i_mark: a list of index, to mark the Ei in this list
    i_label: the label of the marked energy
    i_color: if it is a string, all the marked E are colored as it
             if it is a list, it should have len of len(i_mark), gives the color of all marked bands
    """
    E = df['Energy'].tolist()
    S = df['Spin'].tolist()
    #x = [0.23,0.37]
    dx = 0.4 #the width of energy level bar
    for i in range(0,len(E)):
        if i not in i_mark:
            y=[E[i], E[i]]
            s = S[i] #spin
            ax.scatter(s, E[i], color='grey',s=3)
            ax.plot([s-dx,s+dx], y, color='grey')
    if len(i_mark):    
        if isinstance(i_color, str):
            i_color = [i_color]*len(i_mark) # it the color is str, then all label have same color
        for index, i in enumerate(i_mark):#index is the index of element, i is the elment number
            y=[E[i], E[i]]
            s = S[i]
            ax.scatter(s, E[i], color=i_color[index],s=3)
            ax.plot([s-dx,s+dx], y, color=i_color[index])
            if y[0]<=ylim[1]: #add the text to the marked band
                ax.text(s+1.5*dx,E[i]-0.04,i_label[index]+f',{round(E[i],2)} eV',fontsize=10,color=i_color[index])
                #ax.text(s,y[0]+0.5*dx,round(E[i],2),fontsize=10,color=i_color[index])

    #TODO: Plot a range of S
    ax.set_ylim(ylim)
    ax.set_xlim(0.8,5.5)
    ax.set_xticks([1,2,3,4,5])
    ax.set_xticklabels([1,2,3,4,5])
    ax.set_xlabel("2S+1")


############
plt.rcParams["lines.linewidth"] = 2
plt.rcParams["xtick.labelsize"] = 15
plt.rcParams["ytick.labelsize"] = 15
plt.rcParams["font.size"] = 15
#plt.rcParams["font.family"] = "sans-serif"
#plt.rcParams["font.sans-serif"] = "Arial"
plt.rcParams["axes.titlesize"] = 15
#plt.rcParams["legend.fontsize"] = 16
#plt.rcParams["figure.figsize"] = (12,5.5)
plt.rcParams["figure.figsize"] = (3,6)
plt.rcParams["figure.dpi"] = 100
#_____
ylim=(-0.2,5)

#INPUT:
f_path = "QDET_output.csv"
df = pd.read_csv(f_path)
######

fig, ax = plt.subplots(nrows=1, ncols=1,sharey=True)
# print all S when close to 3: 
print(f"4e4o : (S~3 states)")
print(df[abs(df['Spin']-3)<0.5])
# print all S when close to 1: 
print(f"4e4o : (S~1 states)")
print(df[abs(df['Spin']-1)<0.8])
#Plot_Energy(ax[i],df,ylim=(-0.2,5),i_mark=[0,1,3,4,6],i_label=["A2",'1E',"1A1","3E","E"],i_color='black')
#Plot_Energy(ax[i],df)
Plot_Energy_withS(ax,df, ylim=(-0.2,4),i_mark=[1, 5, 8],i_label=['3E', "3E'","3E'' " ],i_color='black')
#Plot_Energy(ax[i],df,ylim=(-0.2,4),i_mark=[0,1,3,4],i_label=["A2",'1E',"1A1","3E"],i_color='black')
ax.set_title("4e4o")
ax.set_ylabel("Energy(eV)")
fig.subplots_adjust(wspace=0)
fig.savefig("QDET_Band_wS.pdf",bbox_inches="tight")




