from keras.models import model_from_json
from dspp_cnn import X, Y, weights
from dsppkeras.datasets import dspp

# load YAML and create model
with open('model.json', 'r') as fp:
    model = model_from_json(fp.read())
# load weights into new model
model.load_weights("model.h5")
print("Loaded model from disk")

prediction = model.predict(X[::100])

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(9*3, 9*3))
for i, (exp, w, pred) in enumerate(zip(Y[::100], weights[::100], prediction)):
    ax = fig.add_subplot(9,9,i+1)
    ax.plot(exp, label="ncSPC")
    ax.plot(pred, label="predicion")
    ax.plot(w, label="weights")
    ax.legend()
    ax.set_xlim(0,250)
fig.tight_layout()
fig.savefig("model/plot.png")
