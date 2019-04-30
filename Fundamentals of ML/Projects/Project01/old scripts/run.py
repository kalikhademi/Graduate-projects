# -*- coding: utf-8 -*-
"""
File:   run.py
Author: ml-is-fun 
Date:   13 Dec 2018
Desc:   Main file that calls all modules for executing entire code  
    
"""
import numpy as np
from classification import classification
from sklearn.model_selection import train_test_split


'''=======================================IMPORT IMAGE DATA=========================================='''


'''=======================================PRE-PROCESSING IMAGE DATA=========================================='''


'''=======================================DIAGONAL FEATURE EXTRACTION=========================================='''


'''=======================================CLASSIFYING HANDWRITTEN CHARACTERS=========================================='''
k = [1,3,5,7] #k values determined from reference for KNN - 
test_sizes = [0.5,0.4,0.3,0.2,0.1] #train-test splits determined from reference - 

for i in range(len(test_sizes)):
    X_train,X_test,y_train,y_test = train_test_split(train,train_labels,test_size=test_sizes[i])
    
    for j in range(len(k)):
        classification(k[j],X_train,y_train,X_test)
        
'''=======================================EVALUATION METRICS=========================================='''
