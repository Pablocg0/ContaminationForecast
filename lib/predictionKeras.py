import pandas as df
import math
import numpy as np
import os
import keras
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Activation
import tensorflow as tf


def normalize(data, station, contaminant, dirData):
    """
     Function to normalize an array of values with the minimum and the maximun that has been save in a .cvs fileName

    :param data: data to normalize
    :type data: array
    :param station : name station
    :type station: string
    """
    name = station + '_' + contaminant
    values = df.read_csv(dirData + name + '_MaxMin.csv')
    maxx = values['MAX'].values
    minn = values['MIN'].values
    valNorm = []
    i = 0
    for x in data:
        if x == -1:
            norm = 0.0
        else:
            m = float(maxx[i])
            mi = float(minn[i])
            if m == 0 and mi == 0:
                norm = 0.0
            else:
                norm = (x - mi) / (m - mi)
        valNorm.append(float(norm))
        i += 1
    return valNorm

def desNorm(data, station, contaminant, dirData,columnContaminant):
    """
     function to denormalize a value

    :param data: value to be unmasked
    :type data: float32
    :param station: name the stations
    :type station: String
    :param contaminant: name the pollutant
    :type contaminant: String
    :param dirData: address of the files with training information
    :type dirData: String
    """
    real = []
    nameC =  columnContaminant + station.lower()
    # nameC= 'cont_otres'
    name = station + '_' + contaminant
    values = df.read_csv(dirData + name + '_MaxMin.csv')
    index = values.columns[0]
    va = values[(values[index] == nameC)]
    maxx = va['MAX'].values[0]
    minn = va['MIN'].values[0]
    for x in data:
        realVal = (x * (maxx - minn)) + minn
        real.append(realVal)
    return real


def prediction(station, contaminant, arrayPred, dirTrain, dirData):

    result = []

    name = 'train_'+station+'_'+contaminant

    model = load_model(dirTrain + station + '/' + name + '.h5', {'tf': tf})

    for x in arrayPred:
        pred = model.predict(x)
        result.append(pred[0,0])
    return result
