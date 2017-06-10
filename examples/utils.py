'''
Utilities for convnet on the dSPP (https://peptone.io/dssp) dataset.
Peptone Inc. - The Protein Intelligence Company (https://peptone.io)
'''

from keras.callbacks import Callback
from keras.layers import merge
from keras.layers.core import Lambda
from keras.models import Model
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

def lettercode2number(sequence):
    """
        Return an integer vector with amino acid identities, shifted by +1.
        We want to make sure 0 is used for padding and missing data.
    """
    one_digit = {'A': 0, 'C': 1, 'D': 2, 'E': 3, 'F': 4,'G': 5,
    'H': 6, 'I': 7, 'K': 8, 'L': 9, 'M': 10, 'N': 11,'P': 12,
     'Q': 13, 'R': 14, 'S': 15, 'T': 16, 'V': 17,'W': 18, 'Y': 19, 'X': 20}

    assert(len(sequence) >= 1)
    encoded = []
    for letter in sequence:
        encoded.append(one_digit[letter]+1)
    assert(len(encoded) == len(sequence))
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

def normalize(array):
    concatenated = np.concatenate(array)
    mean, std = concatenated.mean(), concatenated.std()
    return [ (row - mean)/std for row in array ]

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
    name="chi2_statistics")

    return stat

def timeit(t):
    """
        Compute time in h,m,s format for performance logging
    """
    m, s = divmod(t, 60)
    h, m = divmod(m, 60)
    return int(h),int(m),int(s)

def make_parallel(model, gpu_count):
    """
        A plain and naive multi-GPU implementation.
        Based on: https://github.com/kuza55/keras-extras/blob/master/utils/multi_gpu.py
    """

    def get_slice(data, idx, parts):

        # This is a necessary work-around the issue related
        # to serialization of multi-GPU model in Keras
        # without tensorflow import declaration we won't
        # be able to predict back the values from a multi-GPU model
        import tensorflow as tf

        shape = tf.shape(data)
        size = tf.concat([ shape[:1] // parts, shape[1:] ],axis=0)
        stride = tf.concat([ shape[:1] // parts, shape[1:]*0 ],axis=0)
        start = stride * idx
        return tf.slice(data, start, size)

    outputs_all = []
    for i in range(len(model.outputs)):
        outputs_all.append([])

    #Place a copy of the model on each GPU, each getting a slice of the batch
    for i in range(gpu_count):
        with tf.device('/gpu:%d' % i):
            with tf.name_scope('tower_%d' % i) as scope:

                inputs = []
                #Slice each input into a piece for processing on this GPU
                for x in model.inputs:
                    input_shape = tuple(x.get_shape().as_list())[1:]
                    slice_n = Lambda(get_slice, output_shape=input_shape, arguments={'idx':i,'parts':gpu_count})(x)
                    inputs.append(slice_n)

                outputs = model(inputs)

                if not isinstance(outputs, list):
                    outputs = [outputs]

                #Save all the outputs for merging back together later
                for l in range(len(outputs)):
                    outputs_all[l].append(outputs[l])

    # merge outputs on CPU
    with tf.device('/cpu:0'):
        merged = []
        for outputs in outputs_all:
            merged.append(merge(outputs, mode='concat', concat_axis=0))

        return Model(input=model.inputs, output=merged)
