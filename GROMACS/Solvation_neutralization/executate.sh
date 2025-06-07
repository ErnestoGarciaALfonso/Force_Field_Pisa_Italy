source /usr/local/gromacs/bin/GMXRC

rm  \#*
rm 1AKI_newbox.gro 1AKI_solv.gro


echo "Remove the SOL and Na in topol,top in case you are running a previous calculation"
read -p "Press [Enter] key to continue..."

# Copy NP.top to NP.itp and create a topol.top


echo "SOLVATION"
read -p "Press [Enter] key to continue..."

gmx editconf -f NP.gro -o 1AKI_newbox.gro -c -d 1.0 -bt cubic
gmx solvate -cp 1AKI_newbox.gro -cs spc216.gro -o 1AKI_solv.gro -p topol.top


#
echo "Adding Ions"
gmx grompp -f ions.mdp -c 1AKI_solv.gro -p topol.top -o ions.tpr -maxwarn 2


#### comment the systme and what is below in order to not repeat system


### Choose SOL to be replaced by Na atoms
gmx genion -s ions.tpr -o 1AKI_solv_ions.gro -p topol.top -pname NA -nname CL -neutral << EOF

7
EOF

echo "Minimization"
read -p "Press [Enter] key to continue..."
gmx grompp -f minim.mdp -c 1AKI_solv_ions.gro  -p topol.top -o em.tpr -maxwarn 2

read -p "run? Press [Enter] key to continue..."
gmx mdrun -v -deffnm em
