import numpy as np
import pandas as df
import tensorflow as tf
from sklearn.model_selection import train_test_split #installl sklearn with pip or anaconda


def init_weight(shape):
    """
    Function for the define Variable function weight
    :param shape: Matrix containing weight
    :type shape : matrix float32

    :return: matrix weight
    """
    with tf.device("/cpu:0"):
        weight = tf.Variable(tf.random_normal(shape));
        return weight;

def init_bias(shape):
    """
    Function for the define Variable function weight
    :param shape: Matrix containing bias
    :type shape : matrix float32
    :return: matrix bias
    """
    with tf.device("/cpu:0"):
        bias=  tf.Variable(tf.random_normal(shape));
        return bias;

def train(x_d,y_data, columns,iteraciones,station,contaminant):
    name = 'train_'+station+'_'+contaminant;
    # Create graph session
    sess= tf.Session();

    # Initialize placeholders
    with tf.device("/cpu:0"):
        x_data = tf.placeholder(shape=[None,columns-1],dtype=tf.float32);
        y_target= tf.placeholder(shape=[None,1],dtype =tf.float32);

    def fully_connected(input_layer,weight,biases):
        with tf.device("/gpu:0"):
            layer = tf.add(tf.matmul(input_layer,weight), biases);
            return tf.nn.sigmoid(layer);           

    #--------Create the first layer (size hidden nodes)--------
    # TODO ya recibe todas las columnas en la primera capa
    with tf.device("/gpu:0"):
        weight_1 = init_weight(shape=[columns-1,columns-1]);
        bias_1 = init_bias(shape=[columns-1]);
        layer_1 = fully_connected(x_data,weight_1,bias_1);

    #--------Create the second layeprint(size);--------
    with tf.device("/gpu:1"):
        weight_2 = init_weight(shape=[columns-1,(columns-1)*2]);
        bias_2= init_bias(shape=[(columns-1)*2]);
        layer_2 = fully_connected(layer_1,weight_2, bias_2);


    #--------Create output layer (1 output value)--------
    with tf.device("/gpu:2"):
        weight_3= init_weight(shape=[(columns-1)*2,1]);
        bias_3 = init_bias(shape=[1]);
        final_output = fully_connected(layer_2,weight_3, bias_3);

    # Declare loss function (L1)
    with tf.device("/gpu:3"):
        loss= tf.reduce_mean(tf.abs(y_target - final_output));

    # Declare optimizer gradientDescent
    with tf.device("/gpu:0"):
        #my_opt = tf.train.GradientDescentOptimizer(0.1);
        my_opt = tf.train.AdamOptimizer(0.001);
        train_step = my_opt.minimize(loss);

    # Initialize Variables
    init = tf.global_variables_initializer();
    saver = tf.train.Saver();
    sess.run(init);
    loss_vec =[];

    # Training loop
    for i in range(iteraciones):
        #
        # TODO deje los tres entrenamiento ya que el primero entrena, la segunda nos da el error del
        #entrenamiento y el tercero es el tercero es el error del test con lo que lleva de entrenamiento
        sess.run(train_step, feed_dict={x_data: x_d, y_target: y_data});

        temp_loss = sess.run(loss, feed_dict={x_data: x_d, y_target: y_data});
        loss_vec.append(temp_loss);

        #test_temp_loss= sess.run(loss, feed_dict={x_data: x_vals_test, y_target: y_vals_test });
        #test_loss.append(test_temp_loss);

        if (i+1)%iteraciones==0:
            total_loss = temp_loss;

    saver.save(sess,'trainData/TrainCC/'+station+'/'+name+'.ckpt')
    sess.close()
    #return total_loss;
