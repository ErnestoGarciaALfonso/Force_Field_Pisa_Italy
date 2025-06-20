#!/bin/bash


# OJO: conda activate acpype in your window bash


antechamber -i Stapler.pdb -fi pdb -o organic.mol2 -fo mol2 -c bcc -nc -1 -m 1 -ek "qm_theory='PM6', grms_tol=0.0005, scfconv=1.d-8, ndiis_attempts=700,"


