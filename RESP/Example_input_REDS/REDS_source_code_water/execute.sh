#!/bin/bash



# type "make" in your console to buil the executable resp 


#file=""
esp_file="esp_file"



#rm $esp_file

#espgen -i $file -o $esp_file -f 1

echo "ESP extracted: done"

# see options with respgen -h, this commadn is useful to get the input files 
#respgen  -i $esp_file -o 1st.in -f resp1 -e 2 


############################ Fit step 1
#see Amber23.pdf page 360/1005
./resp -O  -i 1st.in  -o 1st.out  -e $esp_file -s 1st.esp   -t 1st.chg      

############################ Fit step 2   
./resp -O -i 2nd.in -o 2nd.out  -e $esp_file -q 1st.chg -s 2nd.esp -t 2nd.chg   



