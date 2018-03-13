"""
Developer : Naveen Kambham
Description:  code to test the whole feature extraction phase by plotting the distributions. This plots univariate and bivariate distributions.
Helpful for a quick assement of whole data set including input/output feature relations.
"""
#Importing the required libraries.
import unittest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from FeatureExtraction import battery_sensor_features_extractor


def test_BigFiveFeaturesPhase(file):
    """
    code to draw the visulations for extracted features and scatterplot matrix for input/output features
    :param file path:
    :return nothing:
    """

    #read the data in to a data frame
    dataframe = pd.read_csv(file)

    ###################### Univariate Analysis/plots ##################################
    #plotting a density plot with 3 plots in each row
    dataframe.plot(kind='density', subplots=True, layout=(5, 3), sharex=False, sharey=False)
    plt.savefig(r'density.png')
    
    # plotting a histogram plot with 3 plots in each row
    dataframe.plot(kind='hist', subplots=True, layout=(5, 3), sharex=False, sharey=False)
    plt.savefig(r'histogram.png')

    # plotting a area plot with 3 plots in each row
    dataframe.plot(kind='area', subplots=True, layout=(5, 3), sharex=False, sharey=False)
    plt.savefig(r'histogram.png')
    

    
    ################ Bivariate Analysis/plots #####################################
    #plotting scatter plot matrix for dependent and independent features
    #scatter plot for app usage
    xvars_appusage=["Camera, Maps, Internet apps","Scheduling, OfficeTools, Weather apps","Media apps usage","Other apps usage"]
    yvars=['Openness','Conscientiousness','Extraversion','Agreeableness','Neuroticism']

    xvars_entry_leavetimes = ['Charge start time', 'Battery charging duration', 'Campus entry time', 'Campus leaving time',
             'Time spent in campus']

    g = sns.pairplot(dataframe,x_vars=xvars_appusage,y_vars=yvars)
    g.savefig(r'scatterplot_appusage.png')

    #scatter plot for time related features
    g = sns.pairplot(dataframe, x_vars=xvars_entry_leavetimes, y_vars=yvars)
    g.savefig(r'scatterplot_entryleavetimes.png')
    print("Plots are saved please check for anomolies")
    



