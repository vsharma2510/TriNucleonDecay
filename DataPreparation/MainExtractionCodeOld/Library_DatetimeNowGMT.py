"""
SOURCE:
    Mind of Douglas Adams
    https://stackoverflow.com/questions/67234984/python-get-current-utc-time-ignore-computer-clock-always/67235150
DESCRIPTION:
    Get the current datetime in UTC. 
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
    DummyArg
        Type:
            <class 'NoneType'>
        Description:
            None
RETURNS:
    Result
        Type:
        Description:
"""
#import ntplib
import datetime
#from datetime import datetime, timezone

#-------------------------------------------------------------------------------
def Main(
    AvoidComputerClock= None,
    CheckArguments = True,
    PrintExtra = False,
    ):

    Result = None

    if AvoidComputerClock == None:
        AvoidComputerClock = False

    if (CheckArguments):
        ArgumentErrorMessage = ""

        if (len(ArgumentErrorMessage) > 0 ):
            if(PrintExtra):
                print("ArgumentErrorMessage:\n", ArgumentErrorMessage)
            raise Exception(ArgumentErrorMessage)


    if AvoidComputerClock:
        #print ('WARNING - Using Internet To Get UTC Datetime')
        #client = ntplib.NTPClient()
        #response = client.request('europe.pool.ntp.org', version=3)
        #Result = datetime.datetime.fromtimestamp(response.tx_time, tz=datetime.timezone.utc)        
        raise Exception('not preprared to use ntplib')

    else:
        #Result = datetime.datetime.now(datetime.timezone.utc) #FIXME: Get this working in python2
        Result = datetime.datetime.utcnow(  )

    

    return Result 
















