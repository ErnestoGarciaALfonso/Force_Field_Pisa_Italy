#!/bin/bash


# OJO: conda activate acpype in your window bash

### Remove the Au atoms
antechamber -i Stapler_no_Au.pdb -fi pdb -o organic.mol2 -fo mol2 -c bcc -nc 0 -m 1 -ek "qm_theory='PM6', grms_tol=0.0005, scfconv=1.d-8, ndiis_attempts=700,"

#Then add the Au atoms in the output file in the proper format and the charge you whish
