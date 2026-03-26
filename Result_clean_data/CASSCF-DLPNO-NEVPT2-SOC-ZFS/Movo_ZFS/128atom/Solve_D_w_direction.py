#this script solve for the D and E by defining [0,0,1] as z direction; [ 


import numpy as np
#___________INPUT__________
f_zfs="zfs.out"
ref_z_direction=np.array([0,0,1])
ref_x_direction=np.array([1,0,0])
ref_y_direction=np.array([0,1,0])

print("Definition of direction:\nX:{}\nY:{},\nZ:{}".format(ref_x_direction,ref_y_direction,ref_z_direction))

# Raw matrix for spinspin and spin-orb
# Initialize variables to store the matrices
raw_matrix = []
spin_spin_matrix = []

# Flags to identify sections
in_raw_matrix = False
in_spin_spin_matrix = False

with open(f_zfs,'r') as f:
    for line in f:
        # Identify the start of the raw matrix section
        if "raw-matrix :" in line:
            in_raw_matrix = True
            continue
        # Identify the end of the raw matrix section
        if in_raw_matrix and line.strip() == "":
            in_raw_matrix = False
        
        # Parse raw matrix
        if in_raw_matrix:
            raw_matrix.append(list(map(float, line.split())))
        
        # Identify the start of the SPIN-SPIN-PART matrix section
        if "SPIN-SPIN-PART" in line:
            in_spin_spin_matrix = True
            continue
        # Parse SPIN-SPIN-PART matrix
        if in_spin_spin_matrix and "0          1          2" in line:
           continue
        if in_spin_spin_matrix and len(line.split())==4:
            spin_spin_matrix.append(list(map(float, line.split()[1:])))
        # Identify the end of the SPIN-SPIN-PART matrix section
        if in_spin_spin_matrix and 'Exchange' in line:
            in_spin_spin_matrix = False

# Print the matrices
print("Raw Matrix:")
print(raw_matrix)
print("\nSPIN-SPIN-PART Matrix:")
print(spin_spin_matrix,'\n')


# Diagonalize the matrix_raw
eigenvalues_raw, eigenvectors_raw = np.linalg.eig(raw_matrix)

# Print the results
print("Eigenvalues(raw):")
print(eigenvalues_raw)
print("\nEigenvectors(raw) (columns correspond to eigenvalues):")
print(eigenvectors_raw)

# Diagonalize the matrix_spinspin
eigenvalues_ss, eigenvectors_ss = np.linalg.eig(spin_spin_matrix)

# Print the results
print("\nEigenvalues(ss):")
print(eigenvalues_ss)
print("\nEigenvectors(ss) (columns correspond to eigenvalues):")
print(eigenvectors_ss)


def Index_direction(eigenvectors,projection_vector = np.array([0, 0, 1])):
   #this will return the vector that have largest projection on the projection vector;
   #use it too choose the direction that closest to z direction; 
   # Compute projections of the eigenvectors' columns on [0, 0, 1]
   projections = []
   # Compute the projection for each eigenvector
   for col in eigenvectors.T:
       projection = np.dot(col, projection_vector)  # Dot product
       projections.append(projection)

   # Find the index of the eigenvector with the largest projection
   largest_projection_index = np.argmax(np.abs(projections))  # Use absolute value to handle negative projections
#   print(f"largest projection value:{projections[largest_projection_index]}, index={largest_projection_index}")
   print(largest_projection_index)
   return largest_projection_index

#Find D E total:
print("=============TOTAL================")
eigenvectors = eigenvectors_raw
eigenvalues = eigenvalues_raw
#now choose the Dz, here we will choose the direction closest to 0,0,1 as dz
print("define position of z as closest along Z (raw matrix)")
index_z = Index_direction(eigenvectors, projection_vector=ref_z_direction)
index_x = Index_direction(eigenvectors, projection_vector=ref_x_direction)
index_y = Index_direction(eigenvectors, projection_vector=ref_y_direction)
print(f"Dz={eigenvalues[index_z]}, vector:{eigenvectors.T[index_z]}")
print(f"Dx={eigenvalues[index_x]}, vector:{eigenvectors.T[index_x]}")
print(f"Dy={eigenvalues[index_y]}, vector:{eigenvectors.T[index_y]}")

#find the D and E for raw matrix:
print("Total D and E are: ")
Dz = eigenvalues[index_z]
Dx = eigenvalues[index_x]
Dy = eigenvalues[index_y]

#Dz=-19.588768; Dx=-19.630382;Dy=-19.664784
Dtot=Dz-1/2*(Dx+Dy)
Etot=1/2*(Dy-Dx)
# cm-1 to GHz
cm_to_GHz = 29.9702547

print("cm-1: D,E=",Dtot,Etot)
print("GHz: D,E=",Dtot*cm_to_GHz,Etot*cm_to_GHz)


#find D and E for Spin-Spin matrix:
print("==============SPIN-SPIN==============")
eigenvectors = eigenvectors_ss
eigenvalues = eigenvalues_ss
#now choose the Dz, here we will choose the direction closest to 0,0,1 as dz
print("define position of z as closest along Z (raw matrix)")
index_z = Index_direction(eigenvectors, projection_vector=ref_z_direction)
index_x = Index_direction(eigenvectors, projection_vector=ref_x_direction)
index_y = Index_direction(eigenvectors, projection_vector=ref_y_direction)
print(f"Dz={eigenvalues[index_z]}, vector:{eigenvectors.T[index_z]}")
print(f"Dx={eigenvalues[index_x]}, vector:{eigenvectors.T[index_x]}")
print(f"Dy={eigenvalues[index_y]}, vector:{eigenvectors.T[index_y]}")

#find the D and E for raw matrix:
print("Total D and E are: ")
Dz = eigenvalues[index_z]
Dx = eigenvalues[index_x]
Dy = eigenvalues[index_y]

#Dz=-19.588768; Dx=-19.630382;Dy=-19.664784
Dss=Dz-1/2*(Dx+Dy)
Ess=1/2*(Dy-Dx)
# cm-1 to GHz
cm_to_GHz = 29.9702547

print("cm-1: D,E=",Dss,Ess)
print("GHz: D,E=",Dss*cm_to_GHz,Ess*cm_to_GHz)


#SOC part:
print("=============Spin-Orbit============")
print("Spin-Orbit part = Dtot-Dss")
Dsoc = Dtot-Dss; Esoc = Etot-Ess
print("GHz: D,E=",(Dtot-Dss)*cm_to_GHz,(Etot-Ess)*cm_to_GHz)


All_D = [Dss, Ess, Dsoc, Esoc, Dtot, Etot]
All_D_GHz = [d*cm_to_GHz for d in All_D]
with open('myzfs.txt','w') as out:
   out.write('#Dss  Ess  Dsoc  Esoc  Dtot  Etot\n')
   out.write("{:<10.6f} {:<10.6f} {:<10.6f} {:<10.6f} {:<10.6f} {:<10.6f}".format(*All_D_GHz))
