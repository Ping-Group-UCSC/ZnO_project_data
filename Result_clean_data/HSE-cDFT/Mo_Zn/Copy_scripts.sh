mkdir triplet_gs

#gs
FROM="/Users/szhang943/Library/CloudStorage/OneDrive-Personal/My_Works/Research/ZnO_defect/Results/2_HSErelax_RPA/Bridge_datas/Mo_Zn/q2"
TO="triplet_gs"

for file in CONTCAR INCAR OSZICAR POTCAR EIGENVAL KPOINTS OUTCAR
do 
cp $FROM/$file $TO/
done
