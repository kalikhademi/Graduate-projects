Author: Kiana Alikhademi

These are the libraries I am using:
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from scipy import stats
from random import randint
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import itertools


The project 00 includes three separate train, test and run.py
In the train.py I will use the cross validation along with the training function to tune the KNN parameters so I could use them later in run.py. the range of K-Values could be changes easily. 

Run.py:
At the beginning I will read the bounding box from the more_red_cars.npy to come up with the all centers of the cars. 
I will use this as my ground truth which later expanded in the run.py to the 5x5 windows around it. 

After marking the intances of ground truth, the random points from Training data and ground truth will be generated to form
training and validation dataset as we could not use random functions such as train-test-split. Test data will be formed from random points in the image data. 


After generating the data, the prediction function (KNeighbor_Train) would be called to make the predictions on validation
dataset. Confusion matrix has been plotted using the instructions on [1]. The plot to show the accuracy over the range of different K has been plotted too.
I have commented the code to make image from data points of the cars.

The cross validation function has been defined in Train.py to get the best parameter for K. 

Running the scripts:
I have tested in both terminal and spyder IDE undr the Anaconda. 

Terminal: python run.py would do everything for you. 


P.S. the .npy data files are the empty ones intially was posted for the project. Due to file size limitation for pushing to the repo, I did not push them. Therefore, my train.py , test.py and run.py and more_red_cars.npy should be pulled to the repo with the original data. Otherwise, it will give the index error for reading the training data.  




1.http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
