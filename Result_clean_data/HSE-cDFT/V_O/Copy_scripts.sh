mkdir singlet_gs

#gs
FROM="/Users/szhang943/Library/CloudStorage/OneDrive-Personal/My_Works/Research/ZnO_defect/Results/2_HSErelax_RPA/Bridge_datas/V_O/q0"
TO="singlet_gs"

for file in CONTCAR INCAR OSZICAR POTCAR EIGENVAL KPOINTS OUTCAR
do 
cp $FROM/$file $TO/
done
