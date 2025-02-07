"""

SOURCE:


    There is no time difference between Coordinated Universal Time and Greenwich Mean Time


DESCRIPTION:
    takes a native python datetime object, 
    and turns it into a 'Type_Datestring' object

    Result is always converted to ( GMT == UTC ) time zone

ARGS:
    Datetime -> python datetime object
    Timezone -> specifys the timezone associated with the datetime object provided 


RETURNS:
    Datestring
        Description: 
            looks like  'yyyy_mm_dd_hh_mm_ss_mmmmmm_tzn'
        Type:
            `Type_DateString`

TESTS:
    Test_DatetimeToDateString


"""

#import Library_DatetimeIsGMT
import Library_IntegerToStringPadWithZeros

def Main(
    Datetime = None, 
    Timezone = "NAN",
    DatetimeList = None,    
    ):
    Result = None
        
    if (Datetime is None and DatetimeList is None):
        raise Exception('Datetime cannot be null')

    if Datetime is not None:
        #if not Library_DatetimeIsGMT.Main( Datetime ): #FIXME: Not possible in python2
        #    raise Exception('FAIL: Datetime either not aware, or not GMT. Bad Idea. ')


        DateString = ""
        DateString += Library_IntegerToStringPadWithZeros.Main(Datetime.year,           4) + "_"
        DateString += Library_IntegerToStringPadWithZeros.Main(Datetime.month,          2) + "_"
        DateString += Library_IntegerToStringPadWithZeros.Main(Datetime.day,            2) + "_"
        DateString += Library_IntegerToStringPadWithZeros.Main(Datetime.hour,           2) + "_"
        DateString += Library_IntegerToStringPadWithZeros.Main(Datetime.minute,         2) + "_"
        DateString += Library_IntegerToStringPadWithZeros.Main(Datetime.second,         2) + "_"
        DateString += Library_IntegerToStringPadWithZeros.Main(Datetime.microsecond,    6) + "_" 
        DateString += Timezone
        Result = DateString



    elif DatetimeList is not None:
        DateStringList = []
        for SingleDatetime in DatetimeList:
            SingleDateString = Main(Datetime = SingleDatetime, Timezone = Timezone) 
            DateStringList.append( SingleDateString )
        Result = DateStringList
    return Result
    
    
    
    
    
    
    
    
    
    
