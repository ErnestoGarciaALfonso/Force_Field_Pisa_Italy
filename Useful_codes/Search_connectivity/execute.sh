#!/bin/bash

FCOMPILER=ifort

#inp_file="full_esp_2_45_000.xyz"
inp_file="Au25_AcCys18_final.xyz"

ln -s -f $inp_file file.in

$FCOMPILER Conectivity.f90
./a.out 

# max_bond_distance = 2.7       # Adjust as needed
python mapping_connectivity.py


# Select which chain want to be formatted as input RESP
 python rearranging_RESP.py 
