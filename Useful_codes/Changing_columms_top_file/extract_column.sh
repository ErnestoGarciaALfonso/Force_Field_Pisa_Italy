#!/bin/bash


filename="all_charges_Luca"
output_file="test.txt"


awk '{print $4}' $filename > $output_file
