from tests.neuralNetworkGpu import train as nng
from tests.neuralNetwork import train as nn
from Utilites.FormatData import FormatData
from Utilites.Utilites import Utilites as an
from datetime import datetime, timedelta
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
        temp_loss = nn.train(xy_values[0],xy_values[1],xy_values[2],1000);
        loss_vec.append(temp_loss);
    print(loss_vec);
    plt.plot(loss_vec, 'k-', label='Loss')
    plt.title('Error aumentando el numero de estaciones')
    plt.xlabel('Numero de estaciones')
    plt.ylabel('Loss')
    plt.legend(loc='best')
    plt.savefig("/estaciones.png");

def estationsGpu():
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
        temp_loss = nn.train(xy_values[0],xy_values[1],xy_values[2],i);
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

def iterationGpu():
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


def time():
    time_cpu =[];
    time_gpu =[];
    start  = datetime.strptime(startDate[21],'%Y/%m/%d')
    end = datetime.strptime(endDate,'%Y/%m/%d')
    dy= 8760 * 2;
    estation = est[21];
    date = start + timedelta(hours = dy);
    while date <= end:
        print(date);
        data = FormatData.readData(start,date,[estation]);
        build = FormatData.buildClass(data,[estation],contaminant,24);
        xy_values = an.prepro(data,build, contaminant);
        initCpu = time();
        nn.train(xy_values[0],xy_values[1],xy_values[2],1000);
        finCpu = time();
        initGpu = time();
        nng.train(xy_values[0],xy_values[1],xy_values[2],1000);
        finGpu = time();
        totalCpu = finCpu - initCpu;
        totalGpu = finGpu - initGpu;
        time_cpu.append(totalCpu);
        time_gpu.append(totalGpu);
        date= date + timedelta(hours = dy);
    plt.plot(totalCpu,'k-', label='time CPU');
    plt.plot(totalGpu, 'r--',label='time GPU');
    plt.title('GPU vs CPU');
    plt.xlabel('Years with which the neural network was trained');
    plt.ylabel('Time');
    plt.legend(loc ='best');
    plt.savefig('/time.png')
    plt.show();


def main():
    print("1.Training time test using GPU vs CPU\n");
    print("2.Testing using GPU's \n");
    print("3.Testing using CPU \n");
    opt = int(input("Option to execute: "))
    if opt == 1:
        time();
    elif opt == 2:
        print("1.Estations number \n 2.iterations number \n 3.All the tests \n"));
        option = int(input("Option to execute: "))
        if option == 1:
            estationsGpu();
        elif option == 2:
            iterationGpu();
        elif option == 3:
            estationsGpu();
            iterationGpu();
        else:
            print("Incorrect option");
    elif opt == 3:
        print("1.Estations number \n 2.iterations number \n 3.All the tests \n"));
        option = int(input("Option to execute: "))
        if option == 1:
            estations();
        elif option == 2:
            iteration();
        elif option == 3:
            estations();
            iteration();
        else:
            print("Incorrect option");
    else:
        print("Incorrect option");


if __name__ == '__main__':
    main()
