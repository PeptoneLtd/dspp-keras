#!/usr/bin/env python

'''
train.py
A boilerplate for Deep Learning models using
dSPP - Database of Structural Propensities of Proteins (https://peptone.io/dssp) dataset.
Peptone Inc. - The Protein Intelligence Company (https://peptone.io)
'''

from __future__ import print_function

import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.losses import logcosh
from keras.preprocessing.sequence import pad_sequences

from dsppkeras.datasets import dspp
from utils import Struct, lettercode2onehot, shuffle_and_split, generate_weights, LossRatio, rmsd, chi2

def get_model(args):
    """
    Boilerplate model given some initial configuration

    WARNING this is a boilerplate model simply to get you started
    with dSPP and structural propensities of proteins.
    """
    model = Sequential()
    model.add(Dense(args.maxlen, input_shape=(20*args.maxlen,), name="Prediction"))
    print(model.summary())
    return model

# all free parameters for the model
parameters = Struct(**{
    "maxlen": 800,
})

X, Y = dspp.load_data()
weights = generate_weights(Y)
X = [lettercode2onehot(x) for x in X]
X = pad_sequences(X, 20*parameters.maxlen)
Y = pad_sequences(Y, parameters.maxlen, dtype='float32')
weights = pad_sequences(weights, parameters.maxlen, dtype='float32')

if __name__ == '__main__':

    # Shuffle and split the data
    (x_train, y_train, weights_train), (x_test, y_test, weights_test) = shuffle_and_split(X, Y, weights)

    # Training parameters
    batch_size = 128
    epochs = 10

    model = get_model(parameters)
    model.compile(optimizer=keras.optimizers.Adam(), loss=logcosh, metrics=[rmsd, chi2])

    model.fit(x=x_train, y=y_train, epochs=epochs, batch_size=batch_size,
              validation_data=(x_test, y_test), callbacks=[LossRatio()])
    score = model.evaluate(x_test, y_test)

    # Just some simple diagnostics
    print('Test rmsd:', score[0])
    print('Test chi2:', score[1])

    # Serialize model to JSON
    with open("model.json", "w") as fp:
        fp.write(model.to_json())

    # Serialize weights to HDF5
    model.save_weights("model.h5")
