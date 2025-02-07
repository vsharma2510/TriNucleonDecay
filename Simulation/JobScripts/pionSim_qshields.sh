#!/bin/bash
echo "START"
date
printenv
module reset
module load foss
module load X11
module load Python
module load CMake

printenv

source /projects/tdonnell_lab/group_soft/root/root_v6.23.01_install/bin/thisroot.sh
source /projects/tdonnell_lab/group_soft/geant4/geant4-install/11.0.2/bin/geant4.sh
source /projects/tdonnell_lab/group_soft/MC/setup/setup-g4-11.0.2.sh

random1=$RANDOM
random2=$RANDOM
random3=$RANDOM
echo "Random 1 is $random1"
echo "Random 2 is $random2"
echo "Random 3 is $random3"

random4=$(($random1*$random2 + $random3))
echo "Random 4 is $random4"

time qshields -N80 -i$random4 -U37 -ppi+,0 -q2700 -o r/home/vivek9/TriProtonDecay/Simulation/Output/test_pion_sim_2700MeV_V2_${1}.root

