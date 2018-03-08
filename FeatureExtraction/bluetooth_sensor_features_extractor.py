"""
Developer : Naveen Kambham
Description: Using the Bluetooth sensor Data, number of contacts a participant made with other individuals is caliculated
"""
#Importing the required libraries.

import pandas as pd
import numpy as np


#method to count the distinct strings in a list
def CountDistinctStrings(list):
    return np.count_nonzero(np.unique(list))

def find_contactrate_perday(file):
    """
    This method finds the number of contacts a person made with other people using bluetooth sensor data
    :param file:
    :return df:
    """


    #reading the data in to data frame
    df= pd.read_csv(file)

    #bluetooth can be connected to any type of devices such as printer, computer, smartphones etc. But we need
    # only smartphones as it is carried by participants
    smartphone_class_Id_List=['01020c','50020c','52020c','58020c','5a020c','62020c','70020c','72020c','78020c','7a020c']
    df_smartPhones = df.loc[df.dev_class.isin(smartphone_class_Id_List)]

    #of all smartphones bluetooth sensed take the nearby smartphones only based on signla strength
    df_nearby_smartphones= df_smartPhones[df_smartPhones.rssi > -80 ]
    df_nearby_smartphones['Date'],df_nearby_smartphones['Time'] = zip(*df_nearby_smartphones['record_time'].map(lambda x:x.split(' ')))

    #Grouping By ID, Date so that we can get for each individual on a given day
    grouped = df_nearby_smartphones.groupby(['user_id','Date'])

    #get contact rate each day by counting the nearby smartphones
    ContactRateDailyList=[(key[0],key[1],CountDistinctStrings(value['mac'])) for (key,value) in grouped.__iter__()]
    outputdf= pd.DataFrame(ContactRateDailyList,columns=['ID','Date','ContactRatePerDay'])
    return outputdf


def extract(path):
    return find_contactrate_perday(path)
