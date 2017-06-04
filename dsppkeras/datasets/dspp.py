from ..utils.data_utils import get_file
import numpy as np
import json
import tarfile

def load_data(path='peptone_dspp.tar.gz'):
    """Loads the MNIST dataset.

    # Arguments
        path: path where to cache the dataset locally
            (relative to ~/.keras/datasets).

    # Returns
        Tuple of Numpy arrays: `(x_train, y_train), (x_test, y_test)`.
    """
    path = get_file(path, origin='https://github.com/PeptoneInc/dspp-data/blob/master/database.tar.gz?raw=true')
    tar = tarfile.open(path, "r:gz")
    #print("Open archive at {}".format(path))
    for member in tar.getmembers():
         f = tar.extractfile(member)
         if f is None: continue
         #print("Load json {}".format(f))
         database = json.load(f)
         break

    X, Y = database['X'], database['Y']
    f.close()
    X, Y = map(lambda element: np.array(list(element)), X), map(lambda element: np.array(element), Y)
    return X, Y
