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
import sys


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


def divData(data):
    total  = np.zeros((0,4),dtype=np.float32);
    for i in range(48):
        dataValue = data[i];
        array1D = [];
        size = dataValue.shape;
        numRows = int(size[0]/2);
        numColumns = int(size[1]/2);
        dataSecc1 = dataValue[0:numRows,0:numColumns]
        dataSecc2 = dataValue[numRows:,0:numColumns]
        dataSecc3 = dataValue[0:numRows,numColumns:]
        dataSecc4 = dataValue[numRows:,numColumns:]
        prom1 = dataSecc1.sum()/(numColumns*numRows);
        prom2 = dataSecc2.sum()/(numColumns*numRows);
        prom3 = dataSecc3.sum()/(numColumns*numRows);
        prom4 = dataSecc4.sum()/(numColumns*numRows) ;
        array1D.append(prom1)
        array1D.append(prom2)
        array1D.append(prom3)
        array1D.append(prom4)
        #div= np.vsplit(dataValue,2);
        #divSplit = np.array_split(div[0],8);
        #divSplit1 = np.array_split(div[1],8);
        #for val in divSplit:
        #    meanVal = np.mean(val);
        #    array1D.append(meanVal);
        #for val in divSplit1:
        #    meanVal = np.mean(val);
        #    array1D.append(meanVal)
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
    for x in range(47):
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
    variables=['U10','V10','RAINC','T2', 'TH2', 'RAINNC', 'PBLH', 'SWDOWN', 'GLW'];

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
    #temp = conver1D(var);
    temp = divData(var);
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
        allData.to_csv('/home/pablo/DATA/DataC16/'+name,encoding='utf-8',index= False);
    elif opt == 1:
        filq = '/home/pablo/DATA/DataMean/'+name
        dateVal.to_csv(filq,encoding = 'utf-8',index=False);
    elif opt == 2:
        filq = '/home/pablo/DATA/DataCuadrantes/'+name
        allData.to_csv(filq,encoding = 'utf-8',index=False);



def readCsv(variables):
    """
    :param variables : netCDF4 file name
    :type variables: string
    """
   # os.makedirs('../data/totalData/');
    dataVa = df.DataFrame();
    variables = variables;
    mypath = '/home/pablo/DATA/DataCuadrantes/';
    patron = re.compile(variables+'_\d\d\d\d-\d\d-\d\d'+'.*');
    for base, dirs, filess in os.walk(mypath,topdown=False):
        for value in filess:
            if patron.match(value) != None:
                tempData = df.read_csv(mypath+value);
                tempData = completeMet(tempData);
                dataVa = concat([tempData,dataVa],axis=0);
    dataVa = dataVa.reset_index();
    dataVa= dataVa.drop(labels='index',axis=1);
    dataVa.to_csv('../data/totalData/totalCuadrantes/'+variables+'_total.csv',encoding='utf-8',index=False);
    dataVa = df.DataFrame();


def completeMet(data):
    """
    :param data: meteorology data
    :type data: DataFrame
    """
    fechaOri = []
    newData= df.DataFrame([],columns= data.columns)
    nameColumns = data.columns.values
    nameColumns = nameColumns[1:]
    fecha  = data['fecha'].values
    for i in range(24):
        f = fecha[i]
        fechaOri.append(f);
        dateInit = datetime.strptime(f,'%Y-%m-%d %H:%M:%S');
        da = dateInit + timedelta(hours = 24)
        ti = da.strftime('%Y-%m-%d %H:%M:%S');
        temp = data[data.fecha == ti]
        dtemp = data.loc[temp.index,nameColumns]
        newData= df.concat([newData,dtemp])
    newData= newData.drop(labels='fecha',axis=1)
    newData = newData.reset_index(drop=True);
    fechas = df.DataFrame(fechaOri,columns=['fecha']);
    newData['fecha']= fechas;
    return newData;

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
        data = Dataset('../data/NetCDF/'+cadena);
        os.remove('../data/NetCDF/'+cadena);
    elif patron2.match(nameFile) != None:
        shutil.copy(ls,fname);
        infile = gzip.open(fname, 'rb')
        tmp = tempfile.NamedTemporaryFile(delete=False)
        shutil.copyfileobj(infile, tmp)
        infile.close()
        tmp.close()
        data = Dataset(tmp.name)
        os.unlink(tmp.name)
        os.remove(fname);
    else:
        data = Dataset(ls)
    #os.remove(fname);
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
    tfileCopy = list(tempfile.values.flatten());
    tbaseCopy = list(tempbase.values.flatten());
    l = len(tfile)
    for i in range(l):
        tfil = tfile[i];
        tbas= tbase[i];
        ls = tbas + '/' + tfil
        f = patron2.findall(tfil);
        cadena = clearString(tfil);
        print(cadena);
        try:
            net = open_netcdf(ls,tfil,cadena);
            checkFile(net,tfil,f[0],opt);
            tfileCopy.remove(tfil);
            tbaseCopy.remove(tbas);
        except (OSError,EOFError) as e:
            print(e);
            fdata = df.DataFrame(tfileCopy,columns=['nameFile']);
            fbas = df.DataFrame(tbaseCopy,columns=['nameBase']);
            fdata.to_csv(dirr+'tfile.txt',encoding='utf-8',index=False);
            fbas.to_csv(dirr+'tbase.txt',encoding='utf-8',index=False);
            os.remove('../data/NetCDF/'+cadena);
            sys.exit()
            #readFiles(1);
        except tarfile.ReadError:
            print('error2');
            #fdata = df.DataFrame(tfile,columns=['nameFile']);
            #fbas = df.DataFrame(tbase,columns=['nameBase']);
            #fdata.to_csv(dirr+'tfile.txt',encoding='utf-8',index=False);
            #fbas.to_csv(dirr+'tbase.txt',encoding='utf-8',index=False);
            #readFiles(1);
        except (KeyError, FileNotFoundError, EOFError):
            print('ERROR DE LECTURA');


def totalFiles():
    dirr = '../data/NetCDF/';
    dirr2 = '/DATA/WRF_Operativo/2017/';
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
    dirr = '/DATA/WRF_Operativo/2017/';
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
readFiles(2);
#readFiles2(1);
#variables=['Uat10','Vat10','PREC2'];
#variables=['U10','V10','RAINC'];
variables=['U10','V10','RAINC','T2', 'TH2', 'RAINNC', 'PBLH', 'SWDOWN', 'GLW'];
for i in variables:
    print(i)
    readCsv(i);
#readCsv(variables[0]);
#makeDates('2017-06-13');
