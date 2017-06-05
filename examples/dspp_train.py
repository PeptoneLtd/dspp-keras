'''
Basic convnet on the dSPP (https://peptone.io/dssp) dataset.
Peptone Inc. - The Protein Intelligence Company (https://peptone.io)
'''

from __future__ import print_function
import keras, os
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
from dspp_utils import *


def get_model(parameters):

    model = Sequential()

    # Reshaping
    model.add(Reshape((20, parameters.N), input_shape=(parameters.N*20,), name="Sequence"))

    model.add(Conv1D(2*parameters.N1, parameters.kernel1, padding="same", activation='relu', name="AA_Conv_1"))
    model.add(BatchNormalization())
    model.add(Conv1D(2*parameters.N1, parameters.kernel1, padding="same", activation='relu', name="AA_Conv_2"))
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
    model.add(Reshape((parameters.N, 1), input_shape=(parameters.N,)))
    print(model.summary())

    return model

# all free parameters for the model
args = {
    "N": 800,
    "d1": 0.25, # never used
    "kernel1": 60,
    "p1": 2, # never used
    "N1": 40,
    "ND1": 800,
    "d2": 0.5,
}
parameters = Struct(**args)

X, Y = dspp.load_data()
weights = generate_weights(Y)

X = [lettercode2onehot(x) for x in X]
X = pad(X, 20*parameters.N)
Y = pad(Y, parameters.N)
weights = pad(weights, parameters.N)

if __name__ == '__main__':

    # Shuffle and split the data
    (x_train, y_train, weights_train), (x_test, y_test, weights_test) = shuffle_and_split(X, Y, weights)

    batch_size = 128
    epochs = 10

    model = get_model(parameters)
    model.compile(optimizer=keras.optimizers.Adam(), loss=logcosh, metrics=[rmsd, chi2], sample_weight=weights_train, sample_weight_mode="temporal")

    model.fit(x=x_train, y=y_train, epochs=epochs, batch_size=batch_size, validation_data=(x_test, y_test, weights_test), callbacks=[lossRatio()])
    score = model.evaluate(x_test, y_test, sample_weight=weights_test)

    # Just some simple diagnostics
    print()
    print('Test rmsd:', score[0])
    print('Test chi2:', score[1])

    # Make sure we have output directory
    if not os.path.exists("./model"):
        os.makedirs("./model")

    # Serialize model to JSON
    with open("./model/model.json", "w") as fp:
        fp.write(model.to_json())

    # Serialize weights to HDF5
    model.save_weights("./model/model.h5")
    print("Saved model to ./model/")
