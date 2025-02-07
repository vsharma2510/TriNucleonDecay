import os
import sys
import Config_ReadySubmission

FileNameDelimeterKeyVal = Config_ReadySubmission.FileNameDelimeterKeyVal
FileNameDelimeterPropPair = Config_ReadySubmission.FileNameDelimeterPropPair

args = sys.argv[1:]
ListFilePath = os.path.realpath( args[0] )

ListFileDir  = '/'.join( ListFilePath.split('/')[:-1] )
SingleRunDir = '/'.join( ListFileDir.split('/')[:-1] )

ListFileName = ListFilePath.split('/')[-1]

OutFileName  = ''
OutFileName += ListFileName.split('.')[0] #remove the .list to start us off
OutFileName += FileNameDelimeterPropPair + 'Coincidence' + FileNameDelimeterKeyVal + Config_ReadySubmission.Coincidence
OutFileName += FileNameDelimeterPropPair + 'Validation' + FileNameDelimeterKeyVal + Config_ReadySubmission.Validation
OutFileName += '.root'


OutFilePath = SingleRunDir + '/output/' + OutFileName

print (OutFilePath)

