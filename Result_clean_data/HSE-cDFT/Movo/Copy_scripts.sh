mkdir spin_maj_cdft	spin_min_cdft	triplet_gs singlet_gs

#gs
FROM="/Users/szhang943/Library/CloudStorage/OneDrive-Personal/My_Works/Research/ZnO_defect/Results/2_HSErelax_RPA/Bridge_datas/Mo2+/relax_gs_Mosv"
TO="triplet_gs"
#spin maj: 
FROM="/Users/szhang943/Library/CloudStorage/OneDrive-Personal/My_Works/Research/ZnO_defect/Results/2_HSErelax_RPA/Bridge_datas/Mo2+/relax_cdftup_Mosv"
TO="spin_maj_cdft"
#spin min:
FROM="/Users/szhang943/Library/CloudStorage/OneDrive-Personal/My_Works/Research/ZnO_defect/Results/2_HSErelax_RPA/Bridge_datas/Mo2+/relax_cdftdn_Mosv"
TO="spin_min_cdft"
#singlet gs:
FROM="/Users/szhang943/Library/CloudStorage/OneDrive-Personal/My_Works/Research/ZnO_defect/Results/2_HSErelax_RPA/Bridge_datas/Mo2+/relax_gs_singlet"
TO="singlet_gs"
for file in CONTCAR INCAR OSZICAR POTCAR EIGENVAL KPOINTS OUTCAR
do 
cp $FROM/$file $TO/
done
