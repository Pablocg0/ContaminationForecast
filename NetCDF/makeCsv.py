
from datetime import datetime, timedelta
import pandas as df
from netCDF4 import Dataset
import netCDF4 as nc4
import NewBBOX as ne
from os import listdir
import numpy as np
from pandas import concat
import re
import os


def conver1D(array):
    """
    Function to convert an array to a list
    :param array: array with the data
    :type array = matrix float32
    :return : list with the data
    :return type: list float32
    """
    array1D = [];
    #total = [];
    l = array.shape
    total  = numpy.matrix([])
    i = 0
    for i in range(24):
        print(i);
        tempData = array[i]
        print(tempData);
        for x in tempData:
            for s in x:
                array1D.append(s);
        print(array1D);
    #total.append(array1D)
    total = numpy.insert(total,i,array1D);
    return total;

def makeDates(date):
    """
    Function to create a list with the format year-month-day hours:minutes:seconds
    from 00 hours to 23 hours
    :param date : initial date
    :param type : string
    :return : list with the dates
    :return type : list datatime
    """
    listDates = [];
    date = date + ' 00:00:00';
    d =datetime.strptime(date,'%Y-%m-%d %H:%M:%S');
    listDates.append(d);
    for x in range(23):
        d = d + timedelta(hours=1);
        listDates.append(d);
    allData = df.DataFrame(listDates,columns=['fecha']);
    return allData;


def nameColumns(name,numbColumns):
    """
    Function to create list with the name of the columns
    from the variables
    :param name : Variable name
    :param type : string
    :param numbColumns : Number of columns
    :param type: int
    :return : list with the name of the columns
    :return type: list string
    """
    namesColumns=[];
    for i in range(numbColumns):
        nColumn = name+'_'+str(i);
        namesColumns.append(nColumn);
    return namesColumns;


def makeCsv(net,date):
    """
    Function to create .csv files of some variables that are in a NetCDF file,
    the .cvs file is saved in the data/NetCDF path of the project
    :param net : NetCDF file information
    :param type: NetCDF type
    :param date: initial date
    :param type: string
    """
    allData = makeDates(date);
    variables=['Uat10','Vat10','PREC2'];

    LON = net.variables['Longitude'][:];
    LAT = net.variables['Latitude'][:];

    LONsize = len(LON);
    LATsize = len(LAT);

    minlat= 19.4284700 #19.8 ;
    maxlat=20 #-19.033333;
    minlon=-99.127660 #-99.933333;
    maxlon=-98 #99.366667;

    celda = [];
    var_cut=[];
    for i in variables:
        var= net.variables[i][:]
        celda.append(var);
        result = ne.NewBBOX(var,LON,LAT,LONsize,LATsize,minlat,maxlat,minlon,maxlon);
        var_cut.append(result[0]);


    for ls in range(len(var_cut)):
        temp = conver1D(var_cut[ls]);
        dataMatrix= np.array(temp);
        name = variables[ls]+'_'+date+'.csv'
        myIndex = nameColumns(variables[ls],len(temp[0]));
        tempFrame =df.DataFrame(dataMatrix,columns=myIndex);
        allData = concat([allData,tempFrame], axis=1);
        allData = allData.fillna(value=0);
        meanAllData= allData.mean(axis= 0);
        print(meanAllData);
        allData.to_csv('../data/NetCDF/'+name,encoding='utf-8',index= False);


def readCsv(variables):
    os.makedirs('../data/totalData/');
    data = df.DataFrame();
    variables = variables;
    mypath = '../data/NetCDF/';
    patron = re.compile(variables+'.*');
    for x in listdir(mypath):
        if patron.match(x) != None:
            print(x);
            tempData = df.read_csv(mypath+x);
            data = concat([tempData,data],axis=0);
    data = data.reset_index();
    data= data.drop(labels='index',axis=1);
    data.to_csv('../data/totalData/'+variables+'_total.csv',encoding='utf-8',index=False);


def readFiles():
    """
    Function to read all NetCDF files that are in the specified path
    and named by the format Dom1_year-month-day.nc
    """
    #dirr = '/home/pablo/DATA/' #specified path
    os.makedirs('../data/NetCDF/');
    dirr = '/DATA/OUT/WRF/';
    date = '\d\d\d\d-\d\d-\d\d'
    name = 'Dom2_'
    patron = re.compile(name+'.*')
    patron2 = re.compile(date);
    for x in listdir(dirr):
        if patron.match(x) != None:
            ls= dirr +x;
            print(ls);
            f = patron2.findall(x);
            net = Dataset(ls);
            #makeCsv(net,f[0]);
            checkFile(net,x,f[0]);

def checkFile(net,name,date):
    try:
        net.variables['Longitude'][:];
        net.variables['Latitude'][:];
        makeCsv(net,date);
    except KeyError:
        print('error in file: ' + name);


readFiles();
variables=['Uat10','Vat10','PREC2'];
for i in variables:
    readCsv(x);
#readCsv(variables[0]);
#makeDates('2017-06-13');
