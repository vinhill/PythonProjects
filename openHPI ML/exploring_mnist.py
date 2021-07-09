import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras

data = keras.datasets.mnist
#numpy arrays of shape (60.000, 28, 28) and (10.000, 28, 28) with 0<=values<=255
(train_imgs, train_lbls), (test_imgs, test_lbls) = data.load_data()

#vectorize
train_lbls = keras.utils.to_categorical(train_lbls, 10)
test_lbls = keras.utils.to_categorical(test_lbls, 10)

#normalize
train_imgs = train_imgs / 255
test_imgs = test_imgs / 255

#model that takes 28x28 Image, with relu/sigmoid activation function
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28,28)),
    keras.layers.Dense(128,activation='relu'),
    keras.layers.Dense(10,activation='sigmoid')
])

#compile with stochastic gradient descend and MSQ
model.compile(
    optimizer='sgd',
    loss='mean_squared_error',
    metrics=['accuracy']
)

#train
model.fit(
    train_imgs,
    train_lbls,
    epochs=10,
    verbose=True
)

#evaluate
result = model.evaluate(test_imgs, test_lbls)