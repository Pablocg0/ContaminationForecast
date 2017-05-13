import neuralNetwork as nn
import neuralNetworkGpu as nng
import FormatData as fd
import pandas as df
import matplotlib.pyplot as plt
from time import time

contaminant = 'O3';
loss_vec= [];
estations =['AJM','ATI','BJU','CAM','CCA','CHO','CUA','FAC','IZT','LPR','MER','MGH','NEZ','PED','SAG','SFE','SJA','TAH','TLA','UAX','UIZ','XAL'];
startDate =['2015/01/01','1994/01/02','1986/01/12','2011/07/01','2014/08/01','2007/07/20','2011/10/01','1993/01/01','2007/07/20','2011/07/01','1986/01/16','2015/01/01','2011/07/27','1986/01/16','1995/01/01','2012/02/20','2011/07/01','1995/01/01','1986/01/15','2012/02/20','1987/05/31','1986/01/10'];
endDate = '2017/02/02';
total_data;
total_build;

def estations():
    data = fd.readData(startDate[0],endDate,estations[0]);
    total_data = data;
    build = fd.buildClass(data,[estations[0]],contaminant,24);
    total_build = build;
    xy_values = fd.prepro(data,build);
    temp_loss = nng.train(xy_values[0],xy_values[1],xy_values[2]);
    loss_vec.append(temp_loss);
    i = 1;
    while i < 22 :
        print(estations[i]);
        data = fd.readData(startDate[i],endDate,estations[i]);
        build = fd.buildClass(data,[estations[i]],contaminant,24);
        total_data = df.concat([total_data, data], axis=1);
        total_build = df.concat([total_build, build], axis=1);
        total_data.fillna(value=-1);
        total_build.fillna(value=-1);
        xy_values = fd.prepro(total_data,total_build);
        temp_loss = nng.train(xy_values[0],xy_values[1],xy_values[2]);
        loss_vec.append(temp_loss);
        i= i+1;
    print(loss_vec);
    plt.plot(loss_vec, 'k-', label='Loss')
    plt.title('Error aumentando el numero de estaciones')
    plt.xlabel('Numero de estaciones')
    plt.ylabel('Loss')
    plt.legend(loc='best')
    savefig("estaciones.png")
    plt.show()

estation();
