'''
File name : forecastDate.py
Author: Pablo Camacho Gonzalez
Python version: 3.6.4
Date last modified: 27/02/2018
'''


from datetime import datetime, timedelta
import prediction as pre
from Utilites.metricas import metricas
import pandas as df
import numpy as np
from Utilites.FormatData import FormatData as fd
from time import time
import configparser
import sys


def totalPredection(est, dirData, dirrDataC, dirTrain, contaminant,columnContaminant, fechaInicio, fechaFin):
    """
    function to send to do the forecast of a station and graph it

    :param station: name the station
    :type station: String
    :param dirData: address of the files with training information
    :type dirData: String
    :param dirTrain: address of the training files of the neural network
    :type dirTrain: String
    :param columnContaminant:name of the pollutant in the DataFrame
    :type columnContaminant: String
    :param fechaInicio: start date of the forecast
    :type fechaInicio: date
    :param fechaFin: end date of the forecast
    :type fechaFin: date
    """
    for x in est:
        print(x)
        forecastDate(x, dirData, dirrDataC, dirTrain, contaminant, columnContaminant, fechaInicio, fechaFin)


def forecastDate(station, dirData, dirrDataC, dirTrain, contaminant, columnContaminant, fechaInicio, fechaFin):
    """
    function to make the forecast of a whole year and graph it

    :param station: name the station
    :type station: String
    :param dirData: address of the files with training information
    :type dirData: String
    :param dirTrain: address of the training files of the neural network
    :type dirTrain: String
    :param columnContaminant:name of the pollutant in the DataFrame
    :type columnContaminant: String
    :param fechaInicio: start date of the forecast
    :type fechaInicio: date
    :param fechaFin: end date of the forecast
    :type fechaFin: date
    """
    sta = station
    name = sta + '_' + contaminant
    temp = df.read_csv(dirrDataC + name + '.csv')  # we load the data in the Variable data
    temp = temp.fillna(value=-1.0)
    data = temp[(temp['fecha'] <= fechaFin) & (temp['fecha'] >= fechaInicio)]
    data = data.reset_index(drop=True)
    data = filterData(data, dirData + name + '.csv')
    data = data.fillna(value=-1.0)
    dataTemp = data['fecha'].values
    print(dataTemp)
    nameColumn = columnContaminant +'_'+ sta + '_delta'
    index = data.index.values
    arrayPred = []
    for x in index:
        pred = data.ix[x].values
        valPred = pred[1:]
        valNorm = pre.normalize(valPred, sta, contaminant, dirData)
        arrayPred.append(convert(valNorm))
    result = pre.prediction(sta, contaminant, arrayPred, dirTrain + contaminant + '/', dirData)
    real = desNorm(result, sta, contaminant, dirData, columnContaminant)
    dataPrediccion = real
    savePrediccion(station, dataPrediccion, contaminant, dataTemp)

def filterData(data, dirData):
    """
    function to remove the columns of a dataframe

    :param data: dataframe to which the columns will be removed
    :type data: DataFrame
    :param dirData: address of the files with training information
    :type dirData: String
    :return: DataFrame
    """
    temp = df.read_csv(dirData)
    listColumns = list(temp.columns)
    data = data.loc[:, listColumns]
    return data

def convert(data):
    """
    function to convert a matrix into an array

    :param data: matrix to convert
    :type param: matrix
    :return: array
    :type return: array float32
    """
    size = len(data)
    vl = np.ones([1, size])
    i = 0
    for x in data:
        vl[0, i] = x
        i += 1
    return vl

def desNorm(data, station, contaminant, dirData, columnContaminant):
    """
    function to denormalize a value

    :param data: value to be unmasked
    :type data: float32
    :param station: name the stations
    :type station: String
    :param contaminant: name the pollutant
    :type contaminant: String
    :param dirData: address of the files with training information
    :type dirData: String
    """
    real = []
    nameC = columnContaminant + '_' + station.lower()
    # nameC= columnContaminant
    name = station + '_' + contaminant
    values = df.read_csv(dirData + name + '_MaxMin.csv')
    index = values.columns[0]
    va = values[(values[index] == nameC)]
    maxx = va['MAX'].values[0]
    minn = va['MIN'].values[0]
    for x in data:
        realVal = (x * (maxx - minn)) + minn
        real.append(realVal)
    return real

def savePrediccion(estacion, dataPrediccion, contaminant, fechas):
    """
    function to save the prediction in the database

    :param estacion: name the station
    :type estacion: string
    :param fecha: current date
    :type fecha: date
    :param valor: prediction value
    :type valor: float32
    """
    print(findT(contaminant))
    if estacion == 'SFE':
        size = len(dataPrediccion)
        for i in range(size):
            fecha = fechas[i]
            Valor = dataPrediccion[i]
            fecha =  datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
            fecha = fecha + timedelta(days=1)
            fecha = fecha + timedelta(hours = 6)
            fechaActual = str(fecha.year) + '-' + str(fecha.month) + '-' + str(fecha.day)+' '+str(fecha.hour)+':00:00'
            fd.saveData(estacion, fechaActual, [Valor], findT(contaminant),2)
    elif estacion == 'NEZ':
        size = len(dataPrediccion)
        for i in range(size):
            fecha = fechas[i]
            Valor = dataPrediccion[i]
            fecha =  datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
            fecha = fecha + timedelta(days=1)
            fecha = fecha + timedelta(hours = 11)
            fechaActual = str(fecha.year) + '-' + str(fecha.month) + '-' + str(fecha.day)+' '+str(fecha.hour)+':00:00'
            fd.saveData(estacion, fechaActual, [Valor], findT(contaminant),2)
    elif estacion == 'TAH':
        size = len(dataPrediccion)
        for i in range(size):
            fecha = fechas[i]
            Valor = dataPrediccion[i]
            fecha =  datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
            fecha = fecha + timedelta(days=1)
            fecha = fecha + timedelta(hours = 15)
            fechaActual = str(fecha.year) + '-' + str(fecha.month) + '-' + str(fecha.day)+' '+str(fecha.hour)+':00:00'
            fd.saveData(estacion, fechaActual, [Valor], findT(contaminant),2)
    elif estacion == 'UAX':
        size = len(dataPrediccion)
        for i in range(size):
            fecha = fechas[i]
            Valor = dataPrediccion[i]
            fecha =  datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
            fecha = fecha + timedelta(days=1)
            fecha = fecha + timedelta(hours = 13)
            fechaActual = str(fecha.year) + '-' + str(fecha.month) + '-' + str(fecha.day)+' '+str(fecha.hour)+':00:00'
            fd.saveData(estacion, fechaActual, [Valor], findT(contaminant),2)
    else:
        size = len(dataPrediccion)
        for i in range(size):
            fecha = fechas[i]
            Valor = dataPrediccion[i]
            fecha =  datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
            fecha = fecha + timedelta(days=1)
            fechaActual = str(fecha.year) + '-' + str(fecha.month) + '-' + str(fecha.day)+' '+str(fecha.hour)+':00:00'
            fd.saveData(estacion, fechaActual, [Valor], findT(contaminant),2)



def findT(fileName):
        if "PM2.5" in fileName:
            return "forecast_pmdoscinco"

        if "PM10" in fileName:
            return "forecast_pmdiez"

        if "NOX" in fileName:
            return "forecast_nox"

        if "CO2" in fileName:
            return "forecast_codos"

        if "PMCO" in fileName:
            return "forecast_pmco"

        if "CO" in fileName:
            return "forecast_co"

        if "NO2" in fileName:
            return "forecast_nodos"

        if "NO" in fileName:
            return "forecast_no"

        if "O3" in fileName:
            return "forecast_otres"

        if "SO2" in fileName:
            return "forecast_sodos"


def init():
    contaminant = str(sys.argv[1])
    columnContaminant = str(sys.argv[2])
    print(contaminant)
    print(columnContaminant)
    config = configparser.ConfigParser()
    config.read('/ServerScript/AirQualityModel/ContaminationForecast/modulos/forecast/forecastDate.conf')
    dirData = config.get('forecastDate', 'datos')
    dirrDataC = config.get('forecastDate', 'datosComp')
    dirTrain = config.get('forecastDate', 'train')
    fechaInicio = config.get('forecastDate', 'fechaInicio')
    fechaFin = config.get('forecastDate', 'fechaFin')
    est = config.get('forecastDate', 'estaciones' + contaminant)
    est  = est.split()
    totalPredection(est, dirData+ contaminant+'/', dirrDataC+ contaminant+'/', dirTrain, contaminant,columnContaminant, fechaInicio, fechaFin)

init()
