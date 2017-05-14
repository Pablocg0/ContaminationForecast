import neuralNetworkGpu as nng
import FormatData
import Utilites as an
import pandas as df
import matplotlib.pyplot as plt
from time import time

contaminant = 'O3';
loss_vec= [];
est =['AJM','ATI','BJU','CAM','CCA','CHO','CUA','FAC','IZT','LPR','MER','MGH','NEZ','PED','SAG','SFE','SJA','TAH','TLA','UAX','UIZ','XAL'];
startDate =['2015/01/01','2013/01/26','1992/11/09','2011/07/01','2014/08/01','2007/07/20','1994/01/02','1990/08/07','2007/07/20','2011/07/05','1986/11/01','2015/01/01','2011/07/27','1986/01/17','1986/02/20','2012/02/20','2011/07/01','1994/01/02','1986/11/01','2012/02/20','1990/05/16','1986/11/22'];
endDate = '2017/02/02';

def estations():
    start =startDate[0];
    estation = [];
    for x in est:
        estation += [x];
        print(estation);
        data = FormatData.readData(start,endDate,estation);
        build = FormatData.buildClass(data,[est[0]],contaminant,24);
        xy_values = an.prepro(data,build, contaminant);
        temp_loss = nng.train(xy_values[0],xy_values[1],xy_values[2],1000);
        loss_vec.append(temp_loss);
    print(loss_vec);
    plt.plot(loss_vec, 'k-', label='Loss')
    plt.title('Error aumentando el numero de estaciones')
    plt.xlabel('Numero de estaciones')
    plt.ylabel('Loss')
    plt.legend(loc='best')
    plt.savefig("/estaciones.png");

def iteration():
    i = 200
    start =startDate[10];
    estation= est[10];
    data = FormatData.readData(start,endDate,[estation]);
    build = FormatData.buildClass(data,[est[10]],contaminant,24);
    xy_values = an.prepro(data,build, contaminant);
    while i <= 3000:
        temp_loss = nng.train(xy_values[0],xy_values[1],xy_values[2],i);
        loss_vec.append(temp_loss);
        i = i + 200;
        print(i);
    print(loss_vec);
    plt.plot(loss_vec, 'k-', label='Loss')
    plt.title('Error aumentando el numero de iteraciones de entrenamiento')
    plt.xlabel('Numero de iteraciones')
    plt.ylabel('Loss')
    plt.legend(loc='best')
    plt.savefig("/iteraciones.png");

def estac2():
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
        estation= est[i];
        data = FormatData.readData(startDate[i],endDate,[estation]);
        build = FormatData.buildClass(data,[estation],contaminant,24);
        total_data = df.concat([total_data, data], axis=1);
        total_build = df.concat([total_build, build], axis=1);
        total_data.fillna(value=-1);
        total_build.fillna(value=-1);
        xy_values = an.prepro(total_data,total_build,contaminant);
        temp_loss = nng.train(xy_valuessize[0],xy_values[1],xy_values[2]);
        loss_vec.append(temp_loss);
        i= i+1;
    print(loss_vec);
    plt.plot(loss_vec, 'k-', label='Loss')
    plt.title('Error aumentando el numero de estaciones')
    plt.xlabel('Numero de estaciones')
    plt.ylabel('Loss')
    plt.legend(loc='best')
    savefig("/estaciones.png")
    plt.show()

def main():
    option = int(input("Escoga opcion a ejecutar \n 1.Numero de estaciones \n 2.Numero de iteraciones \n 3.Ambas"));
    if option == 1:
        estations();
    elif option == 2:
        iteration();
    elif option == 3:
        estations();
        iteration();
    else:
        print("opcion incorrecta");

if __name__ == '__main__':
    main()
