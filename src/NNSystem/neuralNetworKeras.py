from time import time
import keras
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
from keras.callbacks import TensorBoard
from keras.utils import multi_gpu_model
#from keras.layers import Lambda, concatenate
#from keras import Model
#import keras.backend as K



def bias(y_true, y_pred):
    return K.mean(y_true - y_pred)

def variance(y_true, y_pred):
    return K.mean((y_true - y_pred)**2)

def train (x_data,y_data, columns, iteraciones, station, contaminant, dirTrain):

    name = 'train_'+station+'_'+contaminant

    x_train = x_data
    print(x_train)
    y_target = y_data
    print(y_target[0][0])

    model = Sequential()

    model.add(Dense(columns-1, activation = 'sigmoid', input_dim = columns -1, name = 'dense_1'))
    model.add(Dense((columns-1)*2, activation = 'sigmoid', name='dense_2'))
    model.add(Dense(1,activation='sigmoid', name = 'dense_3'))

    model = multi_gpu_model(model, gpus=2)


    model.compile(loss='mean_squared_error', optimizer = 'adam')
    #tensorboard = TensorBoard(log_dir="logs/" + station )
    model.fit(x_train, y_target, epochs=150, batch_size=64*4)
    model.save(dirTrain + station + '/' + name + '.h5')
    del model

