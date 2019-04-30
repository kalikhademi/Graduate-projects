# -*- coding: utf-8 -*-
"""
File:   hw02.py
Author: Kiana Alikhademi
Date:   9/18/2018
Desc:   implementation of KNN and probabilistic generative function(Full and diagonal) to classify the train data
    
"""


""" =======================  Import dependencies ========================== """

import numpy as np
from matplotlib import pyplot as plt
from scipy import stats
from scipy.stats import multivariate_normal
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold 
import os 


#plt.close('all') #close any open plots

""" =======================  Import DataSet ========================== """

""" change this part to the path to the folders containing your data"""
folder = "Train data"
2Dpath ='2dDataSetforTrain'
7Dpath = '7dDataSetforTrain'
hyperPath = 'HyperSpectralDataSetforTrain'
path = folder + os.sep
Train_2D = np.loadtxt(path + 2Dpath + ".txt")
Train_7D = np.loadtxt(path + 7Dpath + ".txt")
Train_HS = np.loadtxt(path  + hyperPath + ".txt")

"""====================these lines need to be commented before the cross-validation as we are doing"""
TestFolder = "Train data"
2DpathTest ='2dDataSetforTrain'
7DpathTest = '7dDataSetforTrain'
hyperPathTest = 'HyperSpectralDataSetforTrain'
pathTest = TestFolder + os.sep
Test_2D = np.loadtxt(pathTest + 2DpathTest + ".txt")
Test_7D = np.loadtxt(pathTest + 7DpathTest + ".txt")
Test_HS = np.loadtxt(pathTest  + hyperPathTest + ".txt")



"""


===============================================================================
===============================================================================
======================== Probabilistic Generative Classfier ===================
===============================================================================
==============================================================================="""
Posterior =np.array([])
predictions_PG =np.array([])
PDF =[]
PC= np.array([])
def PriorsFunction(Train_Data,Classes):
# prior_mu,prior_cov, PC are the priors which we compute to pass it into the posterior function
    PC= []
    prior_mu = []
    prior_cov = []
    total_train_data =0
    for j in range(len(Train_Data)):
        total_train_data =0
        mu_class = list(np.mean(Train_Data[j],axis=0))
        prior_mu.append(mu_class)

        cov_class = np.cov(Train_Data[j].T)
        det = np.linalg.det(cov_class)
        if det == 0: 
            for i in range(len(cov_class)):
                for index in range(len(cov_class[0])):
                    if i==index:
                        cov_class[i][index] = cov_class[i][index] + 0.01
        prior_cov.append(cov_class)
        for item in range(len(Train_Data)):
            total_train_data = total_train_data + len(Train_Data[item])
        PC.append(len(Train_Data[j])/total_train_data)
    prior_cov = np.asarray(prior_cov)
    return prior_cov,prior_mu,PC

"""=============================Diagonal Probabilistic Generative Model====================="""
def PriorsFunction_Diag(Train_Data,Classes):
    PC= []
    prior_mu_diag = []
    cov_diagonal = []
    prior_cov = []
    total_train_data =0
    mu_class_diag=0
    for j in range(len(Train_Data)):
        mu_class_diag = np.mean(Train_Data[j],axis=0)
        prior_mu_diag.append(mu_class_diag)
        cov_matrix = np.sum(np.square(Train_Data[j]- prior_mu_diag[j]),axis =0)/len(Train_Data[j])
        cov_diagonal = np.diag(cov_matrix)
        det = np.linalg.det(cov_diagonal)
        if det == 0: 
            for i in range(len(cov_diagonal)):
                for index in range(len(cov_diagonal[0])):
                    if i==index:
                        cov_diagonal[i][index] = cov_diagonal[i][index] + 0.01
        prior_cov.append(cov_diagonal)
        for item in range(len(Train_Data)):
            total_train_data = total_train_data + len(Train_Data[item])
        PC.append(len(Train_Data[j])/total_train_data)
    prior_cov = np.asarray(prior_cov)
    return prior_cov,prior_mu_diag,PC

def PosteriorFunction(Test_Data,mu,cov,probability,Classes):
    denominator_sum=0.0
    PDF =[]
    posterior_value = 0
    predictions_PG =[]
    for j in range(len(Classes)):
        
        PDF_class = multivariate_normal.pdf(Test_Data, mean=mu[j], cov=cov[j])
        PDF.append(PDF_class)

    for i in range(len(Classes)):
        denominator_sum = denominator_sum + (PDF[i]* probability[i])
    Final_posterior =[]
    for item in range(len(Classes)): 
       posterior_value = (PDF[item]*probability[item])/denominator_sum
       Final_posterior.append(posterior_value)
    index = np.argmax(Final_posterior,axis=0)
   
    predictions_PG.append(index)
    return predictions_PG
"""

    ===============================================================================
  ===============================================================================
    ============================ KNN Classifier ===================================
    ===============================================================================
    ==============================================================================="""
#what needs to be done
#this function is getting the neighbor for each test data by getting the distances from the whole data
def GetLabels(Train_Data, test_data,k,Train_label):
    distance =0 
    distance_array =[]
    labels_neighbors=[]
    counting_dict = dict()
    for i in range(len(Train_Data)):
       distance= np.sqrt(np.sum(pow((test_data - Train_Data[i, :]),2)))
       distance_array.append((distance,i))
    distance_array = sorted(distance_array)
    for i in range(k):
        index = distance_array[i][1]
        labels_neighbors.append(Train_label[index])
    
    counting_dict = dict((x,labels_neighbors.count(x)) for x in set(labels_neighbors))
    label_final = max(counting_dict, key=counting_dict.get)
    return label_final  

def fitModel_KNN(Train_Data, Train_label, Test_data, k):
    predictions_KNN =[]
    #labels_neighbors=[]
    for i in range(len(Test_data)):
        predictions_KNN.append(GetLabels(Train_Data,Test_data[i],k,Train_label))
    return predictions_KNN 

""" ======================== Cross Validation ============================= """
# Here you can change your data set. you should comment out only the Train you want. NOTE: do not pick out the labels as we do it in the for loop
Train = Train_2D
#labels = labels_2D
#Classes = np.sort(np.unique(labels))

#===================================================================================
#Train = Train_7D
#labels = labels_7D
#Classes = np.sort(np.unique(labels))

##========================================================================================
#Train = Train_HS
#labels = labels_HS
#Classes = np.sort(np.unique(labels))

"""=================================K-Fold cross validation================================"""
Accuracy_vector=[]
accurcay_total=[]
Mean_average_accuracy_total=[]
accuracy_PG_total=[]
accuracy_PG_Diag_total=[]
kf = KFold(n_splits=4,random_state = None, shuffle = True)
for train_index, valid_index in kf.split(Train):
    Accuracy_vector=[]
    X_train, X_valid = Train[train_index], Train[valid_index] 
    label_train = X_train[:,X_train.shape[1]-1]
    label_valid = X_valid[:,X_valid.shape[1]-1]
      
    X_train = np.delete(X_train,X_train.shape[1]-1,axis = 1)
    X_valid = np.delete(X_valid,X_valid.shape[1]-1,axis = 1)
    print("X.Train is :", X_train)
    """=================Get the trainign labels to identify the classes============="""
    labels = label_train
    Classes = np.sort(np.unique(labels))
    X_train_class = []
    for j in range(Classes.shape[0]):
        jth_class = X_train[label_train == Classes[j],:]
        X_train_class.append(jth_class)
    
    
    #Visualization of first two dimension of your dataSet
    for j in range(Classes.shape[0]):
        plt.scatter(X_train_class[j][:,0],X_train_class[j][:,1])  
      
    
    """ ===============train the PG on the new train data================================"""
    
    cov,mu,probability = PriorsFunction(X_train_class,Classes)
    predictions_PG = PosteriorFunction(X_valid,mu,cov,probability,Classes)
    accuracy_PG=accuracy_score(label_valid, predictions_PG[0])
    accuracy_PG_total.append(accuracy_PG)
    print('\nThe accuracy of Probabilistic Generative classifier is: ', accuracy_PG*100, '%')
    print("the accuarcu PG is", accuracy_PG_total)
    
    """============================ train the diagonal model============================"""
    diag_cov,mu_diag,probability = PriorsFunction_Diag(X_train_class,Classes)
    predictions_PGdiag = PosteriorFunction(X_valid,mu_diag,diag_cov,probability,Classes)
    accuracy_PGdiag=accuracy_score(label_valid, predictions_PGdiag[0])
    print('\nThe accuracy of Probabilistic Diagonal Generative classifier is: ', accuracy_PGdiag*100, '%')
    accuracy_PG_Diag_total.append(accuracy_PGdiag)
    print("the accuracy Probabilistic Diagonal Generative classifier is:", accuracy_PG_Diag_total)
    """================================= KNN model======================================"""
       
    for k in range(3,20):
        predictions_KNN=np.array(fitModel_KNN(X_train, label_train, X_valid, k))
        accuracy_KNN =accuracy_score(label_valid, predictions_KNN)
        print('\nThe accuracy of KNN classifier is: ', accuracy_KNN*100, '%')
        Accuracy_vector.append(accuracy_KNN)
    accurcay_total.append(Accuracy_vector)
    print("the accuracy total is:", accurcay_total)
    print('\nThe len of accuracy total is: ',len(accurcay_total))
    K_range=np.arange(3,20)
    Mean_average_accuracy_total = np.mean(accurcay_total,axis=0)
    print("the mean is:",Mean_average_accuracy_total )
    print("the size of mean is:",len(Mean_average_accuracy_total))
    
    index = np.argmax(Mean_average_accuracy_total)
    optimum_k = K_range[index]
    print("the optimum k is:",optimum_k)
    print("the index is:", index)

"""

 ========================  Test the Model ============================== 

"""

""" This is where you should test the testing data with your classifier """
"""  I have divided the train data into the  X_train_class to make sure it is separated by classes befor giving to my functions"""
# if you want to generate the test results with the models I have been used you should comment this whoel section one by one with each dataste
#X_train_class=[]
#for j in range(Classes.shape[0]):
#          jth_class = Train[labels == Classes[j],:]
#          X_train_class.append(jth_class)
      
"""===============================Trainign and testing for the 2D dataset=================================="""
#cov_diag_test,mu_diag_test,probability = PriorsFunction_Diag(X_train_class,Classes)
#predictions_PGdiag_2D = PosteriorFunction(Test_2D,mu_diag_test,cov_diag_test,probability,Classes)
#print("the prediction of 2D is:", predictions_PGdiag_2D)
"""===============================Trainign and testing for the 7D dataset=================================="""
#cov_diag_test,mu_diag_test,probability = PriorsFunction_Diag(X_train_class,Classes)         
#predictions_PGdiag_7D = PosteriorFunction(Test_7D,mu_diag_test,cov_diag_test,probability,Classes)
#print("the prediction of 7D is:", predictions_PGdiag_7D[0])
"""===============================Trainign and testing for the Hyprespectral  dataset=================================="""
#predictions_KNN_HS = np.array(fitModel_KNN(Train, labels, Test_HS, 18))
#print("the prediction of KNN is:", predictions_KNN_HS)


"""================================= save  into the text files=========================================================="""
#np.savetxt('2DforTestLabels.txt', predictions_PGdiag_2D)
#np.savetxt('7DforTestLabels.txt', predictions_PGdiag_7D)
#np.savetxt('HyperSpectralforTestLabels.txt', predictions_KNN_HS)



