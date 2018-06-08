'''import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import tensorflow as tf
from mlxtend.preprocessing import one_hot

LEARNING_RATE = 1e-4
TRAINING_ITERATIONS = 5
DROPOUT = 0.5
BATCH_SIZE = 1
VALIDATION_SIZE = 10000

data = pd.read_csv('tocsv1.csv')
images = data.iloc[:,1:].values
images = images.astype(np.float)

images = np.multiply(images, 1.0 / 255.0)

image_size = images.shape[1]

image_width = image_height = np.ceil(np.sqrt(image_size)).astype(np.uint8)

labels_flat = data.iloc[:,0].values.ravel()
labels_count = np.unique(labels_flat).shape[0]
print(labels_count)

labels = one_hot(labels_flat)
#print(labels)
labels = labels.astype(np.uint8)
print(labels.shape)

validation_images = images[:VALIDATION_SIZE]
validation_labels = labels[:VALIDATION_SIZE]

train_images = images[VALIDATION_SIZE:]
train_labels = labels[VALIDATION_SIZE:]
#print(validation_labels)'''
import csv
csvfile = "tocsv.csv"
newcsvfile = "tocsv1.csv"
harsha=0
with open(csvfile,'r') as csvinput:
    with open(newcsvfile, 'a') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        for row in csv.reader(csvinput):
            writer.writerow([harsha]+row)
