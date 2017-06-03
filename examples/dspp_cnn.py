'''Trains a simple convnet on the DSPP dataset.

TODO expected accuracy after X epochs 'Gets to 99.25% test accuracy after 12 epochs'
(there is still a lot of margin for parameter tuning).
TODO performance '16 seconds per epoch on a GRID K520 GPU.'
'''

from __future__ import print_function
import keras
from dsppkeras.datasets import dspp
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Reshape, Conv1D, MaxPooling1D, BatchNormalization, Activation, Dropout
from keras.callbacks import Callback
from keras.losses import mean_absolute_error
from keras import backend as K
import numpy as np
import tensorflow as tf

class lossRatio(Callback):
    """
        An extension of Callback class that logs the `loss`/`val_loss` ratio
    """
    def on_epoch_end(self, epoch, logs={}):
        R = logs.get('loss')/logs.get('val_loss')
        print("R(l/v_l)={:2.2f} d(1-R)={:2.2f}".format(R, 1.0-R))

def normalize(array):
    concatenated = np.concatenate(Y)
    mean, std = concatenated.mean(), concatenated.std()
    return [ (row - mean)/std for row in array ]

def pad(array, N):
    padded = [np.pad(row, (0, N-len(row)), 'constant') for row in Y]
    return np.vstack(padded)

def shuffle_and_split(X, Y, seed=123456, fraction=0.8):
    assert(X.shape[0]==Y.shape[0])
    N = X.shape[0]
    np.random.seed(seed)
    indices = np.random.permutation(N)
    idx = int(N*fraction)
    training_idx, test_idx = indices[:idx], indices[idx:]
    (x_train, y_train), (x_test, y_test) = (X[training_idx], Y[training_idx]), (X[test_idx], Y[test_idx])
    return (x_train, y_train), (x_test, y_test)

def rmsd(y_true, y_pred):
    """
        Compute the RMSD.
    """
    return tf.sqrt(tf.reduce_mean(tf.pow(y_pred - y_true, 2)))

def chi2(y_true, y_pred):
    """
        Compute the natural logarithm of CHI^2 statistics using output binning
    """
    # The number of bins, which regulates the resolution of the CHI2 test
    nbins = 10
    # Find the maximum in the true values tensor
    MAX_true = tf.reduce_max(y_true)
    MIN_true = tf.reduce_min(y_true)
    # Compute the distributions of predicted and true value
    H_pred = tf.histogram_fixed_width(y_pred, [MIN_true, MAX_true], nbins=nbins, dtype=tf.int32, name="y_pred_HIST")
    H_true = tf.histogram_fixed_width(y_true, [MIN_true, MAX_true], nbins=nbins, dtype=tf.int32, name="y_true_HIST")
    # Find and compare the max value in H_pred and H_true
    LIMIT_TEST = tf.greater_equal(tf.reduce_max(H_pred),tf.reduce_max(H_true))
    def A():
        return tf.reduce_max(H_pred)
    def B():
        return tf.reduce_max(H_true)
    # We will set the limit based on this value
    LIMIT = tf.cond(LIMIT_TEST, lambda: A(), lambda: B())
    # Avoid division by zero, by setting zero elements to 1e-8
    Y_pred = tf.clip_by_value(tf.to_float(H_pred), 1.0e-8, tf.to_float(LIMIT))
    Y_true = tf.clip_by_value(tf.to_float(H_true), 1.0e-8, tf.to_float(LIMIT))
    # Pearson CHI^2 statistics
    stat = tf.reduce_sum(tf.div(tf.pow(tf.subtract(Y_pred,Y_true), 2),Y_true),name="chi2_STAT")
    return tf.log(stat)

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

def get_model(parameters):

    model = Sequential()

    # Reshaping
    model.add(Reshape((20, parameters.N), input_shape=(parameters.N*20,), name="Sequence"))

    model.add(Conv1D(2*parameters.N1, parameters.kernel1, padding="same", activation='relu', name="AA_Conv_2_1"))
    model.add(BatchNormalization())
    model.add(Conv1D(2*parameters.N1, parameters.kernel1, padding="same", activation='relu', name="AA_Conv_2_2"))
    model.add(BatchNormalization())
    model.add(MaxPooling1D(1, strides=None, padding='same', name="AA_Pooling_2"))

    model.add(Flatten())

    # Classes and storage
    model.add(Dense(parameters.ND1, name="Class_Encoder1"))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(parameters.d2))

    model.add(Dense(parameters.ND1, name="Class_Encoder2"))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(parameters.d2))

    # Predictions
    model.add(Dense(parameters.N, name="Propensity"))

    return model

# all free parameters for the model
args = {
    "N": 800,
    "d1": 0.25,
    "kernel1": 60,
    "p1": 2,
    "N1": 40,
    "ND1": 800,
    "d2": 0.5,
}
parameters = Struct(**args)

# Load, normalize
# X is protein sequence, one-hot encoded
# Y is the ncSPC score, raw between -1 and 1 (beta-sheet to aplpha-helix)
X, Y = dspp.load_data()
X = pad(X, 20*parameters.N)
Y = pad(normalize(Y), parameters.N)

# Shuffle and split the data
(x_train, y_train), (x_test, y_test) = shuffle_and_split(X, Y)

batch_size = 128
epochs = 1

model = get_model(parameters)
model.compile(optimizer=keras.optimizers.Adam(), loss=mean_absolute_error, metrics=[rmsd, chi2])

model.fit(x=x_train, y=y_train, epochs=epochs, batch_size=batch_size, validation_data=(x_test, y_test), callbacks=[lossRatio()])
score = model.evaluate(x_test, y_test)
print('Test loss:', score[0])
print('Test accuracy:', score[1])