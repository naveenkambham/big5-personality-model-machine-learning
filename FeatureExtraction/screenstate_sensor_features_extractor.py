"""
Developer : Naveen Kambham
Description: Code to find the daily(active) smartphone usage feature from Smartphone Screen Sensor data.
Continuous screen ON and OFF states in a single day are caliculated and
collectively these gave us the active mobile duration of each participant in a day.
"""

#Importing the required libraries.
import pandas as pd
from FeatureExtraction.CommonFunctions import converters as converters


def get_activephone_usage(file):
    """
    method to find the activie phone usage of participants
    :param file path:
    :return dataframe:
    """

    #read the data in to dataframe
    df= pd.read_csv(file)


    #split the time record in to date and time. convert the values for easy math
    df['Date'],df['Time'] = zip(*df['record_time'].map(lambda x:x.split(' ')))
    df['ConvertedTime'] = df['Time'].apply(converters.ConvertTime)

    #Loop through each user.
    #Since this depends on continous data records we need to iterate the records aggregation doesn't help much
    userIds= df.user_id.unique()
    outputlist=[]
    for user in userIds:
        tempdf = df.loc[df.user_id == user]
        dates = tempdf.Date.unique()

        #looping through each day
        for date in dates:
            tmpdf = tempdf.loc[((df.Date == date))]
            tmpdf= tmpdf.sort_values(['ConvertedTime'],ascending=(True))
            tmpdf = tmpdf.reset_index(drop=False)

            #dictionary to store the sum of continous time value counts in a give day
            dict_screenstates={}
            dict_screenstates[1]=0
            dict_screenstates[0]=0
            for index,value in tmpdf.iterrows():

               if (index < len(tmpdf)-1):

                   #if the next state is not same as current state then compute the time otherwise skip
                   if (tmpdf.loc[index,'state'] != tmpdf.loc[index+1,'state']):
                       dict_screenstates[tmpdf.loc[index,'state']] +=  tmpdf.loc[index+1,'ConvertedTime'] - tmpdf.loc[index,'ConvertedTime']
                   else:
                       continue

            #append the data record for each user and each day
            outputlist.append([user,date,dict_screenstates[0],dict_screenstates[1]])



    output_dataFrame = pd.DataFrame(outputlist,columns=['ID','Date','ScreenState_ON','ScreenState_OFF',])

    return output_dataFrame



def extract(path):
    """
    method to extract the features from smartphone sensor data
    """
    return get_activephone_usage(path)


#stand alone code to test
# pd.set_option('display.max_rows', 5000)
# print(main(r'/home/naveen/Data/Shed9/Filtered/screenstate.csv'))
