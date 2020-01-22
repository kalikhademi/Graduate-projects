#!/usr/bin/env python
# coding: utf-8

# In[5]:


import numpy as np
import pandas as pd
import matplotlib
import os
import math
import sys
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import warnings
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score 
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier


# In[6]:


data = pd.read_csv("clean_compass.csv")
data['LengthOfStay'] = data[['c_jail_out', 'c_jail_in']].min(axis=1)


# In[7]:


X = data.drop("decile_score",1)  #Feature Matrix
y = data["decile_score"]       #Target Variable

X_trans = pd.get_dummies(X)
X_train, X_test, y_train, y_test = train_test_split(X_trans, y, test_size=.3, random_state=42)


# In[8]:


names = ["Nearest Neighbors", "SVM","Logistic Regression", "Decision Tree", "Random Forest", "Neural Net","Naive Bayes"]

clf_knn = KNeighborsClassifier(3)
clf_svm = SVC(kernel="linear", C=0.025)
clf_lr = LogisticRegression(random_state=42, solver='lbfgs',multi_class='multinomial')
clf_dt = DecisionTreeClassifier(max_depth=5)
clf_RF = RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)
clf_mlp = MLPClassifier(alpha=1, max_iter=1000)
clf_nb = GaussianNB()

        


# In[9]:


#knn
accuracy_list=[]
clf_knn.fit(X_train,y_train)
labels = clf_knn.predict(X_test)
accuracy = accuracy_score(y_test,labels)
accuracy_list.append((names[0],accuracy))


accuracy_list


# In[ ]:


#svm

clf_svm.fit(X_train,y_train)
labels = clf_svm.predict(X_test)
accuracy = accuracy_score(y_test,labels)
accuracy_list.append((names[1],accuracy))


accuracy_list


# In[5]:


#Logistic Regression

clf_lr.fit(X_train,y_train)
labels = clf_lr.predict(X_test)
accuracy = accuracy_score(y_test,labels)
accuracy_list.append((names[2],accuracy))


accuracy_list


# In[6]:


#Decision Tree

clf_dt.fit(X_train,y_train)
labels = clf_dt.predict(X_test)
accuracy = accuracy_score(y_test,labels)
accuracy_list.append((names[3],accuracy))


accuracy_list


# In[ ]:


#knn

clf_RF.fit(X_train,y_train)
labels = clf_RF.predict(X_test)
accuracy = accuracy_score(y_test,labels)
accuracy_list.append((names[4],accuracy))


accuracy_list


# In[8]:


#knn

clf_mlp.fit(X_train,y_train)
labels = clf_mlp.predict(X_test)
accuracy = accuracy_score(y_test,labels)
accuracy_list.append((names[5],accuracy))


accuracy_list


# In[9]:


#knn

clf_nb.fit(X_train,y_train)
labels = clf_nb.predict(X_test)
accuracy = accuracy_score(y_test,labels)
accuracy_list.append((names[6],accuracy))


accuracy_list


# In[ ]:




