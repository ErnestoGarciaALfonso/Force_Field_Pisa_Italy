#!/bin/bash


# OJO: conda activate acpype in your window bash

#file=""
esp_file="esp_wat.dat"


#rm $esp_file

#espgen -i $file -o $esp_file -f 1

echo "ESP extracted: done"

# see options with respgen -h, this commadn is useful to get the input files 
#respgen  -i $esp_file -o 1st.in -f resp1 -e 2 


############################ Fit step 1
#see Amber23.pdf page 360/1005
python py_resp.py -O  -i 1st.in  -o 1st.out   -ip  ../Pol/pGM-pol-2016-09-01 -e $esp_file -s 1st.esp   -t 1st.chg      


# To check the total charge obtained
awk '{sum += $1} END {printf "Total charge: %.4f\n", sum}' charges.txt


############################ Fit step 2   
python py_resp.py -O -i 2nd.in -o 2nd.out  -ip   ../Pol/pGM-pol-2016-09-01 -e $esp_file  -s 2nd.esp -t 2nd.chg -q 1st.chg  


# To check the total charge obtained
awk '{sum += $1} END {printf "Total charge: %.4f\n", sum}' charges.txt

python split_charges.py
