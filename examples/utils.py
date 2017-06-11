#!/usr/bin/env python

'''
Utilities for boilerplate model, which uses dSPP (https://peptone.io/dssp) dataset.
Peptone Inc. - The Protein Intelligence Company (https://peptone.io)
'''
from __future__ import print_function

from keras.callbacks import Callback
import numpy as np
import tensorflow as tf

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class LossRatio(Callback):
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
    one_digit = {'A': 0, 'C': 1, 'D': 2, 'E': 3, 'F': 4, 'G': 5, \
        'H': 6, 'I': 7, 'K': 8, 'L': 9, 'M': 10, 'N': 11, 'P': 12, \
        'Q': 13, 'R': 14, 'S': 15, 'T': 16, 'V': 17, 'W': 18, 'Y': 19}

    assert len(sequence) >= 1
    encoded = []
    for letter in sequence:
        tmp = np.zeros(20)
        tmp[one_digit[letter]] = 1
        encoded.append(tmp)
    assert len(encoded) == len(sequence)
    encoded = np.asarray(encoded)
    return list(encoded.flatten())

def generate_weights(array):
    results = []
    for row in array:
        w = np.zeros(len(row))
        mask = row != 0.0
        w[mask] = 1.0
        results.append(w)
    weights = np.array(results)
    return weights

def shuffle_and_split(X, Y, weights, seed=123456, fraction=0.8):
    assert X.shape[0] == Y.shape[0]
    assert X.shape[0] == weights.shape[0]

    # X = X.reshape(X.shape + (1,))
    # weights = weights.reshape(weights.shape + (1,))

    N = X.shape[0]
    np.random.seed(seed)
    indices = np.random.permutation(N)
    idx = int(N*fraction)
    training_idx, test_idx = indices[:idx], indices[idx:]

    (x_train, y_train, weights_train) = (X[training_idx], Y[training_idx], weights[training_idx])
    (x_test, y_test, weights_test) = (X[test_idx], Y[test_idx], weights[test_idx])

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

    def masking(tensor, mask):
        return tf.boolean_mask(tensor, mask)

    stat = tf.reduce_sum(
        tf.div(
            tf.pow(
                tf.subtract(masking(obs, mask), masking(exp, mask)),
                2),
            masking(exp, mask)),
        name="chi2_statistics")

    return stat
