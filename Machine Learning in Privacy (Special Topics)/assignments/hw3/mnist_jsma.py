import logging
import numpy as np
from six.moves import xrange
import tensorflow as tf
import keras


def setup_session(verbose=False):

    # feel free to customize the session to your specific environment
    #config = tf.ConfigProto(device_count={'GPU': 1, 'CPU': 1})
    sess = tf.Session(config=tf.ConfigProto(log_device_placement=verbose))
    #sess = tf.Session(config=config)
    keras.backend.set_session(sess)

    gpus = keras.backend.tensorflow_backend._get_available_gpus()
    if len(gpus) == 0:
        print('Warning: no available GPU(s)!')


#load mnist data 
def load_preprocess_mnist_data(train_size=20000):
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
    aux_idx = train_size

    x_aux = x_train[aux_idx:, :]
    y_aux = y_train[aux_idx:, :]

    x_temp = x_train[:aux_idx, :]
    y_temp = y_train[:aux_idx, :]

    x_train = x_temp
    y_train = y_temp

    return (x_train, y_train), (x_test, y_test), (x_aux, y_aux)



#obtain image parameters



#define placeholders
