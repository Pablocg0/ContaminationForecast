from Utilites.FormatData import FormatData
from Utilites.Utilites import converToArray as an
import numpy as np
import pandas as df
import tensorflow as tf
from sklearn.model_selection import train_test_split #installl sklearn with pip or anaconda
from sklearn import preprocessing
import matplotlib.pyplot as plt
from time import time

startDate='1992/11/09';
endDate='2017/02/01';
estations=['AJM'];
contaminant = 'O3';

name = estations[0] +'_'+contaminant;
ini = time();
#data = FormatData.readData(startDate,endDate,estations,contaminant);
#build = FormatData.buildClass2(data,['BJU'],contaminant,24,startDate,endDate);
#build = FormatData.buildClass(data,['XAL'],contaminant,24);
data = df.read_csv('data/'+name+'.csv', delim_whitespace =True);
build = df.read_csv('data/'+name+'_pred.csv',delim_whitespace = True);

x_vals = data.values;
x = x_vals.shape;

columns = x[1];
x_vals= x_vals[:,1:columns];
y_vals = an(build,contaminant);
fin = time();
# Normalize data
min_max_scaler = preprocessing.MinMaxScaler()
x_vals= min_max_scaler.fit_transform(x_vals)
min_max_scaler2 = preprocessing.MinMaxScaler()
y_vals = min_max_scaler2.fit_transform(y_vals)

# Create graph session
sess= tf.Session();

# Split data into train/test = 80%/20%
x_vals_train,x_vals_test,y_vals_train,y_vals_test = train_test_split(x_vals, y_vals, test_size=0.2);
size = len(x_vals_train);# The number of neurons in the first layer is equal to the number of columns of data

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

def final_connected(input_layer,weight,biases):
    layer = tf.add(tf.matmul(input_layer,weight), biases);
    return layer;

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
my_opt = tf.train.GradientDescentOptimizer(0.1);
train_step = my_opt.minimize(loss);

# Initialize Variables
init = tf.global_variables_initializer();
sess.run(init);

loss_vec =[];
test_loss =[];

# Training loop
initial = time();
for i in range(1000):
    #
    # TODO deje los tres entrenamiento ya que el primero entrena, la segunda nos da el error del
    #entrenamiento y el tercero es el tercero es el error del test con lo que lleva de entrenamiento
    sess.run(train_step, feed_dict={x_data: x_vals_train, y_target: y_vals_train});

    temp_loss = sess.run(loss, feed_dict={x_data: x_vals_train, y_target: y_vals_train});
    loss_vec.append(temp_loss);

    test_temp_loss= sess.run(loss, feed_dict={x_data: x_vals_test, y_target: y_vals_test });
    test_loss.append(test_temp_loss);

    if (i+1)%1000==0:
        print('Iteration: ' + str(i+1) + '. Loss = ' + str(temp_loss))

saver = tf.train.Saver();
saver.save(sess,'trainData/save')
final = time();
total_execution = final-initial;
total_dta = fin-ini;
print('tiempo de red:',total_dta);
print('Tiempo de datos: ', total_execution);
#Plot loss
prediction =sess.run(final_output, feed_dict={x_data: np.array([[14.0,7.0,-1.0,-1.0,-1.0,-1.0,-1.0,1.0,3.0,21.0]])})
print(prediction);
plt.plot(loss_vec, 'g-', label='Train Loss');
#plt.plot(test_loss, 'r--', label='Test Loss')
plt.title('Loss per Iteration',fontsize=20)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Iterations',fontsize=18)
plt.ylabel('Loss',fontsize=18)
plt.legend(loc='best')
plt.savefig('iteracionesp.png')
plt.show()
