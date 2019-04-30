# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 22:15:49 2018

@author: Diandra
"""
import csv
from PIL import Image
import numpy as np
import pdb
import findContours as fc
from normalization import NormalizeImage
from feature_extraction import featureExtraction
from classification import classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.externals import joblib



'''=======================================LOADING IMAGE DATA=========================================='''
trainData_2 = np.load('ClassData_2.npy') #1655 shape
trainLabels_2 = np.load('ClassLabels_1.npy') #lables for images

for index in range(len(trainData_2)):

    trainData_2[index] = trainData_2[index].astype(np.uint8)

trainData = np.load('extra_data.npy') #1655 shape
trainLabels = np.load('extra_labels.npy') #lables for images
trainData_1 = np.load('extra_data_1.npy') #images of only A and B
trainLabels_1 = np.load('extra_labels_1.npy') #labels only for images A and B

#combinedData = np.concatenate((trainData,trainData_1),axis=0)
combinedLabels = np.concatenate((trainLabels,trainLabels_1),axis=0)
combinedLabels = np.concatenate((trainLabels_2,combinedLabels),axis=0)

trainData = trainData.astype(np.uint8)
pdb.set_trace()
#trainData_1 = trainData_1.astype(np.uint8)
for index in range(len(trainData_1)):

    trainData_1[index] = trainData_1[index].astype(np.uint8)
    
#    if ((trainLabels[index] == 1) or (trainLabels[index] == 2)):
#        trainData_AB.append(trainData[index])
#        trainLabels_AB.append(trainLabels[index])

#trainData_AB = np.asarray(trainData_AB)
#trainLabels_AB = np.asarray(trainLabels_AB)

#pdb.set_trace()

'''=========================================RESIZE AND SAVE AS BITMAP IMAGES========================================'''
NormalizeImage(trainData)
NormalizeImage(trainData_1)
NormalizeImage(trainData_2)
pdb.set_trace()
'''=========================================CONTOUR IMAGES========================================'''
Drawing_list = fc.createContours(trainData.shape[0],'Training_images')
#pdb.set_trace()
features = featureExtraction(Drawing_list)

Drawing_list_1 = fc.createContours(trainData_1.shape[0],'Training_images')
features_1 = featureExtraction(Drawing_list_1)

Drawing_list_2 = fc.createContours(trainData_2.shape[0],'Training_images')
features_2 = featureExtraction(Drawing_list_2)

combined = np.concatenate((features,features_1),axis=0)
combined = np.concatenate((features_2,combined),axis=0)

pdb.set_trace()
'''=======================================CLASSIFYING HANDWRITTEN CHARACTERS=========================================='''
"""
optimum_k = 3
optimum_test_size = 0.3
distance = 'euclidean'
X_train,X_test,y_train,y_test = train_test_split(combined,combinedLabels,test_size=optimum_test_size,shuffle=True)
predictions_final = classification(optimum_k,X_train,y_train,X_test,distance)

"""
knn = joblib.load('knn_model.joblib')
test_predictions = knn.predict(combined)
#pdb.set_trace()
dist = knn.kneighbors(combined,return_distance=True)
#pdb.set_trace()
thresholds = np.load('threshold.npy')
for i in range(len(test_predictions)):
    if(np.amax(dist[0][i],axis=0) > thresholds[0] and np.amax(dist[0][i],axis=0) > thresholds[1] and 
       np.amax(dist[0][i],axis=0) > thresholds[2] and np.amax(dist[0][i],axis=0) > thresholds[3] and
       np.amax(dist[0][i],axis=0) > thresholds[4] and np.amax(dist[0][i],axis=0) > thresholds[5] and
       np.amax(dist[0][i],axis=0) > thresholds[6] and np.amax(dist[0][i],axis=0) > thresholds[7]):
        test_predictions[i] = -1
        


'''=======================================EVALUATION METRICS=========================================='''
print(accuracy_score(combinedLabels,test_predictions))
print(confusion_matrix(combinedLabels,test_predictions))