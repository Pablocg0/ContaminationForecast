from datetime import datetime, timedelta
import pandas as df
from netCDF4 import Dataset
import netCDF4 as nc4
import NewBBOX as ne
from os import listdir
import numpy as np
import re


def conver1D(array):
    array1D = [];
    total = [];
    i = 0
    for i in range(24):
        tempData = array[i]
        for x in tempData:
            for s in x:
                array1D.append(s);
        total.append(array1D)
    return total;

def makeDates(date):
    listDates = [];
    date = date + ' 00:00:00';
    d =datetime.strptime(date,'%Y-%m-%d %H:%M:%S');
    listDates.append(d);
    for x in range(23):
        d = d + timedelta(hours=1);
        listDates.append(d);
    allData = df.DataFrame(listDates,columns=['fecha']);
    return allData;
print(allData);

def nameColumns(name,numbColumns):
    namesColumns=[];
    for i in range(numbColumns):
        nColumn = name+'_'+str(i);
        namesColumns.append(nColumn);
    return namesColumns;


def makeCsv(net,date):
    allData = makeDates(date);
    variables=['Uat10','Vat10','PREC2'];

    LON = net.variables['Longitude'][:];
    LAT = net.variables['Latitude'][:];
    TIME = net.variables['Time'][:];

    LONsize = len(LON);
    LATsize = len(LAT);
    TIMEsize = len(TIME);

    minlat=19.4284700;
    maxlat=20;
    minlon=-99.1276600;
    maxlon=-98;

    celda = [];
    var_cut=[];
    for i in variables:
        var= net.variables[i][:]
        celda.append(var);
        result = ne.NewBBOX(var,LON,LAT,LONsize,LATsize,minlat,maxlat,minlon,maxlon);
        var_cut.append(result[0]);

    #for x in var_cut:
    #    temp= conver1D(x);
    #    dataMatrix = np.array(temp)
    #    print(dataMatrix.shape);
    #    print(len(temp[0]));

    for ls in range(len(var_cut)):
        temp = conver1D(var_cut[ls]);
        dataMatrix= np.array(temp);
        name = variables[ls]+'_'+date+'.csv'
        myIndex = nameColumns(variables[ls],len(temp[0]));
        tempFrame =df.DataFrame(dataMatrix,columns=myIndex);
        allData = concat([allData,tempFrame], axis=1);
        allData.to_csv('data/NetCDF/'+name,encoding='utf-8',index= False);
        #print(allData);


def readFiles():
    dirr = '/home/pablo/DATA/'
    date = '\d\d\d\d-\d\d-\d\d'
    name = 'Dom1_'
    patron = re.compile(name+'.*')
    patron2 = re.compile(date);
    for x in listdir(dirr):
        if patron.match(x) != None:
            ls= dirr +x;
            print(ls);
            f = patron2.findall(x);
            print(f[0]);
            net = Dataset(ls);
            makeCsv(net,f[0]);

readFiles();
#makeDates('2017-06-13');
