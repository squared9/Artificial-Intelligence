import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Activation
import keras
import string


# TODO: fill out the function below that transforms the input series 
# and window-size into a set of input/output pairs for use with our RNN model
def window_transform_series(series, window_size):
    # containers for input/output pairs
    X = []
    y = []

    n = len(series)

    for i in range(n - window_size):
        X.append(series[i:i + window_size])
        y.append(series[i + window_size])

    # reshape each 
    X = np.asarray(X)
    X.shape = (np.shape(X)[0:2])
    y = np.asarray(y)
    y.shape = (len(y),1)
    
    return X,y


def build_part1_RNN(window_size):
    model = Sequential()
    model.add(LSTM(5, input_shape=(window_size, 1)))
    # model.add(Dropout(0.5))
    model.add(Dense(1, activation=None))
    return model


def cleaned_text(text):
    # remove as many non-english characters and character sequences as you can 
    # but don't remove the punctuation given below

    punctuation = ['!', ',', '.', ':', ';', '?']

    allowed_characters = set(punctuation).union(set(string.ascii_letters)).union(set(' '))
    # .union(set(string.digits))  # uncomment for numbers

    unique_characers = set(text)

    for c in unique_characers:
        if c not in allowed_characters:
            text = text.replace(c, '')
    return text


def window_transform_text(text, window_size, step_size):
    # containers for input/output pairs
    inputs = []
    outputs = []
    
    n = len(text)

    for i in range(0, n - window_size, step_size):
        inputs.append(text[i:i + window_size])
        outputs.append(text[i + window_size])

    return inputs,outputs


# a single LSTM hidden layer with softmax activation, categorical_crossentropy loss
def build_part2_RNN(window_size, num_chars):
    model = Sequential()
    model.add(LSTM(200, input_shape=(window_size, num_chars)))
    # model.add(Dropout(0.5))
    model.add(Dense(num_chars, activation='linear'))
    model.add(Activation("softmax"))
    return model
