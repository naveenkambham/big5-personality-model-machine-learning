"""
Developer : Naveen Kambham
Description:  Random Forests Regression Model using Scikit. This generalizes the data and then apply cross validation
to evaluate it with RMSE as metric. Hyper parameters are tuned and set.
"""
#Importing the required libraries.
from sklearn.ensemble import RandomForestRegressor
import pandas
import numpy
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline
from math import sqrt
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import mean_squared_error
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler




def RandomForestsModel(trait,estimator,min_split,max_depth,max_feature):
    #reading the data and filling missing values
    df = pandas.read_csv(r'/home/naveen/Data/DataSet1.csv')
    df= df.fillna(value=0)

    #getting the dependent variables, independent variables
    X = df.loc[:,'mediaUsage':'Scheduling_OfficeTools_Weather']
    Y = df.loc[:,trait]

    #creating the model and pipeling along with scaler
    model = RandomForestRegressor(n_estimators=estimator,
                        min_samples_split=min_split,max_features=max_feature,criterion='mse',max_depth=max_depth)
    seed=7
    numpy.random.seed(seed)
    estimators = []
    estimators.append(('standardize', StandardScaler()))
    estimators.append(('RandomForest', model))
    pipeline = Pipeline(estimators)
    kfold = KFold(n_splits=4, random_state=seed)
    predicted = cross_val_predict(pipeline,X,Y,cv=kfold)


    #fit line for results and actual values
    fig, ax = plt.subplots()
    ax.scatter(Y,predicted, edgecolors=(0, 0, 0))
    ax.plot([0, 1], [0, 1], 'k--', lw=2)
    ax.set_xlabel('Actual Values (Big Five PreSurvey)')
    ax.set_ylabel('Predicted Values')
    plt.title("Random Forests - "+trait)
    plt.savefig('/home/naveen/Desktop/Plots1/'+trait+'.png')


    return (sqrt(mean_squared_error(Y,predicted))*100)





traits=['Openness','Conscientiousness','Extraversion','Agreeableness','Neuroticism']
for trait in traits:
    print(trait,RandomForestsModel(trait,20,50,20,5))
