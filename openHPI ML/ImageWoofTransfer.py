import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import tensorflow_datasets as tfds
import numpy as np
from tensorflow.keras.layers import Dense, Activation, Input, \
  Conv2D, MaxPooling2D, Flatten, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
import matplotlib.pyplot as plt
#!pip install --upgrade deeplearning2020
from deeplearning2020 import helpers, Submission
from deeplearning2020.datasets import ImageWoof
from tensorflow.keras.applications.xception import Xception

#load imagewoof
train_data, test_data, classes = ImageWoof.load_data()

#preprocessing
def preprocess(image, label):
    resized_image = tf.image.resize(image, [300, 300])
    preprocessed_image = tf.keras.applications.xception.preprocess_input(resized_image)
    return resized_image, label

n_classes = len(classes)

batch_size = 32

train_data = train_data.shuffle(1000).take(500) \
    .map(preprocess).batch(batch_size).prefetch(1)
test_data = test_data.take(100) \
    .map(preprocess).batch(batch_size).prefetch(1)

#Model

input = Input(shape=(300,300,3))

base_model = Xception(weights='imagenet', include_top=True, input_tensor=input)

#model = GlobalAveragePooling2D()(base_model.output)
#model = Dropout(0.5)(model)
output_layer = Dense(n_classes, activation='softmax')(base_model.output)

model = Model(base_model.input, output_layer)

model.summary()

#training
for layer in base_model.layers:
    layer.trainable = False

model.compile(
    optimizer = keras.optimizers.Adam(learning_rate=0.2),
    loss = 'sparse_categorical_crossentropy',
    metrics = ['accuracy']
)
history = model.fit(
    train_data,
    epochs=2,
    validation_data=test_data
)
"""
for layer in base_model.layers:
    layer.trainable = True

model.compile(
    optimizer = keras.optimizers.Adam(learning_rate=0.01),
    loss = 'sparse_categorical_crossentropy',
    metrics = ['accuracy']
)
history_fine = model.fit(
    training_data,
    epochs=6,
    validation_data=test_data
)
"""
#helpers.plot_two_histories(histroy, history_fine)
helpers.plot_history('Accuracy ImageWoof', history, 0)

Submission('a61fb9546e2c7c968c11fa94c44f77b2', '3', model).submit()