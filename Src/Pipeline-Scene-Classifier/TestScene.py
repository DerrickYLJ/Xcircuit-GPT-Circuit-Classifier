# Dictionary to map index to class name
class_names = { 0 : "Architecture", 1 : "Circuit", 2 : "Misc"}

# Upload existing model and test it on a single image

import argparse
import sys
# Read argumetns via argparse
parser = argparse.ArgumentParser()
parser.add_argument("model_file", help="The model file to load")
parser.add_argument("image_file", help="The image file to test")

args = parser.parse_args()

model_file = args.model_file

# Load the model
from tensorflow import keras
model = keras.models.load_model(model_file)

# Load the image
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
img = image.load_img(args.image_file, target_size=(150, 150))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0) # Create batch axis

# Predict the image
predictions = model.predict(img_array)
score = predictions[0]
scoreSumTo1 = tf.nn.softmax(score).numpy()

# Get max index of score
max_index = np.argmax(score)
# print("Predicted class: " + class_names[max_index] + "with probability: " + str(scoreSumTo1[max_index]))

print(class_names[max_index])
