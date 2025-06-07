#!/bin/bash
#SBATCH --nodes=6               # Number of nodes
#SBATCH --ntasks-per-node=4     # Number of MPI ranks per node
#SBATCH --cpus-per-task=8       # number of  threads per task
#SBATCH --gpus-per-node=4             # Number of requested gpus per node
##SBATCH --exclusive             # Number of requested gpus per node
##SBATCH --mem=230000MB          # Memory per node
#SBATCH --time 22:59:59         # Walltime, format: HH:MM:SS
#SBATCH --partition=boost_usr_prod
#SBATCH --account=CNHPC_1457049 

#SBATCH -J "FF Au25AcCys18"



module use /home/cinprod/spack/02/modules/BA/0.19/
module load spack
#module load quantum-espresso/7.2rc_local--openmpi--4.1.4--nvhpc--23.1-cuda-11.8.0-2gq
#module load quantum-espresso/7.2rc_local--openmpi--4.1.4--nvhpc--23.1-cuda-11.8.0-jlt

module load profile/lifesc
module load gromacs/2022.3--openmpi--4.1.6--gcc--12.2.0-cuda-12.1
####Minimization
gmx grompp -f minim.mdp -c 1AKI_solv_ions.gro  -p topol.top -o em.tpr -maxwarn 2
gmx_mpi mdrun -v -deffnm em

####Calibration NVT
gmx_mpi grompp -f nvt.mdp  -c em.gro -r em.gro -p topol.top  -n index.ndx  -o nvt.tpr  -maxwarn 1
mpirun -np

####Calibration NPT
gmx_mpi grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr
mpirun -np


##### Molecular dynamics
gmx_mpi grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top  -o md_0_1.tpr
mpirun -np 4 gmx_mpi mdrun -deffnm md_0_1



#To restart simulations
mpirun -np 4 gmx_mpi mdrun -deffnm md_0_1 -cpi md_0_1.cpt



