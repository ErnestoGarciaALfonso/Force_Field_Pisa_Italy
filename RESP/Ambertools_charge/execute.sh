#!/bin/bash


# OJO: conda activate acpype in your window bash

file="full_esp_2_45.log"
esp_file="molecule.dat"


#rm $esp_file

#espgen -i $file -o $esp_file -f 1

echo "ESP extracted: done"

# see options with respgen -h, this commadn is useful to get the input files 
#respgen  -i $esp_file -o 1st.in -f resp1 -e 2 

#see Amber23.pdf page 360/1005
resp -O \
        -i 1st.in \
        -o 1st.out \
        -e $esp_file\
        -s 1st.esp \
        -t 1st.chg       
    
    # To check the total charge obtained
awk '{ for(i=1; i<=NF; i++) sum+=$i } END { print sum }' 1st.chg
    
#respgen  -i $esp_file -o 2nd.in -f resp2 -e 1 -n 1

resp -O \
        -i 2nd.in \
        -o 2nd.out \
        -e $esp_file \
        -s 2nd.esp \
        -t 2nd.chg \
        -q 1st.chg          

# To check the total charge obtained
awk '{ for(i=1; i<=NF; i++) sum+=$i } END { print sum }' 2nd.chg



