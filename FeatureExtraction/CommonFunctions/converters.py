"""
Developer : Naveen Kambham
Description:  This file contains the basic data convertes
"""
#Importing the required libraries.

def ConvertTime(Time):
    Times = Time.split(":")
    return int(Times[0])+((int)(Times[1])*(1/60))

def ConvertToIntList(Values):
    return Values.get_values()

def ConvertToInt(value):
    return int(value)

def ConvertDate(Date):
    Times = Date.split("-")
    return int(Times[1])*30+(int)(Times[2])

def ConvertPercent(number):
    number= str(number)
    number =number.split("%")
    if(len(number) >=1):
        return int(number[0])
    else:
        return int(number)
