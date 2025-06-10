#!/bin/bash


filename="coordinates_DFT"
output_file="test.txt"


awk '{print $2"   "$3"   "$4}' $filename > $output_file
