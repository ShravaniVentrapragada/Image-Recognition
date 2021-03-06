# -*- coding: utf-8 -*-
"""transfer_Learning_vgg16.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ctg7Ys-VbYfSs64fvciwF_Td6Pdze6E0

Name: Snigdha Labh

PRN:17070123105

G-5(2017-21)

### 1) Create Image Paths
"""

import os
from os.path import join


hot_dog_image_dir = '../input/hot-dog-not-hot-dog/seefood/train/hot_dog'

hot_dog_paths = [join(hot_dog_image_dir,filename) for filename in 
                            ['1000288.jpg',
                             '127117.jpg']]

not_hot_dog_image_dir = '../input/hot-dog-not-hot-dog/seefood/train/not_hot_dog'
not_hot_dog_paths = [join(not_hot_dog_image_dir, filename) for filename in
                            ['823536.jpg',
                             '99890.jpg']]

img_paths = hot_dog_paths + not_hot_dog_paths

from IPython.display import Image, display
from learntools.deep_learning.decode_predictions import decode_predictions
import numpy as np
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing.image import load_img, img_to_array


image_size = 224

def read_and_prep_images(img_paths, img_height=image_size, img_width=image_size):
    imgs = [load_img(img_path, target_size=(img_height, img_width)) for img_path in img_paths]
    img_array = np.array([img_to_array(img) for img in imgs])
    output = preprocess_input(img_array)
    return(output)


my_model = ResNet50(weights='../input/resnet50/resnet50_weights_tf_dim_ordering_tf_kernels.h5')
test_data = read_and_prep_images(img_paths)
preds = my_model.predict(test_data)

most_likely_labels = decode_predictions(preds, top=3)

"""### 3) Visualize Predictions"""

for i, img_path in enumerate(img_paths):
    display(Image(img_path))
    print(most_likely_labels[i])

"""### 4) Set Up Code Checking
As a last step before writing your own code, run the following cell to enable feedback on your code.
"""

# Set up code checking
from learntools.core import binder
binder.bind(globals())
from learntools.deep_learning.exercise_3 import *
print("Setup Complete")

def is_hot_dog(preds):
    '''
    inputs:
    preds_array:  array of predictions from pre-trained model

    outputs:
    is_hot_dog_list: a list indicating which predictions show hotdog as the most likely label
    '''
    decoded = decode_predictions(preds, top=1)
    labels = [d[0][1] for d in decoded]
    out = [ I == 'hotdog' for I in labels]
    return out
    pass
    
# Check your answer
q_1.check()

def calc_accuracy(model, paths_to_hotdog_images, paths_to_other_images):
    num_hot_dog_images = len(paths_to_hotdog_images)
    num_other_images = len(paths_to_other_images)
    
    hotdog_image_data = read_and_prep_images(paths_to_hotdog_images)
    preds_for_hotdogs = model.predict(hotdog_image_data)
    
    correct_hot_preds = sum(is_hot_dog(preds_for_hotdogs))
    
    other_image_data = read_and_prep_images(paths_to_other_images)
    preds_other_images = model.predict(other_image_data)
    num_correct_other_image_preds = num_other_images - sum(is_hot_dog(preds_other_images))
    
    total_correct = correct_hot_preds + num_correct_other_image_preds
    total_preds = num_hot_dog_images + num_other_images
    return total_correct/total_preds
    
    pass

# Code to call calc_accuracy.  my_model, hot_dog_paths and not_hot_dog_paths were created in the setup code
my_model_accuracy = calc_accuracy(my_model, hot_dog_paths, not_hot_dog_paths)
print("Fraction correct in small test set: {}".format(my_model_accuracy))

# Check your answer
q_2.check()

# import the model
from tensorflow.keras.applications import VGG16


vgg16_model = VGG16(weights = '../input/vgg16/vgg16_weights_tf_dim_ordering_tf_kernels.h5')
# calculate accuracy on small dataset as a test
vgg16_accuracy = calc_accuracy (vgg16_model, hot_dog_paths,not_hot_dog_paths)

print("Fraction correct in small dataset: {}".format(vgg16_accuracy))

# Check your answer
q_3.check()

!wget -nc https://raw.githubusercontent.com/brpy/colab-pdf/master/colab_pdf.py
from colab_pdf import colab_pdf
colab_pdf('transfer_Learning_vgg16.ipynb')