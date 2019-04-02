'''
File name : autoTraining.py
Author: Pablo Camacho Gonzalez
Python version: 3.6.4
Date last modified: 27/02/2018
'''

import numpy as np
import tensorflow as tf
import pandas as df


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


def training(datax, build, estacion, dirTrain, contaminant, dirData):
    """
    function where the neural network is defined and trained

    :param x_d: Training data
    :type x_d: matrix float32
    :param y_data: predicction data (Training data)
    :type y_data: matrix float32
    :param columns: number of columns in the matrix with training data
    :type columns: int
    :param iteraciones: number of iteration that the neural network will be trained
    :type iteraciones: int
    :param station: name of the station that will train the neural network
    :type station: String
    :param contaminant: name of the pollutant that the neural network will predict
    :type contaminant: String
    :param dirTrain: address where the training is kept
    :type dirTrain: String
    """
    print("Entrenamiento")
    data = df.read_csv(dirData + estacion + '_' + contaminant + '.csv')
    x_vals = data.values
    x = x_vals.shape
    columns = x[1]
    # x_vals= x_vals[:,1:columns];
    # print(x_vals);

    x_data = tf.placeholder(shape=[None, columns - 1], dtype=tf.float32)
    y_target = tf.placeholder(shape=[None, 1], dtype=tf.float32)
    # --------Create the first layer (size hidden nodes)--------
    # TODO ya recibe todas las columnas en la primera capa
    weight_1 = init_weight(shape=[columns - 1, columns - 1])
    bias_1 = init_bias(shape=[columns - 1])
    layer_1 = fully_connected(x_data, weight_1, bias_1)

    # --------Create the second layeprint(size);--------
    weight_2 = init_weight(shape=[columns - 1, (columns - 1) * 2])
    bias_2 = init_bias(shape=[(columns - 1) * 2])
    layer_2 = fully_connected(layer_1, weight_2, bias_2)

    # --------Create output layer (1 output value)--------
    weight_3 = init_weight(shape=[(columns - 1) * 2, 1])
    bias_3 = init_bias(shape=[1])
    final_output = fully_connected(layer_2, weight_3, bias_3)

    # Declare loss function (L1)
    loss = tf.reduce_mean(tf.abs(y_target - final_output))

    # Declare optimizer gradientDescent
    # my_opt = tf.train.GradientDescentOptimizer(0.1)
    my_opt = tf.train.AdamOptimizer(0.001)
    train_step = my_opt.minimize(loss)
    name = 'train_' + estacion + '_' + contaminant
    with tf.Session() as sess:
         #saver = tf.train.Saver()
         saver = tf.train.import_meta_graph(dirTrain + estacion + '/' + name + '-1000.meta')
         saver.restore(sess, tf.train.latest_checkpoint(dirTrain + estacion + '/'))# load training
         init = tf.global_variables_initializer();
         sess.run(init);
         for step in range(1000):
             sess.run(train_step, feed_dict={x_data: datax, y_target: build});

         saver.save(sess, dirTrain + estacion + '/' + name, global_step= step+1, write_meta_graph=False)
         sess.close();
