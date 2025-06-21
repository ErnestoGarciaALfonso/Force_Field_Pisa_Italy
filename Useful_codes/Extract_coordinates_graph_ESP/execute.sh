#!/bin/bash


file="esp.log"
esp_file="molecule.dat"


#rm $esp_file

espgen -i $file -o $esp_file -f 1

python extract_coordinates_from_log.py esp.log

python graph.py
