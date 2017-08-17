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
import tarfile
import gzip
import shutil
import tempfile


def conver1D(array):
    """
    Function to convert an array to a list
    :param array: array with the data
    :type array = matrix float32
    :return : list with the data
    :return type: list float32
    """
    l = array.shape
    total  = np.zeros((0,l[1]*l[2]),dtype=np.float32);
    i = 0
    for i in range(24):
        tempData = array[i]
        array1D=[];
        for x in tempData:
            for s in x:
                array1D.append(s);
        total = np.insert(total,i,array1D,axis=0);
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


def makeCsv(net,date,opt):
    """
    Function to create .csv files of some variables that are in a NetCDF file,
    the .cvs file is saved in the data/NetCDF path of the project
    :param net : NetCDF file information
    :param type: NetCDF type
    :param date: initial date
    :param type: string
    """
    variables=['U10','V10','RAINC'];

    LON = net.variables['XLONG'][:];
    LAT = net.variables['XLAT'][:];

    LON = LON[1][1];
    LAT = LAT[1];


    LONsize = len(LON);
    LATsize = len(LAT);

    minlat= 19.4284700 #19.8 ;
    maxlat=20 #-19.033333;
    minlon= -99.127660 #-99.933333;
    maxlon=-98 #99.366667;

    celda = [];
    var_cut=[];
    for i in variables:
        var= net.variables[i][:]
        celda.append(var);
        result = ne.NewBBOX(var,LON,LAT,LONsize,LATsize,minlat,maxlat,minlon,maxlon);
        var_cut.append(result[0]);


    for ls in range(len(var_cut)):
        saveData(var_cut[ls],variables[ls],date,opt);


def saveData(var,variables,date,opt):
    """
    Function for the data create
    """
    dateVal = makeDates(date);
    allData = makeDates(date);
    temp = conver1D(var);
    dataMatrix= temp;
    name = variables+'_'+date+'.csv'
    myIndex = nameColumns(variables,len(temp[0]));
    tempFrame =df.DataFrame(dataMatrix,columns=myIndex);
    allData = concat([allData,tempFrame], axis=1);
    allData = allData.fillna(value=0);
    meanAllData= allData.mean(axis= 1);
    meanValues = meanAllData.as_matrix();
    mean = df.DataFrame(meanValues,columns=[variables+'_mean']);
    dateVal[variables+'_mean']= mean;
    if opt == 0:
        allData.to_csv('../data/NetCDF/'+name,encoding='utf-8',index= False);
    elif opt == 1:
        filq = '/home/pablo/DATA/'+name
        dateVal.to_csv(filq,encoding = 'utf-8',index=False);




def readCsv(variables):
    """
    :param variables : netCDF4 file name
    :type variables: string
    """
   # os.makedirs('../data/totalData/');
    dataVa = df.DataFrame();
    variables = variables;
    mypath = '/home/pablo/DATA/';
    patron = re.compile(variables+'.*');
    for base, dirs, files in os.walk(mypath,topdown=True):
        for value in files:
            if patron.match(value) != None:
                tempData = df.read_csv(mypath+value);
                dataVa = concat([tempData,dataVa],axis=0);
    dataVa = dataVa.reset_index();
    dataVa= dataVa.drop(labels='index',axis=1);
    dataVa.to_csv('../data/totalData/'+variables+'_total.csv',encoding='utf-8',index=False);
    dataVa = df.DataFrame();


def open_netcdf(ls,nameFile,cadena):
    name ='.nc.tar.gz';
    name1 = '.nc.gz'
    patron = re.compile('.*'+name)
    patron2 = re.compile('.*'+name1);
    fname= '../data/NetCDF/'+nameFile
    if patron.match(nameFile) != None:
        comp = tarfile.open(ls,'r');
        comp.extract(cadena,'../data/NetCDF/');
        comp.close();
        net = Dataset('../data/NetCDF/'+cadena);
        os.remove('../data/NetCDF/'+cadena);
    elif patron2.match(nameFile) != None:
        shutil.copy(ls,fname);
        infile = gzip.open(fname, 'rb')
        tmp = tempfile.NamedTemporaryFile(delete=False)
        shutil.copyfileobj(infile, tmp)
        infile.close()
        tmp.close()
        data = Dataset(tmp.name)
        os.remove(tmp.name)
        os.remove(fname);
    else:
        data = Dataset(fname)
    return data


def readFiles(opt):
    """
    Function to read all NetCDF files that are in the specified path
    and named by the format Dom1_year-month-day.nc
    """
    date = '\d\d\d\d-\d\d-\d\d'
    name = 'wrfout_d02_'
    dirr = '../data/NetCDF/';
    patron = re.compile(name+'.*')
    patron2 = re.compile(date);
    tempfile = df.read_csv(dirr+'tfile.txt');
    tempbase= df.read_csv(dirr+'tbase.txt');
    tfile = list(tempfile.values.flatten());
    tbase = list(tempbase.values.flatten());
    l = len(tfile)
    for i in range(l):
        ls = tbase[i] + '/' + tfile[i]
        f = patron2.findall(tfile[i]);
        cadena = clearString(tfile[i]);
        print(cadena);
        try:
            net = open_netcdf(ls,tfile[i],cadena);
            checkFile(net,tfile[i],f[0],opt);
        except (OSError,EOFError) as e:
            print(e);
            #fdata = df.DataFrame(tfile,columns=['nameFile']);
            #fbas = df.DataFrame(tbase,columns=['nameBase']);
            #fdata.to_csv(dirr+'tfile.txt',encoding='utf-8',index=False);
            #fbas.to_csv(dirr+'tbase.txt',encoding='utf-8',index=False);
            #readFiles(1);
        except tarfile.ReadError:
            print('error2');
            #fdata = df.DataFrame(tfile,columns=['nameFile']);
            #fbas = df.DataFrame(tbase,columns=['nameBase']);
            #fdata.to_csv(dirr+'tfile.txt',encoding='utf-8',index=False);
            #fbas.to_csv(dirr+'tbase.txt',encoding='utf-8',index=False);
            #readFiles(1);


def totalFiles():
    dirr = '../data/NetCDF/';
    dirr2 = '/DATA/WRF/';
    name = 'wrfout_d02_\d\d\d\d-\d\d-\d\d_00.nc'
    fil=[];
    ba = [];
    patron = re.compile(name+'.*')
    for base, dirs, files in os.walk(dirr2,topdown=True):
        for value in files:
            if patron.match(value) != None:
                fil.append(value);
                ba.append(base);
    fdata = df.DataFrame(fil,columns=['nameFile']);
    fbase = df.DataFrame(ba,columns=['nameBase']);
    fdata.to_csv(dirr+'tfile.txt',encoding='utf-8',index=False);
    fbase.to_csv(dirr+'tbase.txt',encoding='utf-8',index=False);




def readFiles2(opt):
    dirr = '/DATA/WRF/';
    name='wrfout_d02_';
    date = '\d\d\d\d-\d\d-\d\d';
    patron = re.compile(name+'.*')
    patron2 = re.compile(date);
    for base, dirs, files in os.walk(dirr,topdown=True):
        #print(base);
        #print(dirs);
        for var in files:
            if patron.match(var) != None:
                ls = base + '/' + var
                f = patron2.findall(var);
                comp = tarfile.open(ls,'r');
                cadena = clearString(var);
                print(cadena);
                comp.extract(cadena,'../data/NetCDF/');
                comp.close();
                net = Dataset('../data/NetCDF/'+cadena);
                checkFile(net,var,f[0],opt);
                os.remove('../data/NetCDF/'+cadena);

def clearString(name):
    if name.find(".tar") != 0:
        name = name.replace(".tar","");

    if name.find(".gz") !=0:
        name=name.replace(".gz", "");


    return name;



def checkFile(net,name,date,opt):
    """
    Function to check if the file has
    the requiered parameters.
    :param net : information that contains the file
    :type net: Dataset
    :param name: file name
    :type name : string
    :param date: date
    :type date: string
    :param opt: option
    :type opt: int
    """
    try:
        net.variables['XLONG'][:];
        net.variables['XLAT'][:];
        makeCsv(net,date,opt);
    except KeyError:
        print('error in file: ' + name);


if not os.path.exists('data/NetCDF'): os.makedirs('data/NetCDF');
if not os.path.exists('data/totalData'): os.makedirs('data/totalData');
totalFiles();
#readFiles(1);
#readFiles2(1);
#variables=['Uat10','Vat10','PREC2'];
#variables=['U10','V10','RAINC'];
#for i in variables:
#    print(i)
#    readCsv(i);
#readCsv(variables[0]);
#makeDates('2017-06-13');
