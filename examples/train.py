'''
Basic convnet on the dSPP (https://peptone.io/dssp) dataset.
Peptone Inc. - The Protein Intelligence Company (https://peptone.io)
'''

from __future__ import print_function
import keras, os, time
from dsppkeras.datasets import dspp
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Reshape, Conv1D, MaxPooling1D, BatchNormalization, Activation
from keras.losses import logcosh
from utils import Struct, lettercode2onehot, shuffle_and_split, LossRatio

def get_model(config):
    """
    Build model given some initial configuration
    """
    model = Sequential()
    model.add(Dense(config.N, input_shape=(config.N,), name="Prediction"))
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

    batch_size = 8000
    epochs = 10

    # Measure time
    tic = time.time()

    model = get_model(parameters)
    model.compile(optimizer=keras.optimizers.Adam(), loss=logcosh, metrics=[rmsd, chi2], sample_weight=weights_train, sample_weight_mode="temporal")

    model.fit(x=x_train, y=y_train, epochs=epochs, batch_size=batch_size, validation_data=(x_test, y_test, weights_test), callbacks=[lossRatio()])
    score = model.evaluate(x_test, y_test, sample_weight=weights_test)

    # Measure time
    toc = time.time()

    # Just some simple diagnostics
    print()
    print('Test rmsd:', score[0])
    print('Test chi2:', score[1])

    # Output time
    print('Training time {}h {}m {}s'.format(timeit(toc-tic)[0], timeit(toc-tic)[1], timeit(toc-tic)[2]))

    # Make sure we have output directory
    if not os.path.exists("./model"):
        os.makedirs("./model")

    # Serialize model to JSON
    with open("./model/model.json", "w") as fp:
        fp.write(model.to_json())

    # Serialize weights to HDF5
    model.save_weights("./model/model.h5")
    print("Saved model to ./model/")
