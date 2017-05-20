from Utilites.Utilites import prepro as an
from Utilites.FormatData import FormatData as fd
from tests.neuralNetwork import train as nn
import pandas as df
import tensorflow as tf

est =['AJM','ATI','BJU','CAM','CCA','CHO','CUA','FAC','IZT','LPR','MER','MGH','NEZ','PED','SAG','SFE','SJA','TAH','TLA','UAX','UIZ','XAL'];
contaminant = 'O3';


def trainNeuralNetworks():
    i=0;
    while i <= 2:
        station = est[i];
        print(station);
        name = station +'_'+contaminant;
        data = df.read_csv('data/'+name+'.csv', delim_whitespace =True);
        build = df.read_csv('data/'+name+'_pred.csv',delim_whitespace = True);
        xy_values = an(data,build, contaminant);
        nn(xy_values[0],xy_values[1],xy_values[2],1000,station,contaminant);
        i+=1;


def prediction(station, date,contaminant):
    name = 'train_'+station+'_'+contaminant;
    data = fd.readData(date,date,[station],contaminant);
    x_vals = data.values;
    x = x_vals.shape;
    columns = x[1];
    x_vals= x_vals[:,1:columns];
    print(x_vals);
    #session= tf.Session();
    #x_data = tf.placeholder(shape=[None,columns-1],dtype=tf.float32);
    #y_target= tf.placeholder(shape=[None,1],dtype =tf.float32);
    #init = tf.global_variables_initializer();
    #with tf.Session() as session:
    #    tf.train.Saver.restore(session,'trainData/'+station+'/'+name,'trainData/'+station+'/'+name);
    #    prediction=sess.run(final_output, feed_dict={x_data:x_vals})
    #print(prediction);

#trainNeuralNetworks();
prediction('BJU','2016/01/08','O3');
