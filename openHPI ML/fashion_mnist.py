import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras.layers import Flatten, Dense
!pip install --upgrade deeplearning2020
from deeplearning2020 import Submission
#load dataset
(train_imgs, train_lbls), (test_imgs, test_lbls) = keras.datasets.fashion_mnist.load_data()
#normalize inputs
train_imgs = train_imgs / 255
test_imgs = test_imgs / 255
#vectorize labels
train_lbls = keras.utils.to_categorical(train_lbls, 10)
test_lbls = keras.utils.to_categorical(test_lbls, 10)
#model
model = keras.Sequential([
    Flatten(input_shape=(28,28)),
    Dense(128,activation='tanh'),
    Dense(10,activation='tanh')
])
#compile, train, eval
model.compile(optimizer='sgd',loss='mean_squared_error',metrics=['accuracy'])
model.fit(train_imgs, train_lbls, epochs=15)
model.evaluate(test_imgs, test_lbls)
#submit to openHPI
Submission('40b2e133647124b0c676925cfde86748', '2', model).submit()