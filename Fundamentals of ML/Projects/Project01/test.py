#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File:   test.py
Author: ml-is-fun 
Date:   13 Dec 2018
Desc:   script to test data using models saved during training 
    
"""

import sys
import numpy as np
from sklearn.externals import joblib
from normalization import NormalizeImage
from findContours import createContours
from feature_extraction import featureExtraction


if __name__ == '__main__':
    
    if len(sys.argv) != 4:
        print('You need to input 4 arguments into the command line')
    
    '''=======================================IMPORT IMAGE DATA=========================================='''
    #passing data from command line 
    testData = np.load(sys.argv[1]) #sys.argv[1]
    #the file to print generated labels will be sys.argv[2]
    #the decision on which model will be sys.argv[3]
    #testLabels = np.load(sys.argv[2])

    '''=======================================PRE-PROCESSING IMAGE DATA=========================================='''
    for index in range(len(testData)):
        testData[index] = testData[index].astype(np.uint8)
    
    NormalizeImage(testData)
    Drawing_list = createContours(testData.shape[0],'Training_images')
    
    '''=======================================DIAGONAL FEATURE EXTRACTION=========================================='''
    features = featureExtraction(Drawing_list)
    
    '''=======================================PREDICTING HANDWRITTEN CHARACTERS=========================================='''
    #Condition for selecting model
    if sys.argv[3] == 'extra':
        knn = joblib.load('knn_model_extra.joblib')
    else:
        knn = joblib.load('knn_model.joblib')
    
    test_predictions = knn.predict(features)
    
    #write test predictions to argv[2]
    outfile = sys.argv[2] + '.npy'
    np.save(outfile,np.asarray(test_predictions))

