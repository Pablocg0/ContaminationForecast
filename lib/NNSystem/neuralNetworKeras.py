import numpy as np
import pandas as df
from time import time
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
from keras.callbacks import TensorBoard
import math
import os


def train (x_data,y_data, columns, iteraciones, station, contaminant, dirTrain):

    name = 'train_'+station+'_'+contaminant

    x_train = x_data
    y_target = y_data

    model = Sequential()

    model.add(Dense(columns-1, activation = 'sigmoid', input_dim = columns -1))
    model.add(Dense((columns-1)*2, activation = 'sigmoid'))
    model.add(Dense(1,activation='sigmoid'))

    model.compile(loss='mean_squared_error', optimizer = 'adam', metrics =['accuracy'])
    tensorboard = TensorBoard(log_dir="logs/{}".format(time()))
    model.fit(x_train, y_target, epochs=200, batch_size=10, callbacks=[tensorboard])
    model.save(dirTrain + station + '/' + name + '.h5')
