from datetime import datetime, timedelta
import time
import sys, os
import pandas as df
import numpy as np
import NetCDF.makeCsv as mk

dirNetCDF = '/DATA/WRF_Operativo/2017/'; #direccion de los archivos NetCDF

def configuracion():
    nameNetcdf = "wrfout_d02_"
    actual = datetime.now();
    actualNetcdf = nameNetcdf+ str(actual.year)+ "-"+ str(actual.month)+ "-"+str(actual.day)+"_00.nc";
    ayer = actual - timedelta(days=1);
    ayerNetcdf = nameNetcdf+ str(ayer.year)+ "-"+ str(ayer.month)+ "-"+str(ayer.day)+"_00.nc";
    return [actual,ayer,actualNetcdf,ayerNetcdf];

def buscarArchivo(archivo):
    for root, dir, ficheros in os.walk(dirNetCDF):
        for i in ficheros:
            if archivo in i.lower():
                return True;
            else:
                return False;


def leerArchivo(informacion):
    if buscarArchivo(informacion[2]):
        mk.open_netcdf(dirNetCDF+informacion[2],informacion[2],mk.clearString(informacion[2]));
    elif buscarArchivo(informacion[3]):
        #implementar
        print(informacion[3]);
    else:
        




configuracion();
#leerArchivo(information);
