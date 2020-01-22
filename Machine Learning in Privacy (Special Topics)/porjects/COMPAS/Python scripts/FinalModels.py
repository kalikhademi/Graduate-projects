#!/usr/bin/env python
# coding: utf-8

# In[97]:


#basic libraries
from sklearn.metrics import confusion_matrix
from keras.layers import Dense
from keras.models import Sequential
import keras
import numpy as np
import pandas as pd
import matplotlib
import os
import math
import sys
# import import_ipynb
# import dnn
import random
from datetime import datetime
# For converting textual categories to integer labels 
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import check_array
#lime
import lime
import lime.lime_tabular
from lime import lime_text
from lime.lime_text import LimeTextExplainer
#tensorflow
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from matplotlib import units


data = pd.read_csv("/Users/kianamac/Documents/GitHub/MLinprivacy/Kiana_compass/clean_compass.csv",index_col=False, header= 0)
y = data["score_text"]       #Target Variable
target = LabelEncoder().fit_transform(y)

continous_var = ['age','priors_count','days_b_screening_arrest','LengthOfStay']
categorical_var = ['c_charge_degree','race','sex','is_recid']

features = continous_var + categorical_var

data = data[features]
# Encodign text values 
categorical_var_encoders = {}
# data['days_b_screening_arrest']=data['days_b_screening_arrest'].apply(int)
X_train, X_test, y_train, y_test = train_test_split(data,target, test_size=.2, random_state=42)

categorical_var_encoders = {}
X_test = X_test.copy()
X_train = X_train.copy()

for var in categorical_var:
    le = LabelEncoder().fit(X_train[var])
    X_train[var+'_ids'] = le.transform(X_train[var])
    X_test[var+'_ids'] = le.transform(X_test[var])
    X_test.pop(var)
    X_train.pop(var)
    categorical_var_encoders[var] = le



##################################################logistic regression####################################################
clf_lr = LogisticRegression(random_state=42)
clf_lr.fit(X_train,y_train)
labels = clf_lr.predict(X_test)
accuracy_lr = accuracy_score(y_test,labels)
print(accuracy_lr*100)
predicted_fn_logreg = lambda x : clf_lr.predict_proba(x).astype(float)



###################################################Random Forest##################################################

clf_RF = RandomForestClassifier(max_depth=10, n_estimators=10, max_features=1)
clf_RF.fit(X_train,y_train)
labels = clf_RF.predict(X_test)
accuracy_rf = accuracy_score(y_test,labels)
print(accuracy_rf*100)


####################################################deep learning###################################################
one_hot_labels = keras.utils.to_categorical(y_train, num_classes=3)
np.random.seed(42)
classifier = Sequential()
# Adding the input layer and the first hidden layer
classifier.add(Dense(activation='relu', units = 6, kernel_initializer="uniform", input_dim = X_train.shape[1]))
# Adding the second hidden layer
classifier.add(Dense(activation='relu', units=6,
                     kernel_initializer="uniform"))
# Adding the output layer
classifier.add(Dense(activation='softmax', units=3,
                     kernel_initializer="uniform"))
classifier.compile(
    optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
classifier.fit(X_train, one_hot_labels, batch_size=10, nb_epoch=100)
y_test_encoded = keras.utils.to_categorical(y_test, num_classes=3)
score = classifier.evaluate(X_test, y_test_encoded, batch_size=128)
print(score)

################################################### LIME ###################################################

X_train_np = X_train.to_numpy()
X_test_numpy = X_test.to_numpy()
num_cols = data._get_numeric_data().columns
cols = data.columns
categorical_features = list(set(cols) - set(num_cols))
class_names =['Low','Medium','High']
explainer =  lime.lime_tabular.LimeTabularExplainer(X_train_np, feature_names = features, class_names=class_names,categorical_features= categorical_var,  verbose= False)
#check what explaantions we have for the frist 100th in test data
i = np.random.randint(0, X_test_numpy.shape[0])
exp = explainer.explain_instance(X_test_numpy[i],clf_lr.predict_proba , num_features=7, top_labels= 1)
exp.show_in_notebook(show_table=True, show_all = True)


#################################################### WhatIF XAI Tool ###################################################


####################################################IBM Fairness 360 ###################################################
