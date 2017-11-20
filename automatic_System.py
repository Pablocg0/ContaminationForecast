from datetime import datetime, timedelta
from Utilites.FormatData import FormatData as fd
import time
import sys, os
import pandas as df
import numpy as np
import prediction as pre
from NetCDF.makeCsv import makeCsv as mk

dirNetCDF = '/DATA/WRF_Operativo/2017/'; #direccion de los archivos NetCDF
#dirCsv = '/data/totalData/totalCuadrantes/';
dirCsv = '/home/pablo/DATA/DataCuadrantes/'; #direccion de los archivos creados apartir de los NetCDF
dirData= 'data/DatosLCB/'; #Direccion de datos de entrenamiento
dirTrain = 'trainData/TrainLCB/'; #Direccion de entrenamiento de la red neuronal
estaciones =['AJM','MGH','CCA','SFE','UAX','CUA','NEZ','CAM','LPR','SJA','CHO','IZT','SAG','TAH','ATI','FAC','UIZ','MER','PED','TLA','BJU','XAL'];
variables=['U10','V10','RAINC','T2', 'TH2', 'RAINNC', 'PBLH', 'SWDOWN', 'GLW'];


def configuracion():
    nameNetcdf = "wrfout_d02_"
    actual = datetime.now();
    actualNetcdf = nameNetcdf+ str(actual.year)+ "-"+ str(actual.month)+ "-"+str(actual.day)+"_00.nc";
    actualCsv = variables[0]+"_"+str(actual.year)+ "-"+ str(actual.month)+ "-"+str(actual.day)+".csv";
    ayer = actual - timedelta(days=1);
    ayerCsv = variables[0]+"_"+str(ayer.year)+ "-"+ str(ayer.month)+ "-"+str(ayer.day)+".csv";
    return [actual,ayer,actualNetcdf,actualCsv,ayerCsv];

def buscarArchivo(archivo):
    for root, dir, ficheros in os.walk(dirNetCDF,topdown=True):
        for i in ficheros:
            print(i)
            if archivo in i:
                return True;
    return False;


def leerArchivo(informacion):
    if buscarArchivo(informacion[3]):
        print(informacion[3]);
        fecha= str(informacion[0].year)+"-"+str(informacion[0].month)+"-"+str(informacion[0].day)
        dataMet = unionMeteorologia(fecha);
        for value in estaciones:
            data = baseContaminantes(informacion[0],value);
            data = data.merge(dataMet,how='left',on='fecha');
            valPred = prediccion(value, data);
            guardarPrediccion(value,informacion[0],valPred)
    elif buscarArchivo(informacion[2]) : #NetCDF
        print(informacion[2]);
        print("netcdf hoy")
        data = mk.open_netcdf(dirNetCDF+informacion[2],informacion[2],mk.clearString(informacion[2]));
        mk.checkFile(data,informacion[2],fecha,2);
        fecha= str(informacion[0].year)+"-"+str(informacion[0].month)+"-"+str(informacion[0].day)
        dataMet = unionMeteorologia(fecha);
        for value in estaciones:
            data = baseContaminantes(informacion[0],value);
            data = data.merge(dataMet,how='left',on='fecha');
            valPred = prediccion(value, data);
            guardarPrediccion(value,informacion[0],valPred)
    else :
        buscarArchivo(informacion[4]); #csv ayer
        print(informacion[4]);
        print("ayer");
        fecha= str(informacion[1].year)+"-"+str(informacion[1].month)+"-"+str(informacion[1].day)
        dataMet = unionMeteorologia(fecha);
        for value in estaciones:
            data = baseContaminantes(informacion[0],value);
            data = data.merge(dataMet,how='left',on='fecha');
            valPred = prediccion(value, data);
            guardarPrediccion(value,informacion[0],valPred)



def prediccion(estacion,data):
    temp = data.ix[0].values;
    temp = temp[1:];
    dataPred = pre.normalize(temp,estacion,"O3",dirData);
    prediccion = pre.prediction(estacion,"O3",dataPred,dirTrain,dirData)
    prediccion = pre.desNorm(prediccion,estacion,"O3",dirData);
    return prediccion;



def baseContaminantes(fecha,estacion):
    fechaActual = str(fecha.year)+'-'+str(fecha.month)+'-'+str(fecha.day)+' '+str(fecha.hour)+':00:00';
    data = fd.readData(fechaActual,fechaActual[estacion],"O3");
    return data;


def unionMeteorologia(fecha):
    data = df.DataFrame();
    for i in variables:
        name = i+"_"+fecha+".csv";
        dataTemp = df.read_csv(dirCsv+name);
        data = data.merge(dataTemp,how='left',on='fecha');
    return data;

def guardarPrediccion(estacion,fecha,Valor):
    fechaActual = str(fecha.year)+'-'+str(fecha.month)+'-'+str(fecha.day)+' '+str(fecha.hour)+':00:00';
    fd.saveData(estacion,fechaActual,Valor)


information=configuracion();
print(information);
leerArchivo(information);
