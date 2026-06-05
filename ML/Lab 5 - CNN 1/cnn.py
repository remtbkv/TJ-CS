import os
import warnings
# hide annoying messages
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
warnings.filterwarnings('ignore', message='Your `PyDataset` class should call')

import numpy as np
import matplotlib.pyplot as plt
from math import ceil
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Input
from keras.src.legacy.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from keras.utils import to_categorical
from keras.datasets import mnist


def dogscats_cnn(epochs=25):
    classifier=Sequential()

    train_datagen = ImageDataGenerator(rescale = 1./255, shear_range = 0.2, zoom_range = 0.2, horizontal_flip = True) 
    test_datagen = ImageDataGenerator(rescale=1./255)

    training_set = train_datagen.flow_from_directory('dogscats/images', target_size=(64, 64), batch_size=32, class_mode='binary') 
    test_set = test_datagen.flow_from_directory('dogscats/valid', target_size=(64, 64), batch_size=32, class_mode='binary') 

    classifier.add(Input(shape=(64, 64, 3)))
    classifier.add(Conv2D(32, (3, 3), activation='relu'))
    classifier.add(MaxPooling2D(pool_size=(2,2)))
    classifier.add(Flatten())
    classifier.add(Dense(units=128, activation='relu'))
    classifier.add(Dense(units=1, activation='sigmoid'))

    classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    history = classifier.fit(training_set, steps_per_epoch=ceil(training_set.samples/32), epochs=epochs, validation_data=test_set, validation_steps=ceil(test_set.samples/32))

    return classifier, history

def mnist_cnn():
    # change dataset
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train = x_train.reshape(-1, 28, 28, 1).astype('float32') / 255
    x_test = x_test.reshape(-1, 28, 28, 1).astype('float32') / 255
    y_train = to_categorical(y_train, num_classes=10)
    y_test = to_categorical(y_test, num_classes=10)

    classifier = Sequential()
    classifier.add(Input(shape=(28, 28, 1)))  # different input shape
    classifier.add(Conv2D(32, (3, 3), activation='relu'))
    classifier.add(MaxPooling2D(pool_size=(2, 2)))
    classifier.add(Flatten())
    classifier.add(Dense(units=128, activation='relu'))
    classifier.add(Dense(units=10, activation='softmax')) # now softmax
    classifier.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy']) # now CCE

    history = classifier.fit(x_train, y_train, epochs=10, batch_size=32, validation_data=(x_test, y_test))
    return classifier, history

def show_plot(history):
    plt.figure(figsize=(8, 5))
    plt.plot([i for i in history.history['accuracy'] if i > 0], label='Training')
    plt.plot(history.history['val_accuracy'], label='Validation')

    plt.title('Model Accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')

    plt.legend()
    plt.show()


# RUN FOR PART 1 GRAPHS
classifier, history = dogscats_cnn()

show_plot(history)

# RU FOR PART 2 GRAPHS
# classifier, history = mnist_cnn()


