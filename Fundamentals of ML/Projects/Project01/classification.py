# -*- coding: utf-8 -*-
"""
File:   classification.py
Author: ml-is-fun 
Date:   13 Dec 2018
Desc:   classify characters/images based on features extracted 
        using k-Nearest Neighbor algorithm   
    
"""

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.externals import joblib

def classification(k,train,train_labels,test,distance_metric):
    
    #kNN Classifier
    knn = KNeighborsClassifier(n_neighbors=k,metric=distance_metric)

    #fitting the model
    knn.fit(train, train_labels)

    #save model to use for testing 
    joblib.dump(knn,'knn_model.joblib')
    
    #predict the response
    pred = knn.predict(test) 
    
    return pred;

