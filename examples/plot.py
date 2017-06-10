#!/usr/bin/env python

'''
Utilities for boilerplate model with dSPP (https://peptone.io/dssp) dataset.
Peptone Inc. - The Protein Intelligence Company (https://peptone.io)
'''
from __future__ import print_function

from keras.models import model_from_json
from train import X, Y, weights
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# load YAML and create model
with open('model.json', 'r') as fp:
    model = model_from_json(fp.read())

# load weights into new model
model.load_weights("model.h5")
print("Loaded model model.h5")

# predict data
print("Predicting data...")
prediction = model.predict(X[::100])

# plot the results
print("Plotting...")
fig = plt.figure(figsize=(9*3, 9*3))
for i, (exp, weight, pred) in enumerate(zip(Y[::100], weights[::100], prediction)):
    ax = fig.add_subplot(9, 9, i+1)
    ax.plot(exp, label="propensity")
    ax.plot(pred, label="prediction")
    ax.plot(weight, label="weights")
    ax.legend()
fig.tight_layout()

fig.savefig("plot.png")
print("Plot saved as plot.png")
