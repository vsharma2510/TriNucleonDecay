#https://docs.google.com/presentation/d/1J7jtHiCKXbNi-XQnE9GYgGcJROSD20DFthF1nrJ12e0/

import sys

import numpy as np
import os
#-------------------------------------------------------------------------------
import Config_ReadySubmission
import Library_FileReadAsText
import Library_FileWriteText
import Library_SystemDirectoryCreateSafe
import Library_DateStringNowGMT
import Library_CopyTemplate
#-------------------------------------------------------------------------------

#Config Loading
#   Obtain the full list of datasets for which we need to prepare condor to run:
#       Note dataset names used to be extracted via commandline with argv:
#           command line args extracted from:   sys.argv
#       Instead using a config file 'Config_ReadySubmission.py' which user can easily modify
#       TODO: think about making this config in json format for future maintenance
DatasetsOfInterest  = Config_ReadySubmission.DatasetsOfInterest
RunTypesOfInterest  = Config_ReadySubmission.RunTypesOfInterest


MultiplicityLow     = Config_ReadySubmission.MultiplicityLow
MultiplicityHigh    = Config_ReadySubmission.MultiplicityHigh
Coincidence         = Config_ReadySubmission.Coincidence
Validation          = Config_ReadySubmission.Validation


#-------------------------------------------------------------------------------
#Directory management:



#Load up all the static directories which are consistent for multiple runs of the data extractor
DirectoryCodeParent          = os.path.realpath( '../')
DirectoryMainCode            = os.getcwd()
DirectoryDatasetInformation  = DirectoryCodeParent + '/DatasetInformation'

#Create all the directories required for a single condor run:
DirectorySingleRun           = DirectoryCodeParent + '/CondorRuns/' + Library_DateStringNowGMT.Main()
DirectorySingleRunCode       = DirectorySingleRun  + '/SingleRunCode'  #where 1 time code lives
DirectoryLists               = DirectorySingleRun  + '/lists'       #where we map data&run to all 19 towers
DirectoryOutput              = DirectorySingleRun  + '/output'      #where output files get dumped from the run
DirectoryLogs                = DirectorySingleRun  + '/logs'      #where output files get dumped from the run

Library_SystemDirectoryCreateSafe.Main(DirectorySingleRun)
Library_SystemDirectoryCreateSafe.Main(DirectorySingleRunCode)
Library_SystemDirectoryCreateSafe.Main(DirectoryLists)
Library_SystemDirectoryCreateSafe.Main(DirectoryOutput)
Library_SystemDirectoryCreateSafe.Main(DirectoryLogs)

FileNameDelimeterKeyVal = Config_ReadySubmission.FileNameDelimeterKeyVal
FileNameDelimeterPropPair = Config_ReadySubmission.FileNameDelimeterPropPair
#-------------------------------------------------------------------------------
#MAKE LIST FILES:
DataLevelString = None
if not ( 'None' in [MultiplicityLow, MultiplicityHigh, Coincidence, Validation] ): 
    DataLevelString = 'FinalizedReduced'
else:
    DataLevelString = 'Production'

#Iterate through each dataset & run combo
for DatasetNumber in DatasetsOfInterest:
    DatasetNumberString = str(DatasetNumber)
    DatasetInformationFilePath = DirectoryDatasetInformation+'/ds' +DatasetNumberString+".dat"
    DatasetInformationFileText = Library_FileReadAsText.Main( DatasetInformationFilePath )
    DatasetInformationFileLines = DatasetInformationFileText.split('\n')

    #Read through the dataset information file line by line to obtain the run number:
    #   Skip first 2 lines because they are column labels which look like:
    #       Dataset | Run | Run Type | Start Time | Stop Time | Run Time | Stop Status
    for DatasetInformationFileLine in DatasetInformationFileLines[2:]: 
        if DatasetInformationFileLine != '':
            RunNumberString = DatasetInformationFileLine.split('|')[1].strip() #trim whitespace
            RunTypeString   = DatasetInformationFileLine.split('|')[2].strip()

            if RunTypeString in RunTypesOfInterest: 
                FilePathListTemplate = DirectoryMainCode + '/Config_TemplateList.list'
                FilePathListTarget   = DirectoryLists + '/Dataset'+FileNameDelimeterKeyVal +DatasetNumberString+FileNameDelimeterPropPair + 'RunNumber'+FileNameDelimeterKeyVal+RunNumberString+'.list'
                ReplacementDictionaryTemplateList = {
                    'DATASETNUMBER' : DatasetNumberString,
                    'RUNNUMBER'     : RunNumberString,
                    'DATALEVEL'     : DataLevelString,
                    }
                Library_CopyTemplate.Main(
                    SourceFilepath = FilePathListTemplate,
                    TargetFilepath = FilePathListTarget,
                    ReplacementDictionary = ReplacementDictionaryTemplateList,
                    )

#Generate a condor submitter script
Library_CopyTemplate.Main(
    SourceFilepath = DirectoryMainCode + '/Config_TemplateSubmitter.condor',
    TargetFilepath = DirectorySingleRunCode + '/submitter.condor',
    ReplacementDictionary = {
        'DIRECTORYLOGS'  : DirectoryLogs,
        'DIRECTORYLISTS' : DirectoryLists,
        } ,
    )


#Generate the C/Root Macro script & deduce which one we need based upon config choices
if not ( 'None' in [MultiplicityLow, MultiplicityHigh, Coincidence, Validation] ):
    Library_CopyTemplate.Main(
        SourceFilepath = DirectoryMainCode + '/Library_TemplateMakeReducedMultiplicityFiles.C',
        TargetFilepath = DirectorySingleRunCode + '/MakeEventFiles.C',
        ReplacementDictionary = {
            'MULTIPLICITYLOW' : str(MultiplicityLow),
            'MULTIPLICITYHIGH': str(MultiplicityHigh),
            },
        )
else:
    Library_CopyTemplate.Main(
        SourceFilepath = DirectoryMainCode + '/Library_TemplateMakeSinglePhysicsEventFiles.C',
        TargetFilepath = DirectorySingleRunCode + '/MakeEventFiles.C',
        )


#Generate the start job script (the .sh file which invokes the C Macro) 
#   FIXME/TODO: 
#       All startjob.sh scripts could be merged into a single one 
#       These possibilities could be merged if all C Macros share same args 
#       (even if many args are unused by each C macro)
#       The problem will be passing None args as strings.
#       Probably have to change missing config defaults to null strings like: ''
#   
#       TLDR; This block feels like bad & redundant code
if not ( 'None' in [MultiplicityLow, MultiplicityHigh, Coincidence, Validation] ):
    Library_CopyTemplate.Main(
        SourceFilepath = DirectoryMainCode + '/' + 'Process_TemplateStartJobReducedMultiplicityFiles.sh',
        TargetFilepath = DirectorySingleRunCode + '/' +  'Process_StartJob.sh',
        )
else:
    Library_CopyTemplate.Main(
        SourceFilepath = DirectoryMainCode + '/' + 'Process_TemplateStartJobSinglePhysicsEventFiles.sh',
        TargetFilepath = DirectorySingleRunCode + '/' +  'Process_StartJob.sh',
        )



#Copy over any other unchanged dependency code files which need no modifications 
FileNamesUnchangedCodeRequired = [
    'Config_ReadySubmission.py',
    'Process_ListFilePathToOutFilePath.py',
    'Process_ListFilePathToCoincidenceString.py',
    'Process_ListFilePathToValidationString.py',
    ]

for SingleFileName in FileNamesUnchangedCodeRequired:
    Library_CopyTemplate.Main(
        SourceFilepath = DirectoryMainCode + '/' + SingleFileName,
        TargetFilepath = DirectorySingleRunCode + '/' + SingleFileName,
        )


















