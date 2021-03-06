# -*- coding: utf-8 -*-
""" CIS6930PML -- Homework 3 -- attacks.py

# This file contains the attacks
"""

import os
import sys

import numpy as np
import keras

import sklearn.metrics as metrics
from sklearn.linear_model import LogisticRegression

import scipy.stats as stats
import tensorflow as tf

"""
## Returns the gradient of the loss (categorical crossentropy) with respect to the input (given class label 'target_class')
"""
def gradient_of_loss_wrt_input(model, x_in, target_class, num_classes=10):
    session = keras.backend.get_session()       # get the session

    # for the loss, we use the categorical crossentropy with respect to target_class (user specified)
    loss = -1.0 * keras.backend.categorical_crossentropy(keras.utils.to_categorical(target_class, num_classes), model.output)
    grads = keras.backend.gradients(loss, model.input)

    # run eval to actually compute the gradient
    # note: the result is a list and the element at index [0] contains the actual gradient array
    grads = session.run(grads, feed_dict={model.input: x_in})

    return grads[0].copy()

"""
## Iterative adversarial perturbation attack which "turns off" pixel one by one. Returns the adversarial perturbation.
## The attack runs until the termination condition or the maximum number of iterations is reached (whichever occurs first)
"""
def turn_off_pixels_iterative_attack(model, x_input, target_class, max_iter, terminate_fn, on_threshold=10):
    x_in = x_input.copy()
    x_adv = x_in.copy()                         # initial adversarial perturbation
    for i in range(0, max_iter):

        # grab the gradient of the loss (given target_class) with respect to the input!
        grad = gradient_of_loss_wrt_input(model, x_in, target_class)

        for j in range(x_in.shape[1]):          # note: range of the loop doesn't matter here, we just need to eventually terminate
            pixel_idx = np.argmax(-grad[0])
            if x_in[0,pixel_idx] > on_threshold:
                break                           # we found a pixel to "turn off"
            grad[0, pixel_idx] = 0.0

        x_adv[0, pixel_idx] = 0                 # "turn off" this pixel

        iters = i+1 # save the number of iterations so we can return it
        # check if we should stop the attack early
        if terminate_fn(model, x_in, x_adv, target_class):
            break

        x_in = x_adv    # for next iter: the current adversarial perturbation becomes our new input

    return x_adv, iters

"""
## Iterative adversarial perturbation attack which turns pixel 'on' one by one. Returns the adversarial perturbation.
## The attack runs until the termination condition or the maximum number of iterations is reached (whichever occurs first)
##
## Implementation notes: 
##      -'on_threshold' is the pixel value above which we consider a pixel to be 'on'; 
##      - 'on_val' is the value to set a pixel to when you want to turn it 'on'.
"""
def turn_on_pixels_iterative_attack(model, x_input, target_class, max_iter, terminate_fn, on_threshold=10, on_val=225):

    x_in = x_input.copy()
    x_adv = x_in.copy()                         # initial adversarial perturbation
    for i in range(0, max_iter):

        # grab the gradient of the loss (given target_class) with respect to the input!
        grad = gradient_of_loss_wrt_input(model, x_in, target_class)

        # ## TODO ##
        # ## Insert your code here
        # ## Use the gradient 'grad' to locate which pixel to turn on (at most one per iteration)
        # ## Note: to turn on a pixel set its value to 'on_val'.
        # ## Be careful and do not modify any pixels that are already on!
        # raise NotImplementedError()
        # note: range of the loop doesn't matter here, we just need to eventually terminate
        for j in range(x_in.shape[1]):
            pixel_idx = np.argmax(grad[0])
            if x_in[0, pixel_idx] <= on_threshold:
                if x_adv[0, pixel_idx] == 0:
                    break                           # we found a pixel to "turn on"
            grad[0, pixel_idx] = 0

        x_adv[0, pixel_idx] = on_val

        iters = i+1 # save the number of iterations so we can return it
        # check if we should stop the attack early
        if terminate_fn(model, x_in, x_adv, target_class):
            break

        x_in = x_adv    # for next iter: the current adversarial perturbation becomes our new input

    return x_adv, iters


def adversarial_examples(model, x_train, target_class, max_iter, eta):
    #random image to start with it
    x = np.random.normal(0.5, 0.3, x_train.shape)

    # GD on the input
    for i in range(max_iter):
        d = gradient_of_loss_wrt_input(model, x,target_class,num_classes=10)
        x -= eta * d

    target_label = np.zeros((10, 1))
    target_label[target_class] = 1
    y = np.full((50000, 10), 0)
    y[:,target_class] = 1
    return x, y


def fgsm_simple(model, x_input, target_class, max_iter, eps, terminate_fn):
    x_in = x_input.copy()
    adv_x = x_in
    # y_bar = model(xadv)

    for i in range(max_iter):
        # Get the gradients of the loss w.r.t to the input image.
        grad = gradient_of_loss_wrt_input(model,x_in, target_class)
        
        # Get the sign of the gradients to create the perturbation
        signed_grad = np.sign(grad[0])
        adv_x = adv_x + eps*signed_grad
        # adv_x = tf.clip_by_value(adv_x, 0, 1)
        iters = i+1
        
        # x_in = adv_x
    return adv_x, iters


