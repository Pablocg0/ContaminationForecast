from datetime import datetime, timedelta
import prediction as pre
import pandas as df
import numpy as np
from Utilites.FormatData import FormatData as fd
from time import time
import calendar
import configparser
import math
import sys

def forecast_month(month, year, dirData, dirTotalCsv, dirTrain,estacion, contaminant):
    lastDay = calendar.monthrange(year,month)[1]
    fechaInicio =  str(year) + '-' + numString(month) + '-01 00:00:00'
    fechaFinal = str(year) + '-' + numString(month) + '-'+ numString(lastDay) +' 23:00:00'
    #print(fechaInicio)
    #print(fechaFinal)
    data = fd.readData(fechaInicio, fechaFinal, [estacion], contaminant)
    data = separateDate(data)
    data = unionMeteorologia(data,dirTotalCsv)
    data = data.fillna(value=-1)
    #print(data)
    #sys.out
    frame_dates = data['fecha'].values
    data =  filterData(data, dirData + estacion + "_" + contaminant + ".csv")
    data = data.fillna(value=-1)
    index = data.index.values
    arrayPred = []
    for x in index:
        pred = data.ix[x].values
        valPred= pred[1:]
        valNorm = pre.normalize(valPred,estacion, contaminant, dirData)
        arrayPred.append(convert(valNorm))
    result = pre.prediction(estacion, contaminant, arrayPred, dirTrain, dirData)
    nameCont = findTable2(contaminant)
    real = pre.desNorm(result, estacion,contaminant, dirData, nameCont + '_')
    for xs in range(len(frame_dates)):
        fecha = frame_dates[xs]
        ts = df.to_datetime(str(fecha))
        fecha_string = ts.strftime('%Y-%m-%d %H:%M:%S')
        pronostico = real[xs]
        guardarPrediccion(estacion, fecha_string,[pronostico],contaminant,4)


def unionMeteorologia(data,dirTotalCsv):
    dataFestivos = df.read_csv('/ServerScript/AirQualityModel/ContaminationForecast/Data/Festivos.csv')
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
    #allD = data.dropna(axis=0, how='any')
    # allD = data.fillna(value=-1)
    data = data.reset_index()
    data = data.drop(labels='index', axis=1)
    return data

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


def guardarPrediccion(estacion, fecha, Valor,contaminant,tipo):
    """
    function to save the prediction in the database

    :param estacion: name the station
    :type estacion: string
    :param fecha: current date
    :type fecha: date
    :param valor: prediction value
    :type valor: float32
    """
    if math.isnan(Valor[0]):
        print('no valor')
        return 0
    fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
    if estacion == 'SFE':
        fecha = fecha + timedelta(days = 1)
        fecha1 = fecha + timedelta(hours = 6)
        fechaActual = str(fecha1.year) + '-' + numString(fecha1.month) + '-' + numString(fecha1.day)+' '+numString(fecha1.hour)+':00:00'
        rept = fd.rev_data(estacion,fechaActual,findT(contaminant),tipo)
        if rept == 0:
            fd.saveData(estacion, fechaActual, Valor, findT(contaminant),tipo)
        else:
            print('valor repetido')
    elif estacion == 'NEZ':
        fecha = fecha + timedelta(days=1)
        fecha = fecha + timedelta(hours = 11)
        fechaActual = str(fecha.year) + '-' + numString(fecha.month) + '-' + numString(fecha.day)+' '+numString(fecha.hour)+':00:00'
        rept = fd.rev_data(estacion,fechaActual,findT(contaminant),tipo)
        if rept == 0:
            fd.saveData(estacion, fechaActual, Valor, findT(contaminant),tipo)
        else:
            print('valor repetido')
    elif estacion == 'TAH':
        fecha = fecha + timedelta(days=1)
        fecha = fecha + timedelta(hours=15)
        fechaActual = str(fecha.year) + '-' + numString(fecha.month) + '-' + numString(fecha.day)+' '+numString(fecha.hour)+':00:00'
        rept = fd.rev_data(estacion,fechaActual,findT(contaminant),tipo)
        if rept == 0:
            fd.saveData(estacion, fechaActual, Valor, findT(contaminant),tipo)
        else:
            print('valor repetido')
    elif estacion == 'UAX':
        fecha = fecha + timedelta(days=1)
        fecha = fecha + timedelta(hours=13)
        fechaActual = str(fecha.year) + '-' + numString(fecha.month) + '-' + numString(fecha.day)+' '+numString(fecha.hour)+':00:00'
        rept = fd.rev_data(estacion,fechaActual,findT(contaminant),tipo)
        if rept == 0:
            fd.saveData(estacion, fechaActual, Valor, findT(contaminant),tipo)
        else:
            print('valor repetido')
    else:
        fecha = fecha + timedelta(days=1)
        fechaActual = str(fecha.year) + '-' + numString(fecha.month) + '-' + numString(fecha.day)+' '+numString(fecha.hour)+':00:00'
        rept = fd.rev_data(estacion,fechaActual,findT(contaminant),tipo)
        if rept == 0:
            fd.saveData(estacion, fechaActual, Valor, findT(contaminant),tipo)
        else:
            print('valor repetido')


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


def numString(num):
    """
    function to convert a number of a digit into a string with two digits

    :param num:number to convert
    :type num: string
    :return : string with two digits
    :type return: String
    """
    if num == 0:
        return "00"
    if num < 10:
        return "0" + str(num)
    else:
        return str(num)

def findTable2(fileName):
        if "PM2.5" in fileName:
            return "cont_pmdoscinco"

        if "PM10" in fileName:
            return "cont_pmdiez"

        if "NOX" in fileName:
            return "cont_nox"

        if "CO2" in fileName:
            return "cont_codos"

        if "PMCO" in fileName:
            return "cont_pmco"

        if "CO" in fileName:
            return "cont_co"

        if "NO2" in fileName:
            return "cont_nodos"

        if "NO" in fileName:
            return "cont_no"

        if "O3" in fileName:
            return "cont_otres"

        if "SO2" in fileName:
            return "cont_sodos"

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
    actual = datetime.now()
    month = actual.month
    year = actual.year
    if month == 1:
        month = 12
        year = year - 1
    else:
        month = month -1
    contaminant = str(sys.argv[1])
    config = configparser.ConfigParser()
    config.read('/home/pablo/ContaminationForecast/modulos/forecast/confForecast_UpdateMonth.conf')
    dirData = config.get('forecast_month', 'dirData')
    dirTotalCsv = config.get('forecast_month', 'dirTotalCsv')
    dirTrain = config.get('forecast_month', 'dirTrain')
    estaciones = config.get('forecast_month', 'estaciones')
    estaciones = estaciones.split()
    for xs in estaciones:
        print('Update mensual de la estacion: ' + xs)
        forecast_month(month, year, dirData, dirTotalCsv, dirTrain +contaminant+ '/', xs, contaminant)

init()
