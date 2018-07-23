'''
File name : automatic_MakeCsv.py
Author: Pablo Camacho Gonzalez
Python version: 3.6.4
Date last modified: 27/02/2018
'''


from datetime import datetime, timedelta
import pandas as df
from netCDF4 import Dataset
#from NewBBOX import NewBBOX as ne
from .NewBBOX import NewBBOX as ne
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
    total = np.zeros((0, l[1] * l[2]), dtype=np.float32)
    i = 0
    for i in range(24):
        tempData = array[i]
        array1D = []
        for x in tempData:
            for s in x:
                array1D.append(s)
        total = np.insert(total, i, array1D, axis=0)
    return total


def divData(data, numRow, numColumns):
    """
    Function to divide the data matrix into 4 submatrices

    :param data: information of NetCDF
    :type data: NetCDF
    :return : 4 submatrices
    :return type : matrix float32
    """
    totalArrays = numRow * numColumns
    total = np.zeros((0, totalArrays), dtype=np.float32)
    for i in range(120):
        dataValue = data[i]
        array1D = []
        # size = dataValue.shape
        # numRows = int(size[0] / 2)
        # numColumns = int(size[1] / 2)
        # dataSecc1 = dataValue[0:numRows, 0:numColumns]
        # dataSecc2 = dataValue[numRows:, 0:numColumns]
        # dataSecc3 = dataValue[0:numRows, numColumns:]
        # dataSecc4 = dataValue[numRows:, numColumns:]
        # prom1 = dataSecc1.sum() / (numColumns * numRows)
        # prom2 = dataSecc2.sum() / (numColumns * numRows)
        # prom3 = dataSecc3.sum() / (numColumns * numRows)
        # prom4 = dataSecc4.sum() / (numColumns * numRows)
        # array1D.append(prom1)
        # array1D.append(prom2)
        # array1D.append(prom3)
        # array1D.append(prom4)
        rows = []
        div = np.vsplit(dataValue, numRow)
        for xs in div:
            divSplit = np.array_split(xs, numColumns)
            for ls in divSplit:
                rows.append(ls)
        for ys in rows:
            meanVal = np.mean(ys)
            array1D.append(meanVal)
        total = np.insert(total, i, array1D, axis=0)
    return total


def makeDates(date):
    """
    Function to create a list with the format year-month-day hours:minutes:seconds

    from 00 hours to 23 hours
    :param date : initial date
    :param type : string
    :return : list with the dates
    :return type : list datatime
    """
    listDates = []
    date = date + ' 00:00:00'
    d = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    listDates.append(d)
    for x in range(119):
        d = d + timedelta(hours=1)
        listDates.append(d)
    allData = df.DataFrame(listDates, columns=['fecha'])
    return allData


def nameColumns(name, numbColumns):
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
    namesColumns = []
    for i in range(numbColumns):
        nColumn = name + '_' + str(i)
        namesColumns.append(nColumn)
    return namesColumns


def makeCsv(net, date, opt, path, numRow, numColumns, minlat, maxlat, minlon, maxlon, variables):
    """
    Function to create .csv files of some variables that are in a NetCDF file,

    the .cvs file is saved in the data/NetCDF path of the project
    :param net : NetCDF file information
    :param type: NetCDF type
    :param date: initial date
    :param type: string
    """
    LON = net.variables['XLONG'][:]
    LAT = net.variables['XLAT'][:]

    LON = LON[1][1]
    LAT = LAT[1]

    LONsize = len(LON)
    LATsize = len(LAT)

    celda = []
    var_cut = []
    for i in variables:
        var = net.variables[i][:]
        celda.append(var)
        result = ne(var, LON, LAT, LONsize, LATsize, minlat, maxlat, minlon, maxlon)
        var_cut.append(result[0])

    for ls in range(len(var_cut)):
        saveData(var_cut[ls], variables[ls], date, opt, path, numRow, numColumns)


def saveData(var, variables, date, opt, path, numRow, numColumns):
    """
    function to save the information in a .csv file

    :param var: information of NetCDF
    :type var: NetCDF
    :param variables: meteorological variables
    :type variables: String
    :param date: date of day
    :type date: date
    :param opt: option to save file
    :type opt: int
    :param path: address where it is saved in .cvs file
    :type path: String
    """
    dateVal = makeDates(date)
    allData = makeDates(date)
    # temp = conver1D(var);
    temp = divData(var, numRow, numColumns)
    dataMatrix = temp
    name = variables + '_' + date + '.csv'
    myIndex = nameColumns(variables, len(temp[0]))
    tempFrame = df.DataFrame(dataMatrix, columns=myIndex)
    allData = concat([allData, tempFrame], axis=1)
    allData = allData.fillna(value=0)
    meanAllData = allData.mean(axis=1)
    meanValues = meanAllData.as_matrix()
    mean = df.DataFrame(meanValues, columns=[variables + '_mean'])
    dateVal[variables + '_mean'] = mean
    if opt == 0:
        allData.to_csv(path + name, encoding='utf-8', index=False)
    elif opt == 1:
        filq = path + name
        dateVal.to_csv(filq, encoding='utf-8', index=False)
    elif opt == 2:
        filq = path + name
        allData.to_csv(filq, encoding='utf-8', index=False)


def open_netcdf(ls, nameFile, cadena, pathCopyData):
    """
    Function to open a NetCDF file

    :param ls: address file
    :type ls: String
    :param nameFile: file name
    :type nameFile: String
    :param cadena: name of the file without extension
    :type cadena: String
    :param pathCopyData: address to copy the file
    :type pathCopyData: String
    :return : data in NetCDF
    :type return: NetCDF
    """
    name = '.nc.tar.gz'
    name1 = '.nc.gz'
    patron = re.compile('.*' + name)
    patron2 = re.compile('.*' + name1)
    fname = pathCopyData + nameFile
    if patron.match(nameFile) != None:
        comp = tarfile.open(ls, 'r')
        comp.extract(cadena, pathCopyData)
        comp.close()
        data = Dataset(pathCopyData + cadena)
        os.remove(pathCopyData + cadena)
    elif patron2.match(nameFile) != None:
        shutil.copy(ls, fname)
        infile = gzip.open(fname, 'rb')
        tmp = tempfile.NamedTemporaryFile(delete=False)
        shutil.copyfileobj(infile, tmp)
        infile.close()
        tmp.close()
        data = Dataset(tmp.name)
        os.unlink(tmp.name)
        os.remove(fname)
    else:
        data = Dataset(ls)
    # os.remove(fname);
    return data


def clearString(name):
    """
    function to remove the extension of a file

    :param name: file name
    :type name: String
    :return: name file witout extension
    :return type: String
    """
    if name.find(".tar") != 0:
        name = name.replace(".tar", "")

    if name.find(".gz") != 0:
        name = name.replace(".gz", "")
    return name


def checkFile(net, name, date, opt, path, numRow, numColumns, minlat, maxlat, minlon, maxlon, variables):
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
        net.variables['XLONG'][:]
        net.variables['XLAT'][:]
        makeCsv(net, date, opt, path, numRow, numColumns, minlat, maxlat, minlon, maxlon, variables)
    except KeyError:
        print('error in file: ' + name)
