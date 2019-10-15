# -*- coding: utf-8 -*-
""" CIS6930PML -- Homework 2 -- attacks.py

# This file contains the attacks
"""

import os
import sys

import numpy as np
import keras

import sklearn.metrics as metrics
from sklearn.linear_model import LogisticRegression

import scipy.stats as stats


"""
## Compute attack performance metrics, i.e., accuracy and advantage (assumes baseline = 0.5)
## Note: also returns the full confusion matrix
"""
def attack_performance(in_or_out_test, in_or_out_pred):
    cm = metrics.confusion_matrix(in_or_out_test, in_or_out_pred)
    accuracy = np.trace(cm) / np.sum(cm.ravel())
    tn, fp, fn, tp = cm.ravel()
    tpr = tp / (tp + fn)
    fpr = fp / (fp + tn)
    advantage = tpr - fpr

    return accuracy, advantage, cm

"""
## Extract a random subdataset of 'sz' records
"""
def random_subdataset(x, y, sz):
    assert x.shape[0] == y.shape[0]
    perm = np.random.permutation(x.shape[0])
    perm = perm[0:sz]

    return x[perm,:].copy(), y[perm,:].copy()


"""
## Train attack models using the 'shadow training' technique of Shokri et al.
## Inputs:
##  - x_aux, y_aux: auxiliary data
##  - target_train_size: size of training data of target model
##  - create_model_fn: function to create a model of the same type as the target model
##  - train_model_fn: function to train a model of the same type as the target model [invoke as: train_model_fn(model, x, y)]
##  - num_shadow: number of shadow models (default: 4)
##  - attack_model_fn: function to create an attack model with scikit-learn
##
##  Output:
##  - attack_models: list of attack models, one per class.
"""
def shokri_attack_models(x_aux, y_aux, target_train_size, create_model_fn, train_model_fn, num_shadow=4, attack_model_fn = lambda : LogisticRegression(solver='lbfgs')):
    assert 2*target_train_size < x_aux.shape[0]

    num_classes = y_aux.shape[1]
    class_train_list = [None] * num_classes

    def add_to_list(data):
        for label in range(0, num_classes):
            dv = data[data[:,-2] == label,:]
            col_idx = [i for i in range(0, num_classes)]
            col_idx.append(num_classes+1)
            if class_train_list[label] is None:
                class_train_list[label] = dv[:,col_idx]
            else:
                class_train_list[label] = np.vstack((class_train_list[label], dv[:,col_idx]))

    for i in range(0, num_shadow):
        ## TODO ##
        ## Insert your code here to train the ith shadow model and obtain the corresponding training data for the attack model
		## You can use random_subdataset() to sample a subdataset from aux and add_to_list() to populate 'class_train_list'
        # raise NotImplementedError()
        class_train_list[i] = np.vstack((class_train_list[i], random_subdataset(x_aux,y_aux)))

    # now train the models
    attack_models = []

    for label in range(0, num_classes):
        data = class_train_list[label]
        np.random.shuffle(data)
        x_data = data[:,:-1]
        y_data = data[:,-1]

        # train attack model
        am = attack_model_fn().fit(x_data, y_data)
        attack_models.append(am)

    return attack_models

"""
## Perform the Shokri et al. attack
## Inputs:
##  - attack_models: list of attack models, one per class.
##  - x_targets, y_targets: records to attack
##  - query_target_model: function to query the target model [invoke as: query_target_model(x)]

##  Output:
##  - in_or_out_pred: in/out prediction for each target
"""
def do_shokri_attack(attack_models, x_targets, y_targets, query_target_model):

    num_classes = y_targets.shape[1]
    assert len(attack_models) == num_classes
    y_targets_labels = np.argmax(y_targets, axis=-1)

    in_or_out_pred = np.zeros((x_targets.shape[0],))

    pv = query_target_model(x_targets)
    assert pv.shape[0] == y_targets_labels.shape[0]

    for i in range(0, pv.shape[0]):
        label = y_targets_labels[i]
        assert 0 <= label < num_classes

        am = attack_models[label]
        in_or_out_pred[i] = am.predict(pv[i,:].reshape(1,-1))

    return in_or_out_pred


"""
## Perform the loss attack, assuming the training and test losses are known
## Inputs:
##  - x_targets, y_targets: records to attack
##  - query_target_model: function to query the target model [invoke as: query_target_model(x)]
##  - loss_fn: function to obtain the loss [invoke as: loss_fn(y, pred_pv)]

##  Output:
##  - in_or_out_pred: in/out prediction for each target
"""
def do_loss_attack(x_targets, y_targets, query_target_model, loss_fn, mean_train_loss, std_train_loss, mean_test_loss, std_test_loss):
    pv = query_target_model(x_targets)
    loss_vec = loss_fn(y_targets, pv)

    in_or_out_pred = np.zeros((x_targets.shape[0],))

    gauss_train = stats.norm(mean_train_loss, std_train_loss).pdf(loss_vec)
    gauss_test = stats.norm(mean_test_loss, std_test_loss).pdf(loss_vec)
    
    # in_or_out_pred = np.where(np.absolute(loss_vec - mean_train_loss)< np.absolute(loss_vec - mean_test_loss), 1, 0)
    
    in_or_out_pred = np.where(gauss_train > gauss_test, 1, 0)

    return in_or_out_pred


"""
## Perform the loss attack2, assuming the training loss is known
## Inputs:
##  - x_targets, y_targets: records to attack
##  - query_target_model: function to query the target model [invoke as: query_target_model(x)]
##  - loss_fn: function to obtain the loss [invoke as: loss_fn(y, pred_pv)]
##  - mean_train_loss, std_loss: mean and std of the training loss
##  - threshold: decision threshold

##  Output:
##  - in_or_out_pred: in/out prediction for each target
"""
def do_loss_attack2(x_targets, y_targets, query_target_model, loss_fn, mean_train_loss, std_train_loss, threshold):
    pv = query_target_model(x_targets)
    loss_vec = loss_fn(y_targets, pv)

    in_or_out_pred = np.zeros((x_targets.shape[0],))

    gauss_cdf = stats.norm(mean_train_loss, std_train_loss).cdf(loss_vec)

    in_or_out_pred = np.where( gauss_cdf < threshold, 1, 0)
    

    return in_or_out_pred


"""
## Perform the posterior attack
## Inputs:
##  - x_targets, y_targets: records to attack
##  - query_target_model: function to query the target model [invoke as: query_target_model(x)]
##  - threshold: decision threshold

##  Output:
##  - in_or_out_pred: in/out prediction for each target
"""
def do_posterior_attack(x_targets, y_targets, query_target_model, threshold):

    ## TODO ##
    ## Insert your code here
    raise NotImplementedError()

    return in_or_out_pred