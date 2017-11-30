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
    weight = tf.Variable(tf.random_normal(shape));
    return weight;

def init_bias(shape):
    """
    Function for the define Variable function weight
    :param shape: Matrix containing bias
    :type shape : matrix float32
    :return: matrix bias
    """
    bias=  tf.Variable(tf.random_normal(shape));
    return bias;

def fully_connected(input_layer,weight,biases):
    layer = tf.add(tf.matmul(input_layer,weight), biases);
    return tf.nn.sigmoid(layer);

def training(datax, build, estacion, dirTrain,contaminant,dirData):
    print("Entrenamiento")
    data = df.read_csv(dirData+estacion+'_'+contaminant+'.csv');
    x_vals = data.values;
    x = x_vals.shape;
    columns = x[1];
    #x_vals= x_vals[:,1:columns];
    #print(x_vals);

    x_data = tf.placeholder(shape=[None,columns-1],dtype=tf.float32);
    y_target= tf.placeholder(shape=[None,1],dtype =tf.float32);
    #--------Create the first layer (size hidden nodes)--------
    # TODO ya recibe todas las columnas en la primera capa
    weight_1 = init_weight(shape=[columns-1,columns-1]);
    bias_1 = init_bias(shape=[columns-1]);
    layer_1 = fully_connected(x_data,weight_1,bias_1);

    #--------Create the second layeprint(size);--------
    weight_2 = init_weight(shape=[columns-1,(columns-1)*2]);
    bias_2= init_bias(shape=[(columns-1)*2]);
    layer_2 = fully_connected(layer_1,weight_2, bias_2);


    #--------Create output layer (1 output value)--------
    weight_3= init_weight(shape=[(columns-1)*2,1]);
    bias_3 = init_bias(shape=[1]);
    final_output = fully_connected(layer_2,weight_3, bias_3);

    # Declare loss function (L1)
    loss= tf.reduce_mean(tf.abs(y_target - final_output));

    # Declare optimizer gradientDescent
    #my_opt = tf.train.GradientDescentOptimizer(0.1);
    my_opt = tf.train.AdamOptimizer(0.001);
    train_step = my_opt.minimize(loss);
    name = 'train_'+estacion+'_'+contaminant;
    with tf.Session() as sess:
        new_saver = tf.train.import_meta_graph(dirTrain+estacion+'/'+name+'.ckpt.meta')
        new_saver.restore(sess, dirTrain+estacion+'/'+name+'.ckpt')
        init = tf.global_variables_initializer();
        sess.run(init);
        for step in range(1000):
            sess.run(train_step, feed_dict={x_data: datax, y_target: build});
        sess.close();
