mkdir spin_maj_cdft	spin_min_cdft	triplet_gs

#gs
FROM="/Users/szhang943/Library/CloudStorage/OneDrive-Personal/My_Works/Research/ZnO_defect/Results/2_HSErelax_RPA/Bridge_datas/Nb+/HSE_relax_refine3"
TO="triplet_gs"
#spin maj: 
FROM="/Users/szhang943/Library/CloudStorage/OneDrive-Personal/My_Works/Research/ZnO_defect/Results/2_HSErelax_RPA/Bridge_datas/Nb+/HSE_cdft_up/HSE_cdft_relax_half_occ_4"
TO="spin_maj_cdft"
#spin min:
FROM="/Users/szhang943/Library/CloudStorage/OneDrive-Personal/My_Works/Research/ZnO_defect/Results/2_HSErelax_RPA/Bridge_datas/Nb+/HSE_cdft_dn/HSE_cdft_gs_geo"
TO="spin_min_cdft"

for file in CONTCAR INCAR OSZICAR POTCAR EIGENVAL KPOINTS OUTCAR
do 
cp $FROM/$file $TO/
done
