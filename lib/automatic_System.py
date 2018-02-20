from datetime import datetime, timedelta
from Utilites.FormatData import FormatData as fd
from Utilites.Utilites import prepro as an
import time
import sys, os
import pandas as df
import numpy as np
import prediction as pre
import autoTraining as tr
from NetCDF.automatic_MakeCsv import open_netcdf, checkFile
import configparser


def configuracion(variables):
    """
    function to extract the name of the NetCDF file from the current day and
    from a previous day

    :param Variable: meteorological variables
    :type variables: String list
    :return: list with the name of the files and the day
    :type return: String list
    """
    nameNetcdf = "wrfout_d02_"
    actual = datetime.now()
    actual = actual - timedelta(hours=1)
    actualNetcdf = nameNetcdf + str(actual.year) + "-" + numString(actual.month) + "-"+numString(actual.day)+"_00.nc";
    actualCsv = variables[0] + "_" + str(actual.year) + "-" + numString(actual.month)+ "-"+numString(actual.day)+".csv";
    ayer = actual - timedelta(days=1)
    ayerCsv = variables[0] + "_" + str(ayer.year) + "-" + numString(ayer.month) + "-"+numString(ayer.day)+".csv";
    return [actual, ayer, actualNetcdf, actualCsv, ayerCsv]


def buscarArchivo(archivo, carpeta):
    """
    function to search a file in a defined folder

    :param archivo: file to search
    :type archivo: String
    :param carpeta: address where the file will be searched
    :type crpeta: String
    :return: true or false
    :type return: boolean
    """
    for root, dir, ficheros in os.walk(carpeta, topdown=True):
        for i in ficheros:
            if archivo in i:
                return True
    return False


def leerArchivo(informacion, estaciones, variables, dirNetCDF, dirCsv, dirData, dirTrain, dirFestivos, dataBackup, path, pathCopyData, contaminant,numRow, numColumns, minlat, maxlat, minlon, maxlon):
    """
    function for the automatic prediction of ozone

    :param informacion:name of netcdf and current date
    :type informacion: list
    :param estaciones: list with weather stations
    :type estaciones: list
    :param variables: meteorological variables
    :param dirNetCDF: address of netcdf files
    :type dirNetCDF : String
    :param dirCsv: Address of processed meteorology archives
    :type dirCsv : String
    :param dirData: address of the files with training information
    :type dirData: String
    :param dirTrain: address of the training files of the neural network
    :type dirTrain: String
    :param dirFestivos: address of the file with the holidays
    :type dirFestivos: String
    :param path:  address where it is saved in .cvs file
    :type path: String
    :param pathCopyData: address to copy the file
    :type pathCopyData: String
    """
    print(dirTrain)
    print(dirData)
    dataBackup = back(dirData, contaminant)
    if buscarArchivo(informacion[3], dirCsv):
        fecha = str(informacion[0].year) + "-" + numString(informacion[0].month)+"-"+numString(informacion[0].day)
        dataMet = unionMeteorologia(fecha, informacion[0], dirCsv, variables)
        dataMet = dataMet.drop('fecha', axis=1)
        for value in estaciones:
            print(value)
            data = baseContaminantes(informacion[0], value, contaminant)
            if data.empty:
                data = dataBackup
                data = data.fillna(value=-1)
                data = filterData(data, dirData + value + "_" + contaminant + ".csv")
                data = data.fillna(value=-1)
                valPred = prediccion(value, data, dirData, dirTrain, contaminant)
                print("Informacion insuficiente para la prediccion")
                guardarPrediccion(value, informacion[0], [-1], contaminant)
            else:
                # data = data.merge(dataMet,how='left', on='fecha');
                data = separateDate(data)
                data = unionData(data, informacion[0], dirFestivos)
                data = df.concat([data, dataMet], axis=1)
                data = data.fillna(value=-1)
                data = filterData(data, dirData + value + "_" + contaminant + ".csv")
                data = data.fillna(value=-1)
                data = data.loc[0:0]
                print(data)
                valPred = prediccion(value, data, dirData, dirTrain, contaminant)
                print(valPred)
                guardarPrediccion(value, informacion[0], valPred, contaminant)
    elif buscarArchivo(informacion[2], dirNetCDF):  # NetCDF
        direccioNetCDF = dirNetCDF +'0' +str(informacion[0].month) + "_" + deMonth(informacion[0].month) + "/"
        data = open_netcdf(direccioNetCDF + informacion[2], informacion[2], informacion[2], pathCopyData);
        fecha = str(informacion[0].year) + "-" + numString(informacion[0].month)+"-"+numString(informacion[0].day)
        checkFile(data, informacion[2], fecha, 2, path, numRow, numColumns, minlat, maxlat, minlon, maxlon, variables)
        dataMet = unionMeteorologia(fecha, informacion[0], dirCsv, variables)
        dataMet = dataMet.drop('fecha', axis=1)
        for value in estaciones:
            data = baseContaminantes(informacion[0], value, contaminant)
            if data.empty:
                data = dataBackup
                data = data.fillna(value=-1)
                data = filterData(data, dirData + value + "_" + contaminant + ".csv")
                data = data.fillna(value=-1)
                valPred = prediccion(value, data, dirData, dirTrain, contaminant)
                print("Informacion insuficiente para la prediccion")
                guardarPrediccion(value, informacion[0], [-1], contaminant)
            else:
                data = separateDate(data)
                data = unionData(data, informacion[0], dirFestivos)
                data = df.concat([data, dataMet], axis=1)
                data = data.fillna(value=-1)
                data = filterData(data, dirData + value + "_" + contaminant + ".csv")
                data = data.fillna(value=-1)
                data = data.loc[0:0]
                print(data)
                valPred = prediccion(value, data, dirData, dirTrain, contaminant)
                print(valPred)
                guardarPrediccion(value, informacion[0], valPred, contaminant)
    else:
        if buscarArchivo(informacion[4], dirCsv):
            # buscarArchivo(informacion[4]); #csv ayer
            fechaAyer = str(informacion[1].year) + "-" + numString(informacion[1].month)+"-"+numString(informacion[1].day)
            dataMet = unionMeteorologia(fechaAyer, informacion[1], dirCsv, variables)
            dataMet = dataMet.drop('fecha', axis=1)
            for value in estaciones:
                print(value)
                data = baseContaminantes(informacion[0], value, contaminant)
                if data.empty:
                    data = dataBackup
                    data = data.fillna(value=-1)
                    data = filterData(data, dirData + value + "_" + contaminant + ".csv")
                    data = data.fillna(value=-1)
                    valPred = prediccion(value, data, dirData, dirTrain, contaminant)
                    print("Informacion insuficiente para la prediccion")
                    guardarPrediccion(value, informacion[0], [-1], contaminant);
                else:
                    data = separateDate(data)
                    data = unionData(data, informacion[0], dirFestivos)
                    data = df.concat([data, dataMet], axis=1)
                    data = filterData(data, dirData + value + "_" + contaminant + ".csv")
                    data = data.fillna(value=-1)
                    data = data.loc[0:0]
                    print(data)
                    valPred = prediccion(value, data, dirData, dirTrain, contaminant)
                    print(valPred)
                    guardarPrediccion(value, informacion[0], valPred, contaminant)
        else:
            anteAyer = informacion[1] - timedelta(days=1)
            nameCsv = variables[0]+"_"+str(anteAyer.year)+ "-"+ numString(anteAyer.month)+ "-"+numString(anteAyer.day)+".csv";
            fechaAnteAyer = str(anteAyer.year) + "-" + numString(anteAyer.month)+"-"+numString(anteAyer.day)
            dataMet = unionMeteorologia(fechaAnteAyer, anteAyer, dirCsv, variables)
            dataMet = dataMet.drop('fecha', axis=1)
            for value in estaciones:
                print(value)
                data = baseContaminantes(informacion[0], value, contaminant)
                if data.empty:
                    data = dataBackup
                    data = data.fillna(value=-1)
                    data = filterData(data, dirData + value + "_" + contaminant + ".csv")
                    data = data.fillna(value=-1)
                    valPred = prediccion(value, data, dirData, dirTrain, contaminant)
                    print("Informacion insuficiente para la prediccion")
                    guardarPrediccion(value, informacion[0], [-1],contaminant)
                else:
                    data = separateDate(data)
                    data = unionData(data, informacion[0], dirFestivos)
                    data = df.concat([data, dataMet], axis=1)
                    data = filterData(data, dirData + value + "_" + contaminant + ".csv")
                    data = data.fillna(value=-1)
                    data = data.loc[0:0]
                    print(data)
                    valPred = prediccion(value, data, dirData, dirTrain, contaminant)
                    print(valPred)
                    guardarPrediccion(value, informacion[0], valPred, contaminant)
    # for x in estaciones:
        # training(informacion[1],x,dirTrain,dirData, dirFestivos, variables, contaminant);


def prediccion(estacion, data, dirData, dirTrain, contaminant):
    """
    function that sends the data to the neural network for the prediction of the pollutant

    :param estacion: name the station
    :type estacion: String
    :param data: information for the prediction
    :type data : list float32
    :param dirData: address of the files with training information
    :type dirData: String
    :param dirTrain: address of the training files of the neural network
    :type dirTrain: String
    :return: prdiction values
    :type return : float32
    """
    temp = data.ix[0].values
    temp = temp[1:]
    dataPred = pre.normalize(temp, estacion, contaminant, dirData)
    dataPred = convert(dataPred)
    prediccion = pre.prediction(estacion, contaminant, [dataPred], dirTrain, dirData)
    print(prediccion)
    prediccion1 = pre.desNorm(prediccion, estacion, contaminant, dirData)
    return prediccion1


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


def baseContaminantes(fecha, estacion, contaminant):
    """
    function to bring the information of the contaminants from the database

    :param fecha: date to bring the information
    :type fecha: date
    :param estacion:name of the station from which the information is extracted
    :type estacion: String
    :return: array with pollutant information
    :type return: array float32
    """
    fechaActual = str(fecha.year) + '-' + numString(fecha.month) + '-' + numString(fecha.day)+' '+numString(fecha.hour)+':00:00'
    data = fd.readData(fechaActual, fechaActual, [estacion], contaminant)
    return data


def training(fechaAyer, estacion, dirTrain, dirData, dirCsv, dirFestivos, variables, contaminant):
    """
    function to train the neural network with the information of 24 hours before

    :param fechaAyer: date of the previous day
    :type fechaAyer: date
    :param estacion: name the station
    :type estacion: String
    :param dirData: address of the files with training information
    :type dirData: String
    :param dirTrain: address of the training files of the neural network
    :type dirTrain: String
    :param dirFestivos: address of the file with the holidays
    :type dirFestivos: String
    :param dirCsv: Address of processed meteorology archives
    :type dirCsv : String
    :param variables: meteorological variables
    :type variables: string list
    """
    print(estacion)
    fecha = str(fechaAyer.year)+'/'+numString(fechaAyer.month)+'/'+numString(fechaAyer.day)+' '+numString(fechaAyer.hour)+':00:00';
    fechaMet = str(fechaAyer.year)+"-"+numString(fechaAyer.month)+"-"+numString(fechaAyer.day);
    fechaBuild = str(fechaAyer.year)+"/"+numString(fechaAyer.month)+"/"+numString(fechaAyer.day);
    data = fd.readData(fecha, fecha, [estacion], contaminant);
    build = fd.buildClass2(data, [estacion], contaminant, 24, fechaBuild, fechaBuild)
    if data.empty:
        print("No se puede hacer el entrenamiento")
    else:
        dataMet = unionMeteorologia(fechaMet, fechaAyer, dirCsv, variables)
        dataMet = dataMet.drop('fecha', axis=1)
        data = separateDate(data)
        data = unionData(data, fechaAyer, dirFestivos)
        data = df.concat([data, dataMet], axis=1)
        data = filterData(data, dirData + estacion + "_" + contaminant + ".csv")
        data = data.fillna(value=-1)
        xy_values = an(data, build, contaminant)  # preprocessing
        tr.training(xy_values[0], xy_values[1], estacion, dirTrain, contaminant, dirData)


def unionMeteorologia(fecha, fechaComplete, dirCsv, variables):
    """
    function to join the information of the pollutants with the metrological

    :param fecha: current date
    :type fecha: date
    :param fechaComplete: current date complete
    :type fechaComplete: date
    :param dirCsv: Address of processed meteorology archives
    :type dirCsv: string
    :param variables: meteorological variables
    :type variables: string list
    """
    data = df.read_csv(dirCsv + "U10_" + fecha + ".csv")
    for i in variables:
        name = i + "_" + fecha + ".csv"
        dataTemp = df.read_csv(dirCsv + name)
        data = data.merge(dataTemp, how='left', on='fecha')
    fechaM = str(fechaComplete.year) + '-' + numString(fechaComplete.month) + '-'+numString(fechaComplete.day)+' '+numString(fechaComplete.hour)+':00:00';
    filterData = data[(data['fecha'] == fechaM)]
    filterData = filterData.reset_index(drop=True)
    return filterData


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


def unionData(data, fechaComplete, dirFestivos):
    """
    Function to join the data of the netcdf and the data of the pollutants

    :param data: DataFrame pollutants data
    :type data: dataFrame
    :return: dataFrame
    """
    fechaM = str(fechaComplete.year) + '-' + numString(fechaComplete.month) + '-'+numString(fechaComplete.day)+' '+numString(fechaComplete.hour)+':00:00';
    dataFestivos = df.read_csv(dirFestivos)
    dataFestivos = dataFestivos.drop(labels='Unnamed: 0', axis=1)
    dataFestivos2 = convertDates(dataFestivos)
    dataFestivos2 = dataFestivos2[(dataFestivos2['fecha'] == fechaM)]
    dataFestivos2 = dataFestivos2.reset_index(drop=True)
    dataFestivos2 = dataFestivos2.drop('fecha', axis=1)
    data = df.concat([data, dataFestivos2], axis=1)
    return data


def guardarPrediccion(estacion, fecha, Valor,contaminant):
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
    fecha = fecha + timedelta(days=1)
    fechaActual = str(fecha.year) + '-' + str(fecha.month) + '-' + str(fecha.day)+' '+str(fecha.hour)+':00:00'
    fd.saveData(estacion, fechaActual, Valor, findT(contaminant))


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


def back(dirData, contaminant):
    temp = df.read_csv(dirData + "MGH_" + contaminant + ".csv")
    return temp.loc[:0]


def numString(num):
    """
    function to convert a number of a digit into a string with two digits

    :param num:number to convert
    :type num: string
    :return : string with two digits
    :type return: String
    """
    if num < 10:
        return "0" + str(num)
    else:
        return str(num)


def deMonth(m):
    """
    function to convert a number in the assigned month

    :param m: number of months
    :type m : int
    :return : name of the month
    :type return: String
    """
    if m == 1:
        return "enero"
    elif m == 2:
        return "febrero"
    elif m == 3:
        return "marzo"
    elif m == 4:
        return "abril"
    elif m == 5:
        return "mayo"
    elif m == 6:
        return "junio"
    elif m == 7:
        return "julio"
    elif m == 8:
        return "agosto"
    elif m == 9:
        return "septiembre"
    elif m == 10:
        return "octubre"
    elif m == 11:
        return "noviembre"
    elif m == 12:
        return "diciembre"


def separateDate(data):
    """
    Function to separate the date in year, month ,day and the function sine of each one of them

    :parama data: DataFrame that contains the dates
    :type data: DataFrame
    """
    dates = data['fecha']
    lenght = len(dates.index)
    years = np.ones((lenght, 1)) * -1
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
        # sinYears[i]= np.sin(d.year);
        months[i] = d.month
        sinMonths[i] = (1 + np.sin(((d.month - 1) / 11) * (2 * np.pi))) * 0.5
        days[i] = d.day
        sinDays[i] = (1 + np.sin(((d.day - 1) / 23) * (2 * np.pi))) * 0.5
        i += 1
    weekD = df.DataFrame(wDay, columns=['weekday'])
    data['weekday'] = weekD
    sinWeekD = df.DataFrame(sinWday, columns=['sinWeekday'])
    data['sinWeekday'] = sinWeekD
    dataYear = df.DataFrame(years, columns=['year'])
    data['year'] = dataYear
    # dataSinYear = df.DataFrame(sinYears, columns= ['sinYear'])print(data);
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
    :type day:int
    :return: int, 1 is Sunday
    """
    a = (14 - month) / 12
    a = int(a)
    y = year - a
    m = month + 12 * a - 2
    week = (day + y + int(y / 4) - int(y / 100) + int(y / 400) + int((31 * m) / 12)) % 7;
    week = week + 1
    sinWeek = (1 + np.sin(((week - 1) / 7) * (2 * np.pi))) * 0.5
    return [week, sinWeek]

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
    config = configparser.ConfigParser()
    config.read('/ServerScript/AirQualityModel/ContaminationForecast/modulos/forecast/confAutomatic_System.conf')
    dirNetCDF = config.get('automatic_System', 'dirNetCDF')
    dirCsv = config.get('automatic_System', 'dirCsv')
    dirData = config.get('automatic_System', 'dirData')
    dirTrain = config.get('automatic_System', 'dirTrain')
    dirFestivos = config.get('automatic_System', 'dirFestivos')
    variables = config.get('automatic_System', 'variables')
    pathCopyData = config.get('automatic_System', 'pathCopyData')
    path = config.get('automatic_System', 'path')
    contaminant = config.get('automatic_System', 'contaminant')
    numRow = int(config.get('automatic_System', 'numRows'))
    numColumns = int(config.get('automatic_System', 'numColumns'))
    minlat = float(config.get('automatic_System', 'minlat'))
    maxlat = float(config.get('automatic_System', 'maxlat'))
    minlon = float(config.get('automatic_System', 'minlon'))
    maxlon = float(config.get('automatic_System', 'maxlon'))
    variables = config.get('automatic_System', 'variables')
    variables = variables.split()
    dataBackup = df.DataFrame
    information = configuracion(variables)
    contaminant = contaminant.split()
    print(contaminant)
    #for i in range(1, 24):
        #nameNetcdf = "wrfout_d02_"
        #hoy= datetime.strptime("2018-01-23 " + str(i) + ":00:00",'%Y-%m-%d %H:%M:%S')
        #dayer = datetime.strptime("2018-01-23 " + str(i) + ":00:00",'%Y-%m-%d %H:%M:%S')
        #actualNetcdf = nameNetcdf+ str(hoy.year)+ "-"+ str(hoy.month)+ "-"+str(hoy.day)+"_00.nc";
        #actualCsv = variables[0]+"_"+str(hoy.year)+ "-"+ str(hoy.month)+ "-"+str(hoy.day)+".csv";
        #ayerCsv = variables[0]+"_"+str(dayer.year)+ "-"+ str(dayer.month)+ "-"+str(dayer.day)+".csv";
        #test =[hoy,dayer,actualNetcdf,actualCsv,ayerCsv]
        #information = test
    for xs in contaminant:
        estaciones = config.get('automatic_System', 'estaciones'+xs)
        estaciones = estaciones.split()
        leerArchivo(information, estaciones, variables, dirNetCDF, dirCsv, dirData + 'B' +xs + '/', dirTrain + xs + '/', dirFestivos, dataBackup,path,pathCopyData, xs,numRow, numColumns, minlat, maxlat, minlon, maxlon)
    #leerArchivo(information, estaciones, variables, dirNetCDF, dirCsv, dirData, dirTrain, dirFestivos, dataBackup,path,pathCopyData, contaminant,numRow, numColumns, minlat, maxlat, minlon, maxlon)


init()

