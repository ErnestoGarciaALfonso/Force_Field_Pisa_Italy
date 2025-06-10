#!/bin/bash
#SBATCH --nodes=6               # Number of nodes
#SBATCH --ntasks-per-node=4     # Number of MPI ranks per node
#SBATCH --cpus-per-task=8       # number of  threads per task
#SBATCH --gpus-per-node=4             # Number of requested gpus per node
##SBATCH --exclusive             # Number of requested gpus per node
##SBATCH --mem=230000MB          # Memory per node
#SBATCH --time 2:59:59         # Walltime, format: HH:MM:SS
#SBATCH --partition=boost_usr_prod
#SBATCH --account=CNHPC_1491920 

#SBATCH -J "Au25AcCys18 test2"


#module purge
source /home/cinprod/spack_setup.sh
module use /home/cinprod/spack/02/modules/BA/0.19/
module load spack
#module load quantum-espresso/7.2rc_local--openmpi--4.1.4--nvhpc--23.1-cuda-11.8.0-2gq
#module load quantum-espresso/7.2rc_local--openmpi--4.1.4--nvhpc--23.1-cuda-11.8.0-jlt

module load profile/lifesc
module load gromacs/2022.3--openmpi--4.1.6--gcc--12.2.0-cuda-12.1

#minimization
#gmx_mpi grompp -f minim.mdp -c 1AKI_solv_ions.gro  -p topol.top -o em.tpr -maxwarn 2
# mpirun -np 4 gmx_mpi  mdrun -v -deffnm em

### NVT
# gmx_mpi make_ndx -f  em.gro -o index.ndx  
#2 | 3 |4
#5 & a ST
#name 13 ST_group
#5 & ! a ST
#q
#EOF
# gmx_mpi grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -n index.ndx -o nvt.tpr
mpirun -np 4 gmx_mpi mdrun -v -deffnm nvt


##### NPT

#******* gmx_mpi grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -n index.ndx -o npt.tpr -v
# mpirun -np 4 gmx_mpi mdrun -v -deffnm npt

##### MD
#**********gmx_mpi grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -n index.ndx -o md_0_1.tpr
#mpirun -np 4 gmx_mpi mdrun -deffnm md_0_1

#To restart
#mpirun -np 4 gmx_mpi mdrun -deffnm md_0_1 -cpi md_0_1.cpt
