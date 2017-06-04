from keras.models import model_from_json
from dspp_cnn import parameters, normalize, pad
from dsppkeras.datasets import dspp

X, Y = dspp.load_data()
X = pad(X, 20*parameters.N)
Y = pad(normalize(Y), parameters.N)

# load YAML and create model
with open('model.json', 'r') as fp:
    model = model_from_json(fp.read())
# load weights into new model
model.load_weights("model.h5")
print("Loaded model from disk")

prediction = model.predict(X[::100])

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(4, prediction.shape[0]*3))
for i, (obs, exp) in enumerate(zip(Y[::100], prediction)):
    ax = fig.add_subplot(prediction.shape[0],1,i+1)
    ax.plot(obs, label="obs")
    ax.plot(exp, label="exp")
    ax.legend()
    ax.set_xlim(0,200)
fig.tight_layout()
fig.savefig("plot.png")
