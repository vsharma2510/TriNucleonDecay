"""
DESCRIPTION:

    Gets current time in format :
        `Type_Datestring` 
        == 
        'yyyy_mm_dd_hh_mm_ss_mmmmmm_GMT'
ARGS:
    NONE

RETURNS:
    Datetime == `Type_Datestring` == '<yyyy_mm_dd_hh_mm_ss_mmmmmm>_GMT'

"""


import Library_DatetimeToDateString
#import datetime
import Library_DatetimeNowGMT

def Main():
    #CurrentDatetime = Library_DatetimeNowGMT.Main() #FIXME: NOPE!

    CurrentDatetime = Library_DatetimeNowGMT.Main(  )
    DateString =  Library_DatetimeToDateString.Main(CurrentDatetime, "GMT")
    return DateString
