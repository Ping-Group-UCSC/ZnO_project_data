mkdir spin_maj_cdft	spin_min_cdft	triplet_gs

#gs
FROM="/Users/szhang943/Library/CloudStorage/OneDrive-Personal/My_Works/Research/ZnO_defect/Results/2_HSErelax_RPA/Bridge_datas/V+/HSE_relax_refine_2"
TO="triplet_gs"
#spin min:
FROM="/Users/szhang943/Library/CloudStorage/OneDrive-Personal/My_Works/Research/ZnO_defect/Results/2_HSErelax_RPA/Bridge_datas/V+/HSE_cdft_dn/HSE_cdft_relax_4"
TO="spin_min_cdft"
#spin maj: 
FROM="/Users/szhang943/Library/CloudStorage/OneDrive-Personal/My_Works/Research/ZnO_defect/Results/2_HSErelax_RPA/Bridge_datas/V+/HSE_cdft_up/HSE_cdft_relax"
TO="spin_maj_cdft"

for file in CONTCAR INCAR OSZICAR POTCAR EIGENVAL KPOINTS OUTCAR
do 
cp $FROM/$file $TO/
done
