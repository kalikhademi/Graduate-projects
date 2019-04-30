#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File:   train.py
Author: ml-is-fun 
Date:   13 Dec 2018
Desc:   script to train kNN model to determine hyper parameters to 
        test with   
    
"""

import numpy as np
import findContours as fc
import cv2
from normalization import NormalizeImage
from feature_extraction import featureExtraction
from classification import classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from confusion_matrix import plot_confusion_matrix

'''=======================================LOADING IMAGE DATA=========================================='''
trainData = np.load('ClassData_2.npy') #1655 shape
trainLabels = np.load('ClassLabels_1.npy') #lables for images
trainData_AB = [] #images of only A and B
trainLabels_AB = [] #labels only for images A and B


trainData_1 = np.load('extra_data.npy') #1655 shape
trainLabels_1 = np.load('extra_labels.npy') #lables for images
trainData_2 = np.load('extra_data_1.npy') #images of only A and B
trainLabels_2 = np.load('extra_labels_1.npy') #labels only for images A and B

combinedLabels = np.concatenate((trainLabels,trainLabels_1),axis=0)
combinedLabels = np.concatenate((combinedLabels,trainLabels_2),axis=0)

for index in range(len(trainData)):
    trainData[index] = trainData[index].astype(np.uint8)
    
    if ((trainLabels[index] == 1) or (trainLabels[index] == 2)):
        trainData_AB.append(trainData[index])
        trainLabels_AB.append(trainLabels[index])
        
trainData_AB = np.asarray(trainData_AB)
trainLabels_AB = np.asarray(trainLabels_AB)

for index in range(len(trainData_2)):
    trainData_2[index] = trainData_2[index].astype(np.uint8)     


trainData_1 = trainData_1.astype(np.uint8)

'''=========================================RESIZE AND SAVE AS BITMAP IMAGES========================================'''
NormalizeImage(trainData)
NormalizeImage(trainData_1)
NormalizeImage(trainData_2)

"""
NormalizeImage(trainData_AB)
"""

'''=========================================CONTOUR IMAGES========================================'''
Drawing_list = fc.createContours(trainData.shape[0],'Training_images')
features = featureExtraction(Drawing_list)

Drawing_list_1 = fc.createContours(trainData_1.shape[0],'Training_images')
features_1 = featureExtraction(Drawing_list_1)

Drawing_list_2 = fc.createContours(trainData_2.shape[0],'Training_images')
features_2 = featureExtraction(Drawing_list_2)

combined = np.concatenate((features,features_1),axis=0)
combined = np.concatenate((combined,features_2),axis=0)

"""
Drawing_list = fc.createContours(trainData_AB.shape[0],'Training_images')
features = featureExtraction(Drawing_list)
"""

'''=======================================CLASSIFYING HANDWRITTEN CHARACTERS=========================================='''
"""
k = [1,3,5,7,9,11,13,15,17,19,21] #k values determined from reference for KNN - 
test_sizes = [0.5,0.4,0.3,0.2,0.1] #train-test splits determined from reference - 
distance_metric = ['euclidean','manhattan','chebyshev']

for i in range(len(test_sizes)):
    X_train,X_test,y_train,y_test = train_test_split(combined,combinedLabels,test_size=test_sizes[i],shuffle=True)

    for j in range(len(distance_metric)):
        for z in range(len(k)):
            predictions = classification(k[z],X_train,y_train,X_test,distance_metric[j])
"""
'''=======================================EVALUATION METRICS========================================== '''
"""            print(accuracy_score(y_test,predictions))"""



optimum_k = 9
optimum_test_size = 0.2
distance = 'manhattan'
X_train,X_test,y_train,y_test = train_test_split(combined,combinedLabels,test_size=optimum_test_size,shuffle=True)
predictions = classification(optimum_k,X_train,y_train,X_test,distance)

'''=======================================EVALUATION METRICS=========================================='''
print(accuracy_score(y_test,predictions))
print(confusion_matrix(y_test,predictions))
print(classification_report(y_test, predictions))


