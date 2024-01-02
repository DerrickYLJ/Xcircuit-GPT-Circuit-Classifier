import tensorflow as tf
from tensorflow import keras
import numpy as np
import argparse

# argparse
ap = argparse.ArgumentParser()

# add argument for image to process (required)
ap.add_argument("-i", "--image", required=True,
                help="path to input image")

# add argument for model to use (required)
ap.add_argument("-m", "--model", required=True,
                help="path to model")

# load saved tensorflow model Xception.h5
model = keras.models.load_model(ap.m)

# predict on a single image
img = keras.preprocessing.image.load_img(
    ap.i, target_size=(150, 150)
)
img_array = keras.preprocessing.image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)  # Create batch axis
predictions = model.predict(img_array)
score = tf.nn.softmax(predictions[0])
