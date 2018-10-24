#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import numpy as np
from keras.models import Sequential
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras import optimizers
from keras import applications
from keras.models import Model
import tensorflow as tf
from keras import backend as K
from tensorflow.python.client import timeline

config = tf.ConfigProto()
# Turns on XLA JIT compilation.
jit_level = tf.OptimizerOptions.ON_1
config.graph_options.optimizer_options.global_jit_level = jit_level
run_metadata = tf.RunMetadata()
sess = tf.Session(config=config)
K.set_session(sess)


# dimensions of our images.
img_width, img_height = 256, 256

train_data_dir = 'tiny-imagenet-200/train'
validation_data_dir = 'tiny-imagenet-200/val'


##preprocessing
# used to rescale the pixel values from [0, 255] to [0, 1] interval
datagen = ImageDataGenerator(rescale=1./255)
batch_size = 128

# automagically retrieve images and their classes for train and validation sets
train_generator = datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode='binary')

validation_generator = datagen.flow_from_directory(
        validation_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode='binary')

# Small Conv Net
# a simple stack of 3 convolution layers with a ReLU activation and followed by max-pooling layers.
model = Sequential()
model.add(Convolution2D(32, (3, 3), input_shape=(img_width, img_height,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

#Training

epochs = 4
train_samples = 8032
validation_samples = 64

#jit_scope = tf.contrib.compiler.jit.experimental_jit_scope

with K.get_session()  as sess:
    run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
    model.compile(loss='MSE', optimizer='Adam', options=run_options, run_metadata=run_metadata)
    model.fit_generator(
        train_generator,
        steps_per_epoch=train_samples // batch_size,
        epochs=epochs,
        validation_data=validation_generator,
        validation_steps=validation_samples// batch_size,)
    print "model fit"
    tl = timeline.Timeline(run_metadata.step_stats)
    ctf = tl.generate_chrome_trace_format()
    with open('timeline.json', 'w') as f:
        f.write(ctf)
    model.evaluate_generator(validation_generator, validation_samples)
#About 60 seconds an epoch when using CPU

#model.save_weights('models/basic_cnn_30_epochs.h5')

#Evaluating on validation set for Computing loss and accuracy :

#model.evaluate_generator(validation_generator, validation_samples)


# In[ ]:


()

