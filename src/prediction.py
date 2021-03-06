'''
File name : prediction.py
Author: Pablo Camacho Gonzalez
Python version: 3.6.4
Date last modified: 27/02/2018
'''

import tensorflow as tf
import pandas as df


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
                #norm = (x - 0) / (m - 0)
        valNorm.append(float(norm))
        i += 1
    return valNorm


def desNorm(data, station, contaminant, dirData, columnContaminant):
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
    nameC = columnContaminant + station.lower()
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


def init_weight(shape):
    """
     Function for the define Variable function weight

    :param shape: Matrix containing weight
    :type shape : matrix float32
    :return: matrix weight
    """
    weight = tf.Variable(tf.random_normal(shape))
    return weight


def init_bias(shape):
    """
     Function for the define Variable function weight

    :param shape: Matrix containing bias
    :type shape : matrix float32
    :return: matrix bias
    """
    bias = tf.Variable(tf.random_normal(shape))
    return bias


def fully_connected(input_layer, weight, biases):
    layer = tf.add(tf.matmul(input_layer, weight), biases)
    return tf.nn.sigmoid(layer)


def prediction(station, contaminant, arrayPred, dirTrain, dirData):
    """
     Function to obtain a prediction of a neural network that has
    already been trained previously

    :param station: station name for the prediction
    :type station: string
    :param contaminant: contaminant for the predictiondate
    :type contaminant: string
    :return: value for the prediction
    """
    result = []
    name = 'train_' + station + '_' + contaminant + ''
    data = df.read_csv(dirData + station + '_' + contaminant + '.csv')
    x_vals = data.values
    x = x_vals.shape
    columns = x[1]
    '#x_vals= x_vals[:,1:columns];'

    x_data = tf.placeholder(shape=[None, columns - 1], dtype=tf.float32)
    y_target = tf.placeholder(shape=[None, 1], dtype=tf.float32)
    '--------Create the first layer (size hidden nodes)--------'
    # TODO ya recibe todas las columnas en la primera capa
    weight_1 = init_weight(shape=[columns - 1, columns - 1])
    bias_1 = init_bias(shape=[columns - 1])
    layer_1 = fully_connected(x_data, weight_1, bias_1)

    '--------Create the second layeprint(size);--------'
    weight_2 = init_weight(shape=[columns - 1, (columns - 1) * 2])
    bias_2 = init_bias(shape=[(columns - 1) * 2])
    layer_2 = fully_connected(layer_1, weight_2, bias_2)

    '--------Create output layer (1 output value)--------'
    weight_3 = init_weight(shape=[(columns - 1) * 2, 1])
    bias_3 = init_bias(shape=[1])
    final_output = fully_connected(layer_2, weight_3, bias_3)

    # Declare loss function (L1)
    loss = tf.reduce_mean(tf.abs(y_target - final_output))

    # Declare optimizer gradientDescent
    #my_opt = tf.train.GradientDescentOptimizer(0.1)
    my_opt = tf.train.AdamOptimizer(0.001)
    train_step = my_opt.minimize(loss)
    with tf.Session() as sess:
        #saver = tf.train.import_meta_graph(dirTrain + station + '/' + name + '-1000.meta')
        saver = tf.train.Saver()
        print(dirTrain + station+"/")
        saver.restore(sess, tf.train.latest_checkpoint(dirTrain + station + '/'))# load training
        #sess.run(tf.global_variables_initializer())
        # print(sess.run(final_output, feed_dict={x_data:values}));
        for x in arrayPred:
            r = sess.run(final_output, feed_dict={x_data: x})
            result.append(r[0, 0])
        sess.close()
        return result
