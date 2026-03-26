#!/bin/bash

# Input file
input_file="casscf.out"

# Extract part between "---- THE CAS-SCF GRADIENT HAS CONVERGED ----" and "LOEWDIN ORBITAL-COMPOSITIONS"
awk '/---- THE CAS-SCF GRADIENT HAS CONVERGED ----/,/LOEWDIN ORBITAL-COMPOSITIONS/' "$input_file" > casscf_results.txt

# Extract part between "NONZERO SOC MATRIX ELEMENTS (cm**-1)" and "Note"
awk '/NONZERO SOC MATRIX ELEMENTS \(cm\*\*-1\)/,/Note/' "$input_file" > SOC_result.txt

echo "Extraction complete!"

