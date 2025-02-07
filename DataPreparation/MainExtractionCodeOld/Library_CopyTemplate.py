"""
SOURCE:
    Mind of Douglas Adams
DESCRIPTION:

    Copies a file from a source filepath
    to a target filepath

ARGS:
    CheckArguments
        Type:
            python boolean
        Description:
            if true, checks the arguments with conditions written in the function
            if false, ignores those conditions
    PrintExtra
        Type:
            python integer
        Description:
            if greater than 0, prints addional information about the function
            if 0, function is expected to print nothing to console
            Additional Notes:
                The greater the number, the more output the function will print
                Most functions only use 0 or 1, but some can print more depending on the number
    Directory
        Type:
            <type 'NoneType'>
        Description:
RETURNS:
    Result
        Type:
        Description:
"""

import os
import copy
import Library_FileReadAsText
import Library_FileWriteText
def Main(
    SourceFilepath = None,
    TargetFilepath = None,
    ReplacementDictionary = None,

    CheckArguments = True,
    PrintExtra = False,
    ):

    Result = False

    if (CheckArguments):
        ArgumentErrorMessage = ""

        if (len(ArgumentErrorMessage) > 0 ):
            if(PrintExtra):
                print("ArgumentErrorMessage:\n", ArgumentErrorMessage)
            raise Exception(ArgumentErrorMessage)

    #Make an in memory deep copy of the template code
    TemplateFileContents = Library_FileReadAsText.Main( SourceFilepath )
    TargetFileContents = copy.deepcopy( TemplateFileContents )

    #For each key,vaue pair in dictionary do a replacement
    if not (ReplacementDictionary is None):
        for Key, Value in ReplacementDictionary.items():
            TargetFileContents = TargetFileContents.replace( Key, Value )

    #Write the results to file at the target location
    Result = Library_FileWriteText.Main( Filepath = TargetFilepath, WriteText = TargetFileContents, )

    #Finally return a result indicating success/failure
    return Result 















