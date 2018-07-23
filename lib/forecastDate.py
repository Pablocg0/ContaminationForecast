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
        #forecastDate(x, dirData, dirrDataC, dirTrain, contaminant, columnContaminant, fechaInicio, fechaFin)
        forecastDate2(x, dirData, dirrDataC, dirTrain, contaminant, columnContaminant, fechaInicio, fechaFin, '/ServerData/DataCsv/totalCuadrantes/')


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


def forecastDate2(station, dirData, dirrDataC, dirTrain, contaminant, columnContaminant, fechaInicio, fechaFin, dirTotalCsv):
    sta = station
    name = sta + '_' + contaminant
    tempData  = baseContaminantes(fechaInicio, fechaFin, station, contaminant)
    if tempData.empty:
        dataBackup = back(dirData, contaminant)
        data = dataBackup
        data = data.fillna(value=-1)
        data = filterData(data, dirData + name + ".csv")
        data = data.fillna(value=-1)
        temp = data.ix[0].values
        temp = temp[1:]
        dataPred = pre.normalize(temp, sta, contaminant, dirData)
        dataPred = convert(dataPred)
        prediccion = pre.prediction(sta, contaminant, [dataPred], dirTrain, dirData)
    else:
        data =  tempData.dropna(axis=1, how = 'all')
        data = data.fillna(value = -1)
        data = data.reset_index(drop = True)
        data = separateDate(data)
        data = unionData(data,dirTotalCsv)
        data = data.drop_duplicates(keep='first')
        data = filterData(data,dirData + name + '.csv')
        data = data.fillna(value = -1)
        dataTemp = data['fecha']
        index = data.index.values
        print(data)
        arrayPred = []
        for x in index:
            pred = data.ix[x].values
            valPred = pred[1:]
            valNorm = pre.normalize(valPred, sta,  contaminant, dirData)
            arrayPred.append(convert(valNorm))
        result = pre.prediction(sta,contaminant,arrayPred, dirTrain,dirData)
        real = desNorm(result, sta, contaminant, dirData, columnContaminant)
        dataPrediccion =  real
        savePrediccion(station, dataPrediccion, contaminant, dataTemp)

def back(dirData, contaminant):
    if contaminant == 'PM10':
        temp = df.read_csv(dirData + 'TAH_' + contaminant + '.csv')
    else:
        temp = df.read_csv(dirData + "MGH_" + contaminant + ".csv")
    return temp.loc[:0]


def baseContaminantes(fechaInicio, fechaFinal, estacion, contaminant):
    """
    function to bring the information of the contaminants from the database

    :param fecha: date to bring the information
    :type fecha: date
    :param estacion:name of the station from which the information is extracted
    :type estacion: String
    :return: array with pollutant information
    :type return: array float32
    """
    #fechaFinal = str(fechaFinal.year) + '-' + numString(fechaFinal.month) + '-' + numString(fechaFinal.day)+' '+numString(fecha.hour)+':00:00'
    #fechaInicio = str(fechaInicio.year) + '-' + numString(fechaInicio.month) + '-' + numString(fechaInicio.day)+' '+numString(fecha.hour)+':00:00'
    data = fd.readData(fechaInicio, fechaFinal, [estacion], contaminant)
    return data.fillna(value=-1)

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

def savePrediccion1(estacion, dataPrediccion, contaminant, fechas):
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
    size = len(dataPrediccion)
    for i in range(size):
        fecha = fechas.iloc[i]
        print(fecha)
        Valor = dataPrediccion[i]
        #fecha =  datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
        if estacion == 'TAH':
            fecha = fecha + timedelta(hours =15)
        else:
            fecha = fecha + timedelta(days=1)
        fechaActual = str(fecha.year) + '-' + str(fecha.month) + '-' + str(fecha.day)+' '+str(fecha.hour)+':00:00'
        fd.saveData(estacion, fechaActual, [Valor[0]], findT(contaminant),3)


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
            fecha = fechas.iloc[i]
            Valor = dataPrediccion[i]
            #fecha =  datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
            fecha = fecha + timedelta(days=1)
            fecha = fecha + timedelta(hours = 6)
            fechaActual = str(fecha.year) + '-' + str(fecha.month) + '-' + str(fecha.day)+' '+str(fecha.hour)+':00:00'
            fd.saveData(estacion, fechaActual, [Valor], findT(contaminant),2)
    elif estacion == 'NEZ':
        size = len(dataPrediccion)
        for i in range(size):
            fecha = fechas.iloc[i]
            Valor = dataPrediccion[i]
            #fecha =  datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
            fecha = fecha + timedelta(days=1)
            fecha = fecha + timedelta(hours = 11)
            fechaActual = str(fecha.year) + '-' + str(fecha.month) + '-' + str(fecha.day)+' '+str(fecha.hour)+':00:00'
            fd.saveData(estacion, fechaActual, [Valor], findT(contaminant),2)
    elif estacion == 'TAH':
        size = len(dataPrediccion)
        for i in range(size):
            fecha = fechas.iloc[i]
            Valor = dataPrediccion[i]
            #fecha =  datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
            fecha = fecha + timedelta(days=1)
            fecha = fecha + timedelta(hours = 15)
            fechaActual = str(fecha.year) + '-' + str(fecha.month) + '-' + str(fecha.day)+' '+str(fecha.hour)+':00:00'
            fd.saveData(estacion, fechaActual, [Valor], findT(contaminant),2)
    elif estacion == 'UAX':
        size = len(dataPrediccion)
        for i in range(size):
            fecha = fechas.iloc[i]
            Valor = dataPrediccion[i]
            #fecha =  datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
            fecha = fecha + timedelta(days=1)
            fecha = fecha + timedelta(hours = 13)
            fechaActual = str(fecha.year) + '-' + str(fecha.month) + '-' + str(fecha.day)+' '+str(fecha.hour)+':00:00'
            fd.saveData(estacion, fechaActual, [Valor], findT(contaminant),2)
    else:
        size = len(dataPrediccion)
        for i in range(size):
            fecha = fechas.iloc[i]
            Valor = dataPrediccion[i]
            #fecha =  datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
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

def separateDate(data):
    """
    Function to separate the date in year, month ,day and the function sine of each one of them

    :parama data: DataFrame that contains the dates
    :type data: DataFrame
    """
    dates = data['fecha']
    lenght = len(dates.index)
    years = np.ones((lenght, 1)) * -1
    sinYears = np.ones((lenght, 1)) * -1
    months = np.ones((lenght, 1)) * -1
    sinMonths = np.ones((lenght, 1)) * -1
    days = np.ones((lenght, 1)) * -1
    sinDays = np.ones((lenght, 1)) * -1
    wDay = np.ones((lenght, 1)) * -1
    sinWday = np.ones((lenght, 1)) * -1
    i = 0
    for x in dates:
        d = x
        # d = datetime.strptime(x,"%Y-%m-%d %H:%M:%S")
        wD = weekday(d.year, d.month, d.day)
        wDay[i] = wD[0]
        sinWday[i] = wD[1]
        years[i] = d.year
        # sinYears[i]= np.sin(d.year)
        months[i] = d.month
        sinMonths[i] = (1 + np.sin(((d.month - 1) / 11) * (2 * np.pi))) / 2
        days[i] = d.day
        sinDays[i] = (1 + np.sin(((d.day - 1) / 23) * (2 * np.pi))) / 2
        i += 1
    weekD = df.DataFrame(wDay, columns=['weekday'])
    data['weekday'] = weekD
    sinWeekD = df.DataFrame(sinWday, columns=['sinWeekday'])
    data['sinWeekday'] = sinWeekD
    dataYear = df.DataFrame(years, columns=['year'])
    data['year'] = dataYear
    # dataSinYear = df.DataFrame(sinYears, columns= ['sinYear'])print(data)
    # data['sinYear'] = dataSinYear
    dataMonths = df.DataFrame(months, columns=['month'])
    data['month'] = dataMonths
    dataSinMonths = df.DataFrame(sinMonths, columns=['sinMonth'])
    data['sinMonth'] = dataSinMonths
    dataDay = df.DataFrame(days, columns=['day'])
    data['day'] = dataDay
    dataSinDay = df.DataFrame(sinDays, columns=['sinDay'])
    data['sinDay'] = dataSinDay
    return data

def unionData(data, dirTotalCsv):
    """
    Function to join the data of the netcdf and the data of the pollutants

    :param data: dataFrame(minollutants data
    :type data: dataFrame
    :return: dataFrame
    """
    dataFestivos = df.read_csv('../../Data/Festivos.csv')
    dataFestivos = dataFestivos.drop('Unnamed: 0', axis=1)
    dataFestivos2 = convertDates(dataFestivos)
    data = data.merge(dataFestivos2, how='left', on='fecha')
    data = data.reset_index()
    data = data.drop(labels='index', axis=1)
    variables = ['U10', 'V10', 'RAINC', 'T2', 'TH2', 'RAINNC', 'PBLH', 'SWDOWN', 'GLW']
    netcdf = dirTotalCsv
    for i in variables:
        netcdf += i + '_total.csv'
        dataNet = df.read_csv(netcdf)
        dataNet2 = convertDates(dataNet)
        data = data.merge(dataNet2, how='left', on='fecha')
        netcdf = dirTotalCsv
    allD = data.dropna(axis=0, how='any')
    # allD = data.fillna(value=-1)
    allD = allD.reset_index()
    allD = allD.drop(labels='index', axis=1)
    return allD

def convertDates(data):
    """
    function to convert a string into a date and save it in a dataframe

    :param data: dataframe with the dates to convert
    :type data : DataFrame
    :return: DataFrame
    """
    fecha = data['fecha']
    data = data.drop(labels='fecha', axis=1)
    date = []
    for i in fecha:
        datef = datetime.strptime(i, '%Y-%m-%d %H:%M:%S')
        date.append(datef)
    dataTemp = df.DataFrame(date, columns=['fecha'])
    data['fecha'] = dataTemp
    return data

def weekday(year, month, day):
    """
    Function to take day of the week using the congruence of Zeller , 1 is Sunday

    :param year: year of the date
    :type year: int
    :param month: month of the date
    :type month: int
    :param day: day of the date
    :type day: int
    :return: int, 1 is Sunday
    """
    a = (14 - month) / 12
    a = int(a)
    y = year - a
    m = month + 12 * a - 2
    week = (day + y + int(y / 4) - int(y / 100) + int(y / 400) + int((31 * m) / 12)) % 7
    week = week + 1
    sinWeek = (1 + np.sin(((week - 1) / 7) * (2 * np.pi))) / 2
    return [week, sinWeek]


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
