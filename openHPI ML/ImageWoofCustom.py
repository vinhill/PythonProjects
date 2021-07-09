import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import tensorflow_datasets as tfds
import numpy as np
from tensorflow.keras.layers import Dense, Activation, Input, \
  Conv2D, MaxPooling2D, Flatten, BatchNormalization
from tensorflow.keras.models import Model
import matplotlib.pyplot as plt
#!pip install --upgrade deeplearning2020
from deeplearning2020 import helpers, Submission
from deeplearning2020.datasets import ImageWoof

#load imagewoof
train_data, test_data, classes = ImageWoof.load_data()

#preprocessing
def preprocess(image, label):
    resized_image = tf.image.resize(image/255, [300, 300])
    return resized_image, label

n_classes = len(classes)

batch_size = 32
train_data = train_data.shuffle(1000)

train_data = train_data.map(preprocess) \
  .batch(batch_size).prefetch(1)          
test_data = test_data.map(preprocess) \
  .batch(batch_size).prefetch(1)

#model
learning_rate=0.001
momentum=0.9
activation='elu'

input_layer = Input(shape=(300, 300, 3))
model = BatchNormalization(axis=[1,2])(input_layer)

model = Conv2D(
    filters=32,
    kernel_size=(7,7),
    strides=(2,2),
    activation=activation
)(model)
model = BatchNormalization(axis=[1,2])(model)
model = MaxPooling2D((2,2))(model)

model = Conv2D(
    filters = 64, 
    kernel_size=(3,3), 
    activation=activation
)(model)
model = BatchNormalization(axis=[1,2])(model)
model = MaxPooling2D((2,2))(model)

model = Conv2D(
    filters = 64, 
    kernel_size=(3,3), 
    activation=activation
)(model)
model = BatchNormalization(axis=[1,2])(model)
model = MaxPooling2D((2,2))(model)

model = Conv2D(
    filters = 96, 
    kernel_size=(3,3), 
    activation=activation
)(model)
model = BatchNormalization(axis=[1,2])(model)
model = MaxPooling2D((2,2))(model)

model = Conv2D(
    filters = 96, 
    kernel_size=(3,3), 
    activation=activation
)(model)
model = BatchNormalization(axis=[1,2])(model)

model = Flatten()(model)
model = Dense(
    200,
    activation=activation
)(model)

model = Dense(
    100,
    activation='tanh'
)(model)

output = Dense(n_classes, activation="softmax")(model)

CNN_model = Model(input_layer, output)

CNN_model.summary()

#compiling
optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
CNN_model.compile(
    loss="sparse_categorical_crossentropy",
    optimizer=optimizer,
    metrics=["accuracy"]
)

#training
history = CNN_model.fit(
    train_data,
    epochs=2,
    validation_data=test_data
)
helpers.plot_history('Accuracy ImageWoof', history, 0)

Submission('a61fb9546e2c7c968c11fa94c44f77b2', '3', CNN_model).submit()