from tests.neuralNetworkGpu import train as nng
from tests.neuralNetwork import train as nn
from Utilites.FormatData import FormatData
from Utilites.Utilites import prepro as an
from datetime import datetime, timedelta
import pandas as df
import matplotlib
#matplotlib.use('agg')
import matplotlib.pyplot as plt
from time import time

contaminant = 'O3';
loss_vec= [];
est =['AJM','MGH','CCA','SFE','UAX','CUA','NEZ','CAM','LPR','SJA','CHO','IZT','SAG','TAH','ATI','FAC','UIZ','MER','PED','TLA','BJU','XAL'];
startDate =['2015/01/01','2015/01/01','2014/08/01','2012/02/20','2012/02/20','2011/10/01','2011/07/27','2011/07/01','2011/07/01','2011/07/01','2007/07/20','2007/07/20','1995/01/01','1995/01/01','1994/01/02','1993/01/01','1987/05/31','1986/01/16','1986/01/16','1986/01/15','1986/01/12','1986/01/10'];
endDate = '2017/02/01';

def estations():
    start =startDate[0];
    estation = [];
    for x in est:
        estation += [x];
        print(estation);
        data = FormatData.readData(start,endDate,estation,contaminant);
        build = FormatData.buildClass2(data,[est[0]],contaminant,24,start,endDate);
        xy_values = an(data,build, contaminant);
        temp_loss = nn(xy_values[0],xy_values[1],xy_values[2],1000,est[0],contaminant);
        loss_vec.append(temp_loss);
    print(loss_vec);
    plt.figure(figsize=(12.2,6.4))
    plt.plot(loss_vec, 'k-', label='Loss')
    plt.title('Error aumentando el numero de estaciones')
    plt.xlabel('Numero de estaciones')
    plt.ylabel('Loss')
    plt.legend(loc='best')
    location = np.range(len(est));
    plt.xticks(location,est,rotation='vertical');
    plt.savefig("estaciones.png", dpi=600);
    plt.show();

def estationsGpu():
    start =startDate[0];
    estation = [];
    for x in est:
        estation += [x];
        print(estation);
        data = FormatData.readData(start,endDate,estation,contaminant);
        build = FormatData.buildClass2(data,[est[0]],contaminant,24,start,endDate);
        xy_values = an(data,build, contaminant);
        temp_loss = nng(xy_values[0],xy_values[1],xy_values[2],1000);
        loss_vec.append(temp_loss);
    print(loss_vec);
    plt.plot(loss_vec, 'k-', label='Loss')
    plt.title('Error aumentando el numero de estaciones')
    plt.xlabel('Numero de estaciones')
    plt.ylabel('Loss')
    plt.legend(loc='best')
    plt.savefig("estacionesGpu.png", dpi=600);
    plt.show();

def iteration():
    i = 200
    start =startDate[0];
    estation= est[10];
    print(estation)
    print(start)
    data = FormatData.readData(start,endDate,[estation],contaminant);
    build = FormatData.buildClass2(data,[est[10]],contaminant,24,start,endDate);
    xy_values = an(data,build, contaminant);
    while i <= 3000:
        temp_loss = nn(xy_values[0],xy_values[1],xy_values[2],i);
        loss_vec.append(temp_loss);
        i = i + 200;
        print(i);
    print(loss_vec);
    plt.plot(loss_vec, 'k-', label='Loss')
    plt.title('Error aumentando el numero de iteraciones de entrenamiento')
    plt.xlabel('Numero de iteraciones')
    plt.ylabel('Loss')
    plt.legend(loc='best')
    plt.savefig("iteraciones.png",dpi=600);
    plt.show();

def iterationGpu():
    i = 200
    start =startDate[0];
    estation= est[10];
    data = FormatData.readData(start,endDate,[estation],contaminant);
    build = FormatData.buildClass2(data,[est[10]],contaminant,24,start,endDate);
    xy_values = an(data,build, contaminant);
    while i <= 3000:
        temp_loss = nng(xy_values[0],xy_values[1],xy_values[2],i);
        loss_vec.append(temp_loss);
        i = i + 200;
        print(i);
    print(loss_vec);
    plt.plot(loss_vec, 'k-', label='Loss')
    plt.title('Error aumentando el numero de iteraciones de entrenamiento')
    plt.xlabel('Numero de iteraciones')
    plt.ylabel('Loss')
    plt.legend(loc='best')
    plt.savefig("iteraciones.png",dpi=600);
    plt.show();


def tiempo():
    time_cpu =[];
    time_gpu =[];
    time_base= [];
    start  = datetime.strptime(startDate[20],'%Y/%m/%d')
    end = datetime.strptime(endDate,'%Y/%m/%d')
    dy= 8760 * 2;
    estation = est[20];
    date = start + timedelta(hours = dy);
    while date <= end:
        sDate = date.strftime('%Y/%m/%d');
        initData=time();
        data = FormatData.readData(start,date,[estation],contaminant);
        build = FormatData.buildClass2(data,[estation],contaminant,24,startDate[20],sDate);
        xy_values = an(data,build, contaminant);
        finData= time();
        initCpu = time();
        temp_loss= nn(xy_values[0],xy_values[1],xy_values[2],1000,estation,contaminant);
        loss_vec.append(temp_loss);
        finCpu = time();
        initGpu = time();
        temp_loss=nng(xy_values[0],xy_values[1],xy_values[2],1000);
        loss_vec.append(temp_loss);
        finGpu = time();
        totalCpu = finCpu - initCpu;
        totalGpu = finGpu - initGpu;
        totalBase = finData - initData;
        time_base.append(totalBase);
        time_cpu.append(totalCpu);
        time_gpu.append(totalGpu);
        date= date + timedelta(hours = dy);
    plt.plot(time_base,'g-',label='time Data base');
    plt.plot(time_cpu,'k-', label='time CPU');
    plt.plot(time_gpu, 'r-',label='time GPU');
    plt.title('GPU vs CPU');
    plt.xlabel('Years');
    plt.ylabel('Time');
    plt.legend(loc ='best');
    plt.savefig('tiempo.png',dpi=600);
    plt.show();

def testData():
    i= 0;
    dataBase_time= [];
    file_time=[];
    while i <= 21:
        station = est[i];
        print(station);
        init_dataBase = time();
        data = FormatData.readData(startDate[i],endDate,[est[i]],contaminant);
        build = FormatData.buildClass2(data,[est[i]],contaminant,24,startDate[i],endDate);
        xy_values = an(data,build, contaminant);
        fin_dataBase= time();
        init_fileTime = time();
        name = station +'_'+contaminant;
        data = df.read_csv('data/'+name+'.csv');
        build = df.read_csv('data/'+name+'_pred.csv');
        xy_values = an(data,build, contaminant);
        fin_fileTime = time();
        total_dataBase = fin_dataBase -init_dataBase;
        total_file= fin_fileTime - init_fileTime;
        dataBase_time.append(total_dataBase);
        file_time.append(total_file);
        i+=1;
    plt.plot(file_time,'k-', label='time File');
    plt.plot(dataBase_time, 'r-',label='time DataBase');
    plt.title('DataBase vs File');
    plt.xlabel('stations');
    plt.ylabel('Time (second)');
    plt.legend(loc ='best');
    plt.savefig('tiempoDataBase.png',dpi=600);
    plt.show();

def testData2():
    i= 0;
    dataBase_time= [];
    file_time=[];
    s = []
    while i <= 21 :
        s.append(est[i]);
        print(s)
        init_dataBase = time();
        data = FormatData.readData(startDate[i],endDate,s,contaminant);
        build = FormatData.buildClass2(data,s,contaminant,24,startDate[i],endDate);
        #xy_values = an(data,build, contaminant);
        fin_dataBase= time();
        init_fileTime = time();
        for x in s:
            station = x
            name = station +'_'+contaminant;
            data = df.read_csv('data/'+name+'.csv');
            build = df.read_csv('data/'+name+'_pred.csv');
            #xy_values = an(data,build, contaminant);
        fin_fileTime = time();
        total_dataBase = fin_dataBase -init_dataBase;
        total_file= fin_fileTime - init_fileTime;
        dataBase_time.append(total_dataBase);
        file_time.append(total_file);
        i +=1;
    plt.plot(file_time,'g-', label='time File');
    plt.plot(dataBase_time, 'r-',label='time DataBase');
    plt.title('DataBase vs File');
    plt.xlabel('stations');
    plt.ylabel('Time (second)');
    plt.legend(loc ='best');
    plt.savefig('Graficas/tiempoDataBase2.png',dpi=600);
    plt.show();



def main():
    print("1.Training time test using GPU vs CPU\n");
    print("2.Testing using GPU's \n");
    print("3.Testing using CPU \n");
    print('4, Testing DataBase vs File')
    opt = int(input("Option to execute: "))
    if opt == 1:
        tiempo();
    elif opt == 2:
        print("1.Estations number \n 2.iterations number \n 3.All the tests \n");
        option = int(input("Option to execute: "));
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
        print("1.Estations number \n 2.iterations number \n 3.All the tests \n");
        option = int(input("Option to execute: "));
        if option == 1:
            estations();
        elif option == 2:
            iteration();
        elif option == 3:
            estations();
            iteration();
        else:
            print("Incorrect option");
    elif opt == 4:
        testData2();
    else:
        print("Incorrect option");


if __name__ == '__main__':
    main()
