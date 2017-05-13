import neuralNetworkGpu as nng
import FormatData
import Utilites as an
import pandas as df
import matplotlib.pyplot as plt
from time import time

contaminant = 'O3';
loss_vec= [];
est =['AJM','ATI','BJU','CAM','CCA','CHO','CUA','FAC','IZT','LPR','MER','MGH','NEZ','PED','SAG','SFE','SJA','TAH','TLA','UAX','UIZ','XAL'];
startDate =['2015/01/01','1994/01/02','1986/01/12','2011/07/01','2014/08/01','2007/07/20','2011/10/01','1993/01/01','2007/07/20','2011/07/01','1986/01/16','2015/01/01','2011/07/27','1986/01/16','1995/01/01','2012/02/20','2011/07/01','1995/01/01','1986/01/15','2012/02/20','1987/05/31','1986/01/10'];
endDate = '2017/02/02';

def estations():
    estation= est[0];
    start = startDate[0];
    data = FormatData.readData(start,endDate,[estation]);
    total_data = data;
    build = FormatData.buildClass(data,[estation],contaminant,24);
    total_build = build;
    xy_values = an.prepro(data,build, contaminant);
    temp_loss = nng.train(xy_values[0],xy_values[1],xy_values[2]);
    loss_vec.append(temp_loss);
    i = 1;
    while i < 22 :
        print(est[i]);
        estation= est[0];
        data = FormatData.readData(startDate[i],endDate,[estation]);
        print(data);
        build = FormatData.buildClass(data,[estation],contaminant,24);
        total_data = df.concat([total_data, data], axis=1);
        total_build = df.concat([total_build, build], axis=1);
        total_data.fillna(value=-1);
        total_build.fillna(value=-1);
        xy_values = an.prepro(total_data,total_build);
        temp_loss = nng.train(xy_valuessize[0],xy_values[1],xy_values[2]);
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

estations();
