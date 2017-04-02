import FormatData
import Utilites as an
import numpy as np
import pandas as df
import tensorflow as tf
from sklearn.model_selection import train_test_split #installl sklearn with pip or anaconda
import matplotlib.pyplot as plt

startDate='2009/02/20';
endDate='2009/02/25';
estations=['MER','TAX','TLA'];
contaminant = 'NOX';

data = FormatData.readData(startDate,endDate,estations);
build = FormatData.buildClass(data,['MER'],contaminant,24);


x_vals = np.nan_to_num(data.values);

x = x_vals.shape;
columns = x[1]
x_vals= x_vals[:,1:columns];
y_vals = an.converToArray(build,contaminant);

# Normalize data
x_vals = np.nan_to_num(an.normalize_array(x_vals));
y_vals = np.nan_to_num(an.normalize_cols(y_vals));

# Create graph session
sess= tf.Session();

# Split data into train/test = 80%/20%
x_vals_train,x_vals_test,y_vals_train,y_vals_test = train_test_split(x_vals, y_vals, test_size=0.2)
size = len(x_vals_train);# The number of neurons in the first layer is equal to the number of columns of data
# Declare batch size
batch_size= 20;

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

# Initialize placeholders
x_data = tf.placeholder(shape=[None,columns-1],dtype=tf.float32);
y_target= tf.placeholder(shape=[None,1],dtype =tf.float32);


def fully_connected(input_layer,weight,biases):
    layer = tf.add(tf.matmul(input_layer,weight), biases);
    return tf.nn.sigmoid(layer);

#--------Create the first layer (size hidden nodes)--------
# TODO ya recibe todas las columnas en la primera capa
weight_1 = init_weight(shape=[columns-1,size]);
bias_1 = init_bias(shape=[size]);
layer_1 = fully_connected(x_data,weight_1,bias_1);

#--------Create the second layeprint(size);
print(columns-1);
print(x_vals_test.shape);
print(y_vals_train.shape);
print(y_vals_test.shape);r (size*2 hidden nodes)--------
weight_2 = init_weight(shape=[size,size*2]);
bias_2= init_bias(shape=[size*2]);
layer_2 = fully_connected(layer_1,weight_2, bias_2);


#--------Create output layer (1 output value)--------
weight_3= init_weight(shape=[size*2,1]);
bias_3 = init_bias(shape=[1]);
final_output = fully_connected(layer_2,weight_3, bias_3);

# Declare loss function (L1)
loss= tf.reduce_mean(tf.abs(y_target - final_output));

# Declare optimizer gradientDescent
my_opt = tf.train.GradientDescentOptimizer(0.001);
train_step =  my_opt.minimize(loss);

# Initialize Variables
init = tf.global_variables_initializer();
sess.run(init);

loss_vec =[];
test_loss =[];

# Training loop
for i in range(1000):
    #random data for x_values and y_values

    # TODO esto es necesario, no habia entendido bien por que se hace esto, no es que se este cambiando
    # en cada iteracion los datos con los que se entrena, si no que en cada iteracion se van a agregando datos,
    # entonces batch_size es el tamaño de datos que queremos que se vaya dado en cada iteracion.

    rand_index = np.random.choice(len(x_vals_train), size= batch_size);
    rand_x = x_vals_train[rand_index];
    rand_y = y_vals_train[rand_index];

    #
    # TODO deje los tres entrenamiento ya que el primero entrena, la segunda nos da el error del
    #entrenamiento y el tercero es el tercero es el error del test con lo que lleva de entrenamiento
    sess.run(train_step, feed_dict={x_data: rand_x, y_target: rand_y});

    temp_loss = sess.run(loss, feed_dict={x_data: rand_x, y_target: rand_y});
    loss_vec.append(temp_loss);

    test_temp_loss= sess.run(loss, feed_dict={x_data: x_vals_test, y_target: y_vals_test });
    test_loss.append(test_temp_loss);

    if (i+1)%200==0:
        print('Iteration: ' + str(i+1) + '. Loss = ' + str(temp_loss))

# Plot loss
plt.plot(loss_vec, 'k-', label='Train Loss')
plt.plot(test_loss, 'r--', label='Test Loss')
plt.title('Loss per Iteration')
plt.xlabel('Iterations')
plt.ylabel('Loss')
plt.show()
