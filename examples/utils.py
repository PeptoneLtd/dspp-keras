
from __future__ import print_function
import keras
from dsppkeras.datasets import dspp
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Reshape, Conv1D, MaxPooling1D, BatchNormalization, Activation, Dropout
from keras.callbacks import Callback
from keras.losses import logcosh
from keras import backend as K
import numpy as np
import pandas as pd
import tensorflow as tf

class lossRatio(Callback):
    """
        An extension of Callback class that logs the `loss`/`val_loss` ratio
    """
    def on_epoch_end(self, epoch, logs={}):
        R = logs.get('loss')/logs.get('val_loss')
        print(" R(l/v_l)={:2.2f}".format(R))


def lettercode2onehot(sequence):
    """
        Return a binary one-hot vector
    """
    one_digit = {'A': 0, 'C': 1, 'D': 2, 'E': 3, 'F': 4,'G': 5,
    'H': 6, 'I': 7, 'K': 8, 'L': 9, 'M': 10, 'N': 11,'P': 12,
     'Q': 13, 'R': 14, 'S': 15, 'T': 16, 'V': 17,'W': 18, 'Y': 19}

    assert(len(sequence) >= 1)
    encoded = []
    for letter in sequence:
        tmp = np.zeros(20)
        tmp[one_digit[letter]] = 1
        encoded.append(tmp)
    assert(len(encoded) == len(sequence))
    encoded = np.asarray(encoded)
    return list(encoded.flatten())

def generate_weights(array, parameters):
    results = []
    for element in array:
        w = np.zeros(parameters.N)
        w[:len(element)] = 1.0
        results.append(w)
    weights = np.array(results)
    return weights

def normalize(array):
    concatenated = np.concatenate(array)
    mean, std = concatenated.mean(), concatenated.std()
    return [ (row - mean)/std for row in array ]

def pad(array, N):
    padded = [np.pad(row, (0, N-len(row)), 'constant') for row in array]
    return np.vstack(padded)

def shuffle_and_split(X, Y, weights, seed=123456, fraction=0.8):
    assert(X.shape[0]==Y.shape[0])
    assert(X.shape[0]==weights.shape[0])
    N = X.shape[0]
    np.random.seed(seed)
    indices = np.random.permutation(N)
    idx = int(N*fraction)
    training_idx, test_idx = indices[:idx], indices[idx:]
    (x_train, y_train, weights_train) = (X[training_idx], Y[training_idx], weights[training_idx])
    (x_test, y_test, weights_test) = (X[test_idx], Y[test_idx], weights[test_idx])

    y_test = np.reshape(y_test, y_test.shape + (1,))
    y_train = np.reshape(y_train, y_train.shape + (1,))

    return (x_train, y_train, weights_train), (x_test, y_test, weights_test)

def rmsd(y_true, y_pred):
    """
        Compute the RMSD.
    """
    return tf.sqrt(tf.reduce_mean(tf.pow(y_pred - y_true, 2)))

def chi2(exp, obs):
    """
        Compute CHI^2 statistics of non-zero expected elements
    """
    zero = tf.constant(0, dtype=tf.float32)
    mask = tf.not_equal(exp, zero)

    def foo(tensor, mask):
        return tf.boolean_mask(tensor, mask)

    stat = tf.reduce_sum(
        tf.div(
            tf.pow(
                tf.subtract(foo(obs, mask),foo(exp, mask)),
            2),
        foo(exp, mask)),
    name="log_chi2_statistics")

    return stat

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

def handle_nan_distribution(X, Y):
    df = pd.DataFrame({"Seq": np.concatenate([list(x) for x in X]), "ncSPC": np.concatenate(Y)})
    df = df[df.ncSPC != 0.0]
    distribution = {k: gr.ncSPC.values for k, gr in df.groupby("Seq")}

    results = []
    for x, y in zip(X, Y):
        y = np.array(y)
        mask = y == 0.0
        y[mask] = [np.random.choice(distribution[letter]) for letter in x[mask]]
        results.append((x,y))

    return zip(*results)

def handle_nan_remove(X, Y):
    df = pd.DataFrame({"Seq": np.concatenate([list(x) for x in X]), "ncSPC": np.concatenate(Y)})
    df = df[df.ncSPC != 0.0]
    distribution = {k: gr.ncSPC.values for k, gr in df.groupby("Seq")}

    results = []
    for x, y in zip(X, Y):
        y = np.array(y)
        mask = y != 0.0
        results.append((x[mask],y[mask]))

    return zip(*results)
