#!/bin/bash
source /opt/exp_software/cuore/bin/setup.sh
echo LD_LIBRARY_PATH: $LD_LIBRARY_PATH #<--- what is this?
which diana
which root



#$1 is .list filepath from condor submitter script:
ListFilePath="$(realpath $1)" 
echo list filepath: $ListFilePath

#Using knowledge of the list file figure out the single run code directory:
ListFolderPath="$(dirname $ListFilePath)"
DataExtractionSingleRunCodeDir="$(dirname $ListFolderPath)/SingleRunCode"
echo MainCodeDir : $DataExtractionSingleRunCodeDir


#Construct other args we need to for the C script to work:
OutFilePath="$(python $DataExtractionSingleRunCodeDir/Process_ListFilePathToOutFilePath.py $1)"
echo out filepath: $OutFilePath


#Print and run the C code script on a single .list file
command="root -b '$DataExtractionSingleRunCodeDir/MakeEventFiles.C(\"$ListFilePath\",\"$OutFilePath\")'"
echo ----Final Run Command:----
echo $command
echo --------------------------

eval $command


