#!/bin/bash
#SBATCH --output slurm-%j.out
#SBATCH --ntasks-per-node=128
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1G
#SBATCH --partition=normal_q
#SBATCH --time=1:00:00
#SBATCH --account=tdonnell_lab
if [ -z ${HOME+x} ]; then
    export HOME=$(echo ~)
    source /etc/profile
    source /etc/bashrc
    source $HOME/.bashrc
fi

#Execute job steps
numtasks=128
for ((i=0;i<numtasks;i++)) 
do
    index=$i
    /home/vivek9/TriProtonDecay/Simulation/JobScripts/pionSim_qshields.sh $index >/home/vivek9/TriProtonDecay/Simulation/JobScripts/Output/pionSim_qshields_$index.out &>/home/vivek9/TriProtonDecay/Simulation/JobScripts/Error/pionSim_qshields_$index.err &
done
wait
