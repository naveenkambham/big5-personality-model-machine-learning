"""
Developer : Naveen Kambham
Description: Code to find campus arrival time, campus departure time, time spent in campus, number  of  unique WiFi routers visited
around the city for each day using  the  known  MAC  addresses of University  and  geographic  coordinates  for  each  campus  WiFirouter.
"""
#Importing the required libraries.

import numpy as np
import pandas as pd

import FeatureExtraction.CommonFunctions.dataprocessing_helper as dataprocessor


def CountDistinctStrings(list):
    return np.count_nonzero(np.unique(list))

def get_campus_entry_leave_times(file):
    """
    method to find the campus entry time, leave time and time on campus
    First time in a day a phone sees a campus router is entry time of the participant/phone and
    last time is leave time. Difference of these two gives time spent on campus.
    :param file:
    :return:
    """
    #Read the data in to data frame
    df = pd.read_csv(file)


    #consider only university wifi router address records and split the record_time in to date and time
    df_with_UofS_Wifi = df.loc[df.ssid.isin(['uofs-secure','uofs-public','uofs-guest'])]
    df_with_UofS_Wifi['Date'],df_with_UofS_Wifi['Time'] = zip(*df_with_UofS_Wifi['record_time'].map(lambda x:x.split(' ')))

    #Group by Id, Date
    grouped= df_with_UofS_Wifi.groupby(['user_id','Date'])


    #From the aggreagation get the min, max times i.e campues entry, leave times
    lst_campus_entry_leaving_timings = [(key[0],key[1], min(value['Time']), max(value['Time'])) for (key, value) in grouped.__iter__()]

    # create data frame out of three features.
    df = pd.DataFrame(lst_campus_entry_leaving_timings, columns=['ID','Date', 'EntryTime','LeavingTime'])
    df['Time_In_School']= df['EntryTime'] - df['LeavingTime']

    return df

def get_diff_wifi_seen(file):
    """
    method to find the different routers a phone seen throguh wifi sensors. Here routers with out hand-shake-connection
    are also recorded by the wifi sensor
    :param file:
    :return df:
    """

    #read the data in to df and split the record_time in to Date and Time
    df = pd.read_csv(file)
    df['ssid']= df['ssid'].astype(str)
    df['record_time']= df['record_time'].astype(str)
    df['Date'],df['Time'] = zip(*df['record_time'].map(lambda x:x.split(' ')))

    #Group by Id, Date
    grouped= df.groupby(['user_id','Date'])


    #count distinct wifi strings
    lst_wifi_routers_visited_daily = [(key[0],key[1],CountDistinctStrings(value['ssid'])) for (key, value) in grouped.__iter__()]
    df_wifis_seen = pd.DataFrame(lst_wifi_routers_visited_daily, columns=['ID','Date','WifiCountPerDay'])

    return df_wifis_seen



def extract(path):

    #extracting campus entry leave times, time in school and different wifi router seen in city
    df_campus_entry_leave_times=get_campus_entry_leave_times(path)
    df_diff_wifi_seen= get_diff_wifi_seen(path)


    #merging the data frames
    df_wifi_features= dataprocessor.merge([df_campus_entry_leave_times, df_diff_wifi_seen], ['ID', 'Date'])
    return df_wifi_features




#stand alone code to test the data
# df_wifi =main(r"/home/naveen/Data/Shed10/wifi.csv")
# print(len(df_wifi))
