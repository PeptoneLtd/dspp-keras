from ..utils.data_utils import get_file
import numpy as np
import cPickle as pickle

def load_data(path='peptone_dspp.pkl'):
    """Loads the MNIST dataset.

    # Arguments
        path: path where to cache the dataset locally
            (relative to ~/.keras/datasets).

    # Returns
        Tuple of Numpy arrays: `(x_train, y_train), (x_test, y_test)`.
    """
    path = get_file(path, origin='https://github.com/PeptoneInc/dspp-data/blob/master/database.pkl?raw=true')
    f = np.load(path)

    f =  open(path, 'rb')
    database = pickle.load(f)
    X, Y = database['X'], database['Y']
    f.close()
    return (X, Y)
