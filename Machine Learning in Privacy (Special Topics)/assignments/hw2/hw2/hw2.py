# -*- coding: utf-8 -*-
""" CIS6930PML -- Homework 2 -- hw2.py

# This file is the main homework file
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
# we'll use keras for neural networks
import keras
from keras.datasets import mnist
import os
# our neural network architectures
import nets
import collections
import attacks
import warnings
import math
from keras.datasets import cifar100
from keras.layers import Conv2D, MaxPooling2D
from keras.models import Sequential
warnings.simplefilter("ignore")
from sklearn.neural_network import MLPClassifier
## os / paths
def ensure_exists(dir_fp):
    if not os.path.exists(dir_fp):
        os.makedirs(dir_fp)

## parsing / string conversion to int / float
def is_int(s):
    try:
        z = int(s)
        return z
    except ValueError:
        return None


def is_number(s):
    try:
        z = int(s)
        return z
    except ValueError:
        try:
            z = float(s)
            return z
        except ValueError:
            return None


"""
## Load and preprocess the dataset
"""
def load_preprocess_mnist_data(train_in_out_size=2000):
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    # MNIST has overall shape (60000, 28, 28) -- 60k images, each is 28x28 pixels
    print('Loaded mnist data; shape: {} [y: {}], test shape: {} [y: {}]'.format(x_train.shape, y_train.shape,
                                                                                      x_test.shape, y_test.shape))
    # Let's flatten the images for easier processing (labels don't change)
    flat_vector_size = 28 * 28
    x_train = x_train.reshape(x_train.shape[0], flat_vector_size)
    x_test = x_test.reshape(x_test.shape[0], flat_vector_size)

    # Put the labels in "one-hot" encoding using keras' to_categorical()
    num_classes = 10
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    # let's split the training set further
    aux_idx = train_in_out_size

    x_aux = x_train[aux_idx:,:]
    y_aux = y_train[aux_idx:,:]

    x_temp = x_train[:aux_idx,:]
    y_temp = y_train[:aux_idx,:]

    out_idx = int(aux_idx/2.0)
    x_out = x_temp[out_idx:,:]
    y_out = y_temp[out_idx:,:]

    x_train = x_temp[:out_idx,:]
    y_train = y_temp[:out_idx,:]

    return (x_train, y_train), (x_out, y_out), (x_test, y_test), (x_aux, y_aux)


"""
## Plots an image or set of images (all 28x28)
## input is either a single image, i.e., np.array with shape (28,28), or a square number of images, i.e., np.array with shape (z*z, 28, 28) for some integer z > 1
"""
def plot_image(im, fname='out.png', show=False):
    fig = plt.figure()
    im = im.reshape((-1,28, 28))

    num = im.shape[0]
    assert num <= 3 or np.sqrt(num)**2 == num, 'Number of images is too large or not a perfect square!'
    if num <= 3:
        for i in range(0, num):
            plt.subplot(1, num, 1 + i)
            plt.axis('off')
            plt.imshow(im[i], cmap='gray_r') # plot raw pixel data
    else:
        sq = int(np.sqrt(num))
        for i in range(0, num):
            plt.subplot(sq, sq, 1 + i)
            plt.axis('off')
            plt.imshow(im[i], cmap='gray_r') # plot raw pixel data

    ensure_exists('./plots')
    out_fp = './plots/{}'.format(fname)
    plt.savefig(out_fp)

    if show is False:
        plt.close()


"""
## Setup tf session. Please customize to your specific environment!
"""
def setup_session(verbose=False):

    # feel free to customize the session to your specific environment
    #config = tf.ConfigProto(device_count={'GPU': 1, 'CPU': 1})
    sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(log_device_placement=verbose))
    #sess = tf.Session(config=config)
    keras.backend.set_session(sess)

    gpus = keras.backend.tensorflow_backend._get_available_gpus()
    if len(gpus) == 0:
        print('Warning: no available GPU(s)!')


"""
## Extract 'sz' targets from in/out data
"""
def get_targets(x_in, y_in, x_out, y_out, sz=5000):

    x_temp = np.vstack((x_in, x_out))
    y_temp = np.vstack((y_in, y_out))

    inv = np.ones((x_in.shape[0],1))
    outv = np.zeros((x_out.shape[0],1))
    in_out_temp = np.vstack((inv, outv))

    assert x_temp.shape[0] == y_temp.shape[0]

    if sz > x_temp.shape[0]:
        sz = x_temp.shape[0]

    perm = np.random.permutation(x_temp.shape[0])
    perm = perm[0:sz]
    x_targets = x_temp[perm,:]
    y_targets = y_temp[perm,:]

    in_out_targets = in_out_temp[perm,:]

    return x_targets, y_targets, in_out_targets



## this is the main
def main():

    # figure out the problem number
    assert len(sys.argv) >= 5, 'Incorrect number of arguments!'
    p_split = sys.argv[1].split('problem')
    assert len(p_split) == 2 and p_split[0] == '', 'Invalid argument {}.'.format(sys.argv[1])
    problem_str = p_split[1]

    assert is_number(problem_str) is not None, 'Invalid argument {}.'.format(sys.argv[1])
    problem = float(problem_str)
    probno = int(problem)

    if probno <= 0 or probno > 4:
        assert False, 'Problem {} is not a valid problem # for this assignment/homework!'.format(problem)

    ## change this line to override the verbosity behavior
    verb = True if probno == 1 else False

    # get arguments
    target_model_str = sys.argv[2]
    if target_model_str.startswith('simple'):
        simple_args = target_model_str.split(',')
        assert simple_args[0] == 'simple' and len(simple_args) == 3, '{} is not a valid network description string!'.format(target_model_str)
        hidden = is_int(simple_args[1])
        reg_const = is_number(simple_args[2])
        assert hidden is not None and hidden > 0 and reg_const is not None and reg_const >= 0.0, '{} is not a valid network description string!'.format(target_model_str)
        target_model_train_fn = lambda: nets.get_simple_classifier(num_hidden=hidden, l2_regularization_constant=reg_const,
                                                                   verbose=verb)
    elif target_model_str == 'deep':
        target_model_train_fn = lambda: nets.get_deeper_classifier(verbose=verb)
    else:
        assert False, '{} is not a valid network description string!'.format(target_model_str)

    target_model = target_model_train_fn() # compile the target model

    train_in_out_size = is_int(sys.argv[3])
    num_epochs = is_int(sys.argv[4])

    assert train_in_out_size is not None and 100 <= train_in_out_size <= 10000, '{} is not a valid size for the target model training dataset!'.format(sys.argv[3])
    assert num_epochs is not None and 0 < num_epochs <= 10000, '{} is not a valid size for the number of epochs to train the target model!'.format(sys.argv[4])

    setup_session() # setup the tf session

    # load the dataset
    train, out, test, aux = load_preprocess_mnist_data(train_in_out_size=2*train_in_out_size)
    x_train, y_train = train
    target_train_size = x_train.shape[0]
    x_out, y_out = out
    x_test, y_test = test
    x_aux, y_aux = aux

    # extract targets (some in, some out)
    x_targets, y_targets, in_or_out_targets = get_targets(x_train, y_train, x_out, y_out)

    assert train_in_out_size == target_train_size, 'Inconsistent training data size!'

    # train the target model
    train_loss, train_accuracy, test_loss, test_accuracy = nets.train_model(target_model, x_train, y_train, x_test, y_test, num_epochs, verbose=verb)

    print('Trained target model on {} records. Train accuracy and loss: {:.1f}%, {:.2f} -- Test accuracy and loss: {:.1f}%, {:.2f}'.format(target_train_size,
                                                                                    100.0*train_accuracy, train_loss, 100.0*test_accuracy, test_loss))

    query_target_model = lambda x: target_model.predict(x)
    predictions = query_target_model(x_test)

    if probno == 1: ## problem 1
        assert len(sys.argv) == 5, 'Invalid extra argument'

        #to find which ones are misclassified
        # idx= []
        # result =[]
        # predictions = predictions.round()
        # idx =(predictions == y_test).all(axis=1)
        # # print(collections.Counter(idx))
        # # print(idx)
        # for i in range(len(idx)):
        # 	if idx[i] == False:
	       #  	plot_image(x_test[i], fname='out_{}.png'.format(i), show=False)
        

    elif probno == 2: ## problem 2

        assert len(sys.argv) == 7, 'Incorrect number of argument'

        num_shadow = is_int(sys.argv[5])
        attack_model_str = sys.argv[6]

        assert num_shadow is not None and 1 < num_shadow <= 200, '{} is not a valid number of shadow models!'.format(sys.argv[5])

        ## You can add new model types here
        if attack_model_str == 'LR':
            from sklearn.linear_model import LogisticRegression
            attack_model_fn = lambda : LogisticRegression(solver='lbfgs')
        elif attack_model_str == 'DT':
            from sklearn.tree import DecisionTreeClassifier
            attack_model_fn = DecisionTreeClassifier
        elif attack_model_str == 'RF':
            from sklearn.ensemble import RandomForestClassifier
            attack_model_fn = RandomForestClassifier
        elif attack_model_str == 'NB':
            from sklearn.naive_bayes import GaussianNB
            attack_model_fn = GaussianNB
        elif attack_model_str == 'MLP':
            from sklearn.neural_network import MLPClassifier
            attack_model_fn = lambda : MLPClassifier(max_iter=500)
        elif attack_model_str == 'SVM':
            from sklearn.svm import LinearSVC
            attack_model_fn = LinearSVC
        else:
            assert False, '{} is not a valid attack model type!'.format(attack_model_str)

        create_model_fn = target_model_train_fn
        train_model_fn = lambda model, x, y: nets.train_model(model, x, y, None, None, num_epochs, verbose=False)

        attack_models = attacks.shokri_attack_models(x_aux, y_aux, target_train_size, create_model_fn, train_model_fn,
                                                    num_shadow=num_shadow, attack_model_fn=attack_model_fn)


        in_or_out_pred = attacks.do_shokri_attack(attack_models, x_targets, y_targets, query_target_model)
        accuracy, advantage, _ = attacks.attack_performance(in_or_out_targets, in_or_out_pred)

        print('Shokri attack ({}) accuracy, advantage: {:.1f}%, {:.2f}'.format(attack_model_str, 100.0*accuracy, advantage))


    elif probno == 3:  ## problem 3

        assert len(sys.argv) == 5, 'Invalid extra argument'

        loss_fn = nets.compute_loss
        loss_train_vec = loss_fn(y_train, target_model.predict(x_train))
        loss_test_vec = loss_fn(y_test, target_model.predict(x_test))

        mean_train_loss = np.mean(loss_train_vec)
        std_train_loss = np.std(loss_train_vec)
        mean_test_loss = np.mean(loss_test_vec)
        std_test_loss = np.std(loss_test_vec)

        #loss attack
        in_or_out_pred = attacks.do_loss_attack(x_targets, y_targets, query_target_model, loss_fn, mean_train_loss, std_train_loss,
                                                mean_test_loss, std_test_loss)
        accuracy, advantage, _ = attacks.attack_performance(in_or_out_targets, in_or_out_pred)
        accuracy_loss = []

        print('Loss attack accuracy, advantage: {:.1f}%, {:.2f}'.format(100.0*accuracy, advantage))

        #picking the best threshold for the loss atack2
        accuracy_list = []
        accuracy_posterior=[]
        threshold = [0.1,0.3,0.5,0.7,0.9]
        for item  in threshold:
	        in_or_out_pred = attacks.do_loss_attack2(x_targets, y_targets, query_target_model, loss_fn, mean_train_loss, std_train_loss, item)
	        accuracy, advantage, _ = attacks.attack_performance(in_or_out_targets, in_or_out_pred)
	        accuracy_list.append(accuracy)
        # print(accuracy_list)
        accuracy_list = [ round(elem, 2) for elem in accuracy_list ]
        idx = accuracy_list.index(max(accuracy_list))
        best_threshold_lossattack2 = threshold[idx]

        print("the best threshold for loss attack 2 is:", best_threshold_lossattack2,max(accuracy_list))
        ## Insert your code here to compute the best threshold (for posterior_attack)
        plot_list =[]
        for i in range(len(accuracy_list)):
            plot_list.append((threshold[i],accuracy_list[i]))

        labels, ys = zip(*plot_list)
        xs = np.arange(len(labels)) 
        width =  0.5
        high = max(ys)
        low = min(ys)
        # plt.ylim([math.ceil(low-0.5*(high-low)), math.ceil(high+0.5*(high-low))])
        plt.bar(xs, ys, width, align='center')

        plt.xticks(xs, labels) #Replace default x-ticks with xs, then replace xs with labels
        plt.yticks(ys)
        print("loss 2 acc:", accuracy_list)
        plt.savefig('Lossattack2_threshold.png')

        #posterior attack
        for item  in threshold:
	        in_or_out_pred = attacks.do_posterior_attack(x_targets, y_targets, query_target_model, item )
	        accuracy, advantage, _ = attacks.attack_performance(in_or_out_targets, in_or_out_pred)
	        accuracy_posterior.append(accuracy)
        # in_or_out_pred_post = attacks.do_posterior_attack(x_targets, y_targets, query_target_model, 0.5)
        # accuracy, advantage, _ = attacks.attack_performance(in_or_out_targets, in_or_out_pred_post)
        accuracy_posterior = [ round(elem, 2) for elem in accuracy_posterior ]
        idx_post = accuracy_posterior.index(max(accuracy_posterior))
        best_threshold_posterior = threshold[idx_post]
        print('posterior attack accuracy, threshold: {:.1f}%, {:.2f}'.format(100.0*accuracy_posterior[idx_post], best_threshold_posterior))
        ## Insert your code here to compute the best threshold (for posterior_attack)
        plot_list_posterior =[]
        for i in range(len(accuracy_posterior)):
            plot_list_posterior.append((threshold[i],accuracy_posterior[i]))

        labels, ys = zip(*plot_list_posterior)
        xs = np.arange(len(labels)) 
        width =  0.5

        plt.bar(xs, ys, width, align='center')

        plt.xticks(xs, labels) #Replace default x-ticks with xs, then replace xs with labels
        plt.yticks(ys)
        print("posterior acc:", accuracy_posterior)
        
        plt.savefig('Posterior_threshold.png')
    elif probno == 4:  ## problem 4
	    num_shadow = is_int(sys.argv[5])
	    from sklearn.neural_network import MLPClassifier
	    attack_model_fn = lambda : MLPClassifier(max_iter=500)
	    create_model_fn = target_model_train_fn
	    train_model_fn = lambda model, x, y: nets.train_model(model, x, y, None, None, num_epochs, verbose=False)
	    attack_models = attacks.shokri_attack_models(x_aux, y_aux, target_train_size, create_model_fn, train_model_fn,
	                                                num_shadow=num_shadow, attack_model_fn=attack_model_fn)
	    in_or_out_pred_shokri = attacks.do_shokri_attack(attack_models, x_targets, y_targets, query_target_model)
	    accuracy_shokri, advantage, _ = attacks.attack_performance(in_or_out_targets, in_or_out_pred_shokri)

	    print('Shokri attack (MLP) accuracy, advantage: {:.1f}%, {:.2f}'.format( 100.0*accuracy_shokri, advantage))
	    #Do Loss Attack
	    loss_fn = nets.compute_loss
	    loss_train_vec = loss_fn(y_train, target_model.predict(x_train))
	    loss_test_vec = loss_fn(y_test, target_model.predict(x_test))

	    mean_train_loss = np.mean(loss_train_vec)
	    std_train_loss = np.std(loss_train_vec)
	    mean_test_loss = np.mean(loss_test_vec)
	    std_test_loss = np.std(loss_test_vec)

	    #loss attack
	    in_or_out_pred_loss = attacks.do_loss_attack(x_targets, y_targets, query_target_model, loss_fn, mean_train_loss, std_train_loss,
	                                            mean_test_loss, std_test_loss)
	    accuracy_loss, advantage, _ = attacks.attack_performance(in_or_out_targets, in_or_out_pred_loss)

	    print('Loss attack accuracy, advantage: {:.1f}%, {:.2f}'.format(100.0*accuracy_loss, advantage))
	    #Do Loss Attack 2
	    in_or_out_pred_loss2 = attacks.do_loss_attack2(x_targets, y_targets, query_target_model, loss_fn, mean_train_loss, std_train_loss, 0.5)
	    accuracy_loss2, advantage, _ = attacks.attack_performance(in_or_out_targets, in_or_out_pred_loss2)
	    print('Loss attack2 accuracy, advantage: {:.1f}%, {:.2f}'.format(100.0*accuracy_loss2, advantage))
	    #Do posterior attack
	    in_or_out_pred_post = attacks.do_posterior_attack(x_targets, y_targets, query_target_model, 0.7 )
	    accuracy_posterior, advantage, _ = attacks.attack_performance(in_or_out_targets, in_or_out_pred_post)
	    print('posterior accuracy, advantage: {:.1f}%, {:.2f}'.format(100.0*accuracy_posterior, advantage))

    elif probno == 5:  ## problem 5 (bonus)

        assert len(sys.argv) >= 5, 'Inconsistent number of arguments'

        # (X_train, y_train), (X_test, y_test) = cifar100.load_data()
		# print('x_train shape:', x_train.shape)
		# print(x_train.shape[0], 'train samples')
		# print(x_test.shape[0], 'test samples')
		#nbclasses = 100
		# Y_train = np_utils.to_categorical(y_train, nb_classes)
		# Y_test = np_utils.to_categorical(y_test, nb_classes)
		# train_loss, train_accuracy, test_loss, test_accuracy = nets.train_model(target_model, x_train, y_train, x_test, y_test, num_epochs, verbose=verb)

	 	#print('Trained target model on {} records. Train accuracy and loss: {:.1f}%, {:.2f} -- Test accuracy and loss: {:.1f}%, {:.2f}'.format(target_train_size,
  		#                                                                                   100.0*train_accuracy, train_loss, 100.0*test_accuracy, test_loss))

	 	# query_target_model = lambda x: target_model.predict(x)
	 	# predictions = query_target_model(x_test)


		        

if __name__ == '__main__':
    main()
