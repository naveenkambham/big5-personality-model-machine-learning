"""
Developer : Naveen Kambham
Description:  This file contains the code to drive the feature extraction step. This assumes that data is located at /home/naveen/Data/ folders
"""
import pandas as pd

import FeatureExtraction.CommonFunctions.dataprocessing_helper as dataprocessor
from FeatureExtraction.DataSet import DataSet
#Data Studies
DataFolders=["/home/naveen/Data/Shed8/Filtered/","/home/naveen/Data/Shed9/Filtered/","/home/naveen/Data/Shed10/Filtered/"]

for filepath in DataFolders:
    
    #load the data and extract the features from different smartphone sensors
    dataset=DataSet(filepath)
    dataset.extract_features()

    #merge the ground truth i.e Big Five Personality values and extracted input features
    presurvey = pd.read_csv(filepath+'/PreSurvey_Processed.csv')
    features=pd.read_csv(filepath+'/FeaturesExtraction.csv')
    df_data=dataprocessor.merge([features,presurvey],['ID'])
    df_data.to_csv(filepath+'/Final_DataSet.csv')







