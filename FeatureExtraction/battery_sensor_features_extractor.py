"""
Developer : Naveen Kambham
Description:  Based on the Battery sensor Data, charger plug in time and duration of plug in time are extracted on a daily basis.
"""
#Importing the required libraries.
# Importing the required libraries.
import collections as col
import functools
from collections import Counter

import pandas as pd

import FeatureExtraction.CommonFunctions.converters as converters
from FeatureExtraction.CommonFunctions import dataprocessing_helper
# Importing the required libraries.
# Importing the required libraries.
import collections as col
import functools
from collections import Counter

import pandas as pd

import FeatureExtraction.CommonFunctions.converters as converters
from FeatureExtraction.CommonFunctions import dataprocessing_helper


def TakeMostProbableTimeInStudy(study_values,day_values):
    """
    Sometimes it is possible that partcipant can charge the mobile multipletimes in a day
    In such caseswe consider the most probable time of corresponding participant
    occurred in the entire study period.
    :param StudyValues:
    :param DayValues:
    :return:
    """

    #if total number of values in a day are one then return the only value i.e only one charger plugin time in a given day
    if day_values.count ==1 :
        return day_values

    #more than one time found, hence get the day values and the time values for entire study

    else:
        #get the study time and day values values count
        counter = Counter(study_values)
        return functools.reduce(lambda max_key,current_key: max_key if counter[max_key]>counter[current_key] else current_key, study_values)



def get_charger_plugintime_daily(file):
    """
    Method to compute the battery charger plug in time
    :param file:
    :return data frame:
    """

    #read the data in to a dataframe
    df= pd.read_csv(file)

    #splitting datetime in to date and time columns
    df['Date'], df['Time'] = zip(*df['start_time'].map(lambda x: x.split(' ')))

    #removing rows with battery plugged status as o which is unplugged and converting the time to Integer for easy caliculations
    df= df[df.plugged !=0]
    df['Time'] =df['Time'].apply(converters.ConvertTime)
    df['Time'] =df['Time'].apply(converters.ConvertToInt)


    #getting the all plug in times for a particular participant
    tempdf = df
    tempgrouping = tempdf.groupby(['user_id'])
    batterychargeTimePerStudy= [(key,col.Counter(converters.ConvertToIntList(value['Time']))) for (key, value) in tempgrouping.__iter__()]
    batterychargeTimePerStudydf= pd.DataFrame(batterychargeTimePerStudy,columns=['ID','Values'])

    #Group by Time and
    grouping = df.groupby(['user_id','Date'])

    #Get battery time for each day by taking the most probable time in the entire study if there are more than one recod
    batterychargeTime_perDay= [(key[0],key[1],TakeMostProbableTimeInStudy(batterychargeTimePerStudydf[batterychargeTimePerStudydf.ID ==key[0]],value['Time'])) for (key,value) in grouping.__iter__()]
    outputdf= pd.DataFrame(batterychargeTime_perDay,columns=['ID','Date','CharginTimeDaily'])

    return outputdf


def max_battery_plugin_time_daily(file):

    """
    computes the maximum plug in time of battery in a give day for all participants
    :param file:
    :return:
    """

    #read the data in to data fram
    df= pd.read_csv(file)


    #create new df columns for start,end date and time columns and convert the values in to integer for math advantages
    df['StartDate'],df['StartTime'] = zip(*df['start_time'].map(lambda x:x.split(' ')))
    df['ConvertedStartTime'] = df['StartTime'].apply(converters.ConvertTime)
    df['ConvertedStartDate'] = df['StartDate'].apply(converters.ConvertDate)
    df['EndDate'],df['EndTime'] = zip(*df['end_time'].map(lambda x:x.split(' ')))
    df['ConvertedEndTime'] = df['EndTime'].apply(converters.ConvertTime)
    df['ConvertedEndDate'] = df['EndDate'].apply(converters.ConvertDate)



    userIds= df.user_id.unique()
    outputlist=[]

    # Since this depends on continous data records we need to iterate the records simple aggregation doesn't help much
    #processing for corresponding participant
    for user in userIds:
        tempdf = df.loc[df.user_id == user]
        Dates = tempdf.StartDate.unique()

        #processing for each day
        for date in Dates:
            tmpdf = tempdf.loc[((df.StartDate == date))]
            tmpdf= tmpdf.sort_values(['ConvertedStartTime'],ascending=(True))
            tmpdf= tmpdf[tmpdf.plugged.isin([1,2])]
            durations =[0]

            for index,value in tmpdf.iterrows():
                if (tmpdf.loc[index,'StartDate'] == tmpdf.loc[index,'EndDate']):
                    durations.append(tmpdf.loc[index,'ConvertedEndTime'] - tmpdf.loc[index,'ConvertedStartTime'])
                else:
                    durations.append((24.0 - tmpdf.loc[index,'ConvertedStartTime']) + tmpdf.loc[index,'ConvertedEndTime'])

    output_dataFrame = pd.DataFrame(outputlist,columns=['ID','Date','Battery_Charging_Duration',])
    return output_dataFrame

def extract(path):

    #getting the daily charger plug in times in a day for each participants
    df_charge_plugin_times=get_charger_plugintime_daily(path)

    #getting the maximum charger plugin duration in a day for each participants
    df_max_plugin_duration=max_battery_plugin_time_daily(path)

    #merging the extracted features
    battery_df= dataprocessing_helper.merge([df_charge_plugin_times, df_max_plugin_duration], ['ID', 'Date'])


    return battery_df



#Code to test the functionality independently
# df_battery=extract(r"/home/naveen/Data/Shed10/Filtered/battery_events.csv")
# print((df_battery))
