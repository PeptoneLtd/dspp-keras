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


def chi2(exp, obs):
    """
        Compute the log of CHI^2 statistics of non-zero expected elements
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

if __name__ == '__main__':

    # Load, normalize
    # X is protein sequence, one-hot encoded
    # Y is the ncSPC score, raw between -1 and 1 (beta-sheet to aplpha-helix)
    X, Y = dspp.load_data()
    X = pad(X, 20*parameters.N)
    Y = pad(normalize(Y), parameters.N)

    # Shuffle and split the data
    (x_train, y_train), (x_test, y_test) = shuffle_and_split(X, Y)

    batch_size = 128
    epochs = 100

    model = get_model(parameters)
    model.compile(optimizer=keras.optimizers.Adam(), loss=mean_absolute_error, metrics=[rmsd, chi2])

    model.fit(x=x_train, y=y_train, epochs=epochs, batch_size=batch_size, validation_data=(x_test, y_test), callbacks=[lossRatio()])
    score = model.evaluate(x_test, y_test)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])

    # serialize model to JSON
    with open("model.json", "w") as fp:
        fp.write(model.to_json())
    # serialize weights to HDF5
    model.save_weights("model.h5")
    print("Saved model to disk")
