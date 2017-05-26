# Peptone DSPP dataset and example for Keras

This is a integration/plug-in for using the DSPP dataset from Peptone Inc with Keras, a deep learning library.

## Installation

```python setup.py
```

## Getting started

Here is how to load the dataset

- X is one-hot encoded amino-acids sequence vector

- Y is the ncSPC disorder predictor (bound between -1, 1), for each sequence.

```
from dsppkeras.datasets import dspp

X, Y = dspp.load_data()
```

See the examples/ directory for an example convolutional neural network in dspp_cnn.py
