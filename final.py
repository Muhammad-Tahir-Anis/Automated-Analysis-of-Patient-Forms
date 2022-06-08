#Importing the Libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def label(value):
    #Import the dataset
    dataset = pd.read_csv('trainig/Child.csv')
    X_test1= pd.read_csv('Images/Data.csv')

    #split the dataset into X AND Y
    X = dataset.iloc[:,:-1].values
    Y = dataset.iloc[:,-1].values



    #Feature Scalling because we want to definate range
    # from sklearn.preprocessing import StandardScaler
    # sc_X=StandardScaler()
    # X=sc_X.fit_transform(X)

    # # # Label encoding
    # from sklearn.preprocessing import LabelEncoder
    # le = LabelEncoder()
    # Y=le.fit_transform(Y)
    # #///Here we split the data set into training and test set
    from sklearn.model_selection import train_test_split
    X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.3, random_state=0)



    # //////////////////FINAL//////////////////////////
    #make a prediction with an RFE pipeline
    from numpy import std
    from sklearn.feature_selection import RFE
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.pipeline import Pipeline


    from sklearn.metrics import confusion_matrix,accuracy_score
    # create pipeline
    rfe = RFE(estimator=DecisionTreeClassifier(), n_features_to_select=10)
    model = DecisionTreeClassifier(criterion='entropy',random_state=0)
    model1=model.fit(X_train,Y_train)

    pipeline = Pipeline(steps=[('s',rfe),('m',model)])
    # fit the model on all available data
    pipeline.fit(X, Y)
    # make a prediction

    y_pred_1 = pipeline.predict(X_test)
    print(X_test)
    #Nichy wali line correct ha
    y_pred_2 = pipeline.predict(X_test1)
    print(X_test1)
    #y_predd = pipeline.predict(X[:165,:])
    print(y_pred_2)
    score2=accuracy_score(Y_test,y_pred_1)
    print('Accuracy of Model With Feature Reduction : %.2f' % (score2*100))
    value = y_pred_2
    # # /////////////////////////////////////////////////////////