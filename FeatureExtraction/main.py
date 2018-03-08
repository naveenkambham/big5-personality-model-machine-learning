"""
Developer : Naveen Kambham
Description:  This file contains the code to drive the feature extraction step. This assumes that data is located at below mentioned folders
"""
import pandas as pd

import FeatureExtraction.CommonFunctions.dataprocessing_helper as dataprocessor
from FeatureExtraction.DataSet import DataSet
#Data Studies
DataFolders=["/home/naveen/Data/Shed8/Filtered/","/home/naveen/Data/Shed9/Filtered/","/home/naveen/Data/Shed10/Filtered/"]

for filepath in DataFolders:
    # dataprocessor.filter_data_on_complaince(filepath, 50)
    dataset=DataSet(filepath)
    dataset.extract_features()

    #merge the ground truth and input features
    presurvey = pd.read_csv(filepath+'/PreSurvey_Processed.csv')
    features=pd.read_csv(filepath+'/FeaturesExtraction.csv')
    df_data=dataprocessor.merge([features,presurvey],['ID'])
    df_data.to_csv(filepath+'/Final_DataSet.csv')







