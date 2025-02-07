#https://docs.google.com/presentation/d/1J7jtHiCKXbNi-XQnE9GYgGcJROSD20DFthF1nrJ12e0
#https://docs.google.com/presentation/d/1xLeYE8vg9CbZ6X43ahQiWzb5ll4L2cxoDRcedMz-sk4/
#Config_ReadySubmission.py


DatasetsOfInterest = [
    3601,
    #3602,
    #3603,
    #3604,
    #3605,
    #3606,
    #3607,
    #3608,
    #3609,
    #3610,
    #3611,
    #3612,
    #3613,
    #3614,
    #3615,
    ]

RunTypesOfInterest = [
    'Background',
    ]


#Optional args: Default None Strings Required
MultiplicityLow     = 'None'
MultiplicityHigh    = 'None'
Coincidence         = 'None'
Validation          = 'None'


#Optional args: User desired properties:
#MultiplicityLow = 1
#MultiplicityHigh = 30
#Coincidence = "FastCoincidence_40keV_5ms_0nu"
#Validation  = "MultipletValidation_40keV_5ms_0nu"


#Minor convienience parameters which do not change extraction behavior:
FileNameDelimeterKeyVal   = '-' #between key & value 
FileNameDelimeterPropPair = '&' #between keyvaluepair1 & keyvaluepair2
#   e.g. FileName = Key1 + FileNameDelimeterKeyVal + Value1 + FileNameDelimeterPropPair + Key2 + FileNameDelimeterKeyVal + Value2 + ...
#
#   Note1: uproot fails with filenames with ':'
#   Note2: condor fails with filenames with ','

