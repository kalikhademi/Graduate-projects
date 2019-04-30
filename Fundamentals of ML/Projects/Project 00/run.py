#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 09:24:33 2018

@author: kianamac
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 09:21:13 2018

@author: Kiana Alikhademi

"""
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split,KFold
from sklearn.cluster import KMeans
from scipy import stats
from random import randint
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import itertools
from test import kNearestNeighbor_Test 
from train import kNearestNeighbor_Train,cross_val


"""======================================= Read data======================================================="""

lable = np.load('data_test.npy')
gtruth = np.load('ground_truth.npy')
data = np.load('data_train.npy')
another_gtruth = np.load('more_red_cars.npy')
training=[]
validation=[]
new_data_points=[]
test =[]
training_points =[]
training_rgb =[]
validation_points=[]
validation_rgb=[]
test_points=[]
test_rgb =[]


"""=============================================compute the complete ground truth=================================="""
for item in range(another_gtruth.shape[0]):
    x = int((another_gtruth[item,0]+another_gtruth[item,2])/2)
    y = int((another_gtruth[item,1]+another_gtruth[item,3])/2)
    label = 2
    new_data_points.append([x,y,label])
new_data_points_np = np.array(new_data_points)

lable_new = new_data_points_np[:,0:new_data_points_np.shape[1]-1]
#print(lable_new)
"""=================================================== labeling the pixels in a window around ground truth==========="""
gtruth_new=[]
gtruth_training=[]
gtruth_new_np=[]
gtruth_training_rgb =[] 
for row in lable_new:
    for i in range(row[0]-2,row[0]+3):
        for j in range(row[1]-2,row[1]+3):
            label=2
            gtruth_new.append([i,j,label])

gtruth_new_np = np.array(gtruth_new)
#print(gtruth_new_np)
gtruth_new_np = gtruth_new_np[:,0:gtruth_new_np.shape[1]-1]
gtruth_validation_rgb =[]
label_z = 2
label_b = 1
"""============================================= Generate random training and validation data and test data ===================="""
for _ in range (2000):
    x,y= randint(572,1378), randint(1648,1891)
    training_points.append([x,y])
    rgb_index1 = data[x,y].ravel().tolist()
    training_rgb.append( rgb_index1)
    gtruth_training_rgb.append([rgb_index1, label_b])
    #============================= the gtruth value added=============
    z = np.random.randint(0,gtruth_new_np.shape[0],1)
    training_points.append(gtruth_new_np[z])
    rgb_index = data[gtruth_new_np[z,0],gtruth_new_np[z,1]].ravel().tolist()
    training_rgb.append(rgb_index)
    gtruth_training_rgb.append([rgb_index, label_z])
    
for _ in range (600):
    x,y= randint(375,499), randint(1762,1830)
    validation_points.append([x,y])
    rgb_index2 = data[x,y].ravel().tolist()
    validation_rgb.append(rgb_index2)
    gtruth_validation_rgb.append([rgb_index2, label_b])
     #============================= the gtruth value added=============
    z = np.random.randint(0,gtruth_new_np.shape[0],1)
    validation_points.append(gtruth_new_np[z].ravel().tolist())
    rgb_index = data[gtruth_new_np[z,0],gtruth_new_np[z,1]].ravel().tolist()
    validation_rgb.append(rgb_index)
    gtruth_validation_rgb.append([rgb_index, label_z])

for _ in range(2000):
    x,y = randint(505,1297), randint(50, 471)
    test_points.append([x,y])
    test_rgb.append(lable[x,y].tolist())



"""=================================================== label training and validation based on Ground truth============="""
np_training=np.array(training_rgb)
np_validation=np.array(validation_rgb)

"""================================================ call the function from train.py=================================="""
Krange = range(3,40,2)
label_values = [row[1] for row in gtruth_validation_rgb ]
k_value = cross_val(training_rgb,gtruth_training_rgb,validation_rgb,Krange,validation_points, gtruth_validation_rgb)
Prediction_train, red_cars = kNearestNeighbor_Train(training_rgb,gtruth_training_rgb,validation_rgb,k_value,validation_points)

"""================================================= plotting confusion matrix =========================================="""
print("the training prediction is:", Prediction_train)
print("the coordinate of cars are:",red_cars )
accuracy =  accuracy_score(label_values, Prediction_train)
cm = confusion_matrix(label_values,Prediction_train)
print("the accuracy is:", accuracy)
print(classification_report(label_values, Prediction_train))
"""This function prints and plots the confusion matrix. Normalization can be applied by setting `normalize=True`."""
def plot_confusion_matrix(cm, classes,normalize=False,title='Confusion matrix',cmap=plt.cm.Blues):
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
    
""" calling the plotting function and pass the confusin matrix object we built before"""
np.set_printoptions(precision=2)
plt.figure()
plot_confusion_matrix(cm, classes=[2,1], normalize=True,title='Normalized confusion matrix')
plt.show()


"""=========================================== call function from test.py================================================="""
np_test = np.array(test)
red_cars_test =[]
Prediction_test, red_cars_test = kNearestNeighbor_Test(training_rgb,gtruth_training_rgb,test_rgb ,k_value,test_points)
print("the prediction test is :", Prediction_test)
coordinates = [row[0] for row in red_cars]
print("the coordinate of cars are:",red_cars_test )
with open("Test_label.txt", "w") as output:
    output.write(str(Prediction_test)) 

label_values = [row[1] for row in gtruth_validation_rgb ]
x_coord = np.array([row[0] for row in red_cars])
y_coord = np.array([row[1] for row in red_cars])

#plt.imshow(data)
#plt.plot(x_coord, y_coord, 'ro')
#plt.axis('image')
#plt.show()