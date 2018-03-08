"""
Developer : Naveen Kambham
Description:  Neural Networks Regression Model using Tensor Flow. This generalizes the data and then apply cross validation
to evaluate it with RMSE as metric. Hyper parameters are tuned and set.
"""
#Importing the required libraries.

import numpy
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from math import sqrt
from sklearn.model_selection import cross_val_predict
import os
from  matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error



#Enable the GPU and read data and fill null values
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = ""
dataframe = pandas.read_csv(r'/home/naveen/Documents/DataSet1_1.csv')
dataframe = dataframe.fillna(value=0)


def model():
    """
    method to create the input,output layers and the output layers with relu activation and adam optimer and mse as loss function
    :return:
    """
    model = Sequential()
    model.add(Dense(30, input_dim=13, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal'))
    model.compile(loss='mean_squared_error', optimizer='adam')

    return model

def NeuralNets(trait):

    #get the dependent and independent variables
    X = dataframe.loc[:,'mediaUsage':'Scheduling_OfficeTools_Weather'].values
    Y = dataframe.loc[:,trait].values


    #adding seed and standardizing the data
    seed=7
    numpy.random.seed(seed)
    estimators = []
    estimators.append(('standardize', StandardScaler()))
    estimators.append(('mlp', KerasRegressor(build_fn=model, nb_epoch=300, batch_size=50 , verbose=0)))



    #pipeline to run stadadization and model
    pipeline = Pipeline(estimators)
    kfold = KFold(n_splits=4, random_state=seed)


    predicted = cross_val_predict(pipeline,X,Y,cv=kfold)

    #Scatter Plot for results and actual values
    fig, ax = plt.subplots()
    ax.scatter(Y,predicted, edgecolors=(0, 0, 0))
    ax.plot([0, 1], [0, 1], 'k--', lw=2)
    ax.set_xlabel('Actual Values (Big Five PreSurvey)')
    ax.set_ylabel('Predicted Values')
    plt.title("Neural Networks - "+trait)
    # plt.show()# enable for debugging
    plt.savefig('/home/naveen/Desktop/Plots1/'+trait+'.png')


    return (sqrt(mean_squared_error(Y,predicted))*100)


#looping for each Big Five trait.
traits=['Openness','Conscientiousness','Extraversion','Agreeableness','Neuroticism']

for trait in traits:
    print(trait,NeuralNets(trait))
