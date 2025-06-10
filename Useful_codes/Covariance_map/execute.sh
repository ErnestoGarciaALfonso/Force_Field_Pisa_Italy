#!/bin/bash

FCompiler=ifort

$FCompiler istogramma.f90 -o histo
./histo <  traj_old.xvg >output   # Check the header-isto file


python covariance_map.py   < output 

