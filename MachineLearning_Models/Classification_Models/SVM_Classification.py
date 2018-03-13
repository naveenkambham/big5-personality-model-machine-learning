"""
Developer : Naveen Kambham
Description:  Classification Model based on Support Vector Machine using Scikit.
This generalizes the data and then apply cross validation to evaluate it.
Hyper parameters are tuned using GridsearchCV and set.
"""
#Importing the required libraries.
import numpy
import pandas
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_predict
from sklearn import svm
from sklearn.metrics import precision_score

#load the data and fill missing values
dataframe = pandas.read_csv(r'/home/naveen/Documents/DataSet1_1.csv')
dataframe = dataframe.fillna(value=0)



def Labelclasses(value):
    """
    Method to bin the value ranges. Since the trait value ranges are 0,1 dividing in to three bins
    """
    if value >=0 and value <=0.3:
        return 0
    elif value >0.3 and value <=0.6:
        return 1
    elif value >0.6 and value <=1:
        return 2
    

def SVCModel(trait):
    """
    method to model the continuos problem as classification problem using Support Vector Machines
    """

    #converting the continuous values in to bins and reading the input(X) and output(Y) features 
    dataframe[trait] = dataframe[trait].apply(Labelclasses)
    X = dataframe.loc[:,'mediaUsage':'Scheduling_OfficeTools_Weather'].values
    Y = dataframe.loc[:,trait].values

    # applying scaling and modelling in pipeline
    seed=7
    numpy.random.seed(seed)
    estimators = []
    estimators.append(('standardize', StandardScaler()))
    model = svm.SVC(kernel='rbf',C=0.8,gamma='auto')
    estimators.append(('mlp',model ))
    pipeline = Pipeline(estimators)
    
    #cross validation
    kfold = KFold(n_splits=4, random_state=seed)
    predicted = cross_val_predict(pipeline,X,Y,cv=kfold)
    
    #confusion matrix
    print(confusion_matrix(Y,predicted))

    #returning the accuracy
    return (precision_score(Y, predicted, average='macro'))

#modeling each Big Five trait.
traits=['Openness','Conscientiousness','Extraversion','Agreeableness','Neuroticism']

for trait in traits:
    print(trait,SVCModel(trait))



