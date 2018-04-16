'''
File name : automatic_System.py
Author: Pablo Camacho Gonzalez
Python version: 3.6.4
Date last modified: 28/02/2018
'''


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
            option = update4hours(value, contaminant, informacion[0], dirData, dirTrain, dirCsv,dirFestivos, variables, fecha)
            #option = 0
            if option == 0:
                data = baseContaminantes(informacion[0], value, contaminant)
                if data.empty:
                    data = dataBackup
                    data = data.fillna(value=-1)
                    data = filterData(data, dirData + value + "_" + contaminant + ".csv")
                    data = data.fillna(value=-1)
                    valPred = prediccion(value, data, dirData, dirTrain, contaminant)
                    print("Informacion insuficiente para la prediccion")
                    #guardarPrediccion(value, informacion[0], [-1], contaminant)
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
            else:
                print('update 4 hours')
    elif buscarArchivo(informacion[2], dirNetCDF):  # NetCDF
        direccioNetCDF = dirNetCDF +'0' +str(informacion[0].month) + "_" + deMonth(informacion[0].month) + "/"
        data = open_netcdf(direccioNetCDF + informacion[2], informacion[2], informacion[2], pathCopyData);
        fecha = str(informacion[0].year) + "-" + numString(informacion[0].month)+"-"+numString(informacion[0].day)
        checkFile(data, informacion[2], fecha, 2, path, numRow, numColumns, minlat, maxlat, minlon, maxlon, variables)
        dataMet = unionMeteorologia(fecha, informacion[0], dirCsv, variables)
        dataMet = dataMet.drop('fecha', axis=1)
        for value in estaciones:
            option = update4hours(value, contaminant, informacion[0], dirData, dirTrain, dirCsv,dirFestivos, variables, fecha)
            #option = 0
            if option == 0:
                data = baseContaminantes(informacion[0], value, contaminant)
                if data.empty:
                    data = dataBackup
                    data = data.fillna(value=-1)
                    data = filterData(data, dirData + value + "_" + contaminant + ".csv")
                    data = data.fillna(value=-1)
                    valPred = prediccion(value, data, dirData, dirTrain, contaminant)
                    print("Informacion insuficiente para la prediccion")
                    #guardarPrediccion(value, informacion[0], [-1], contaminant)
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
                print('update  4 hours')
    else:
        if buscarArchivo(informacion[4], dirCsv):
            # buscarArchivo(informacion[4]); #csv ayer
            fechaAyer = str(informacion[1].year) + "-" + numString(informacion[1].month)+"-"+numString(informacion[1].day)
            dataMet = unionMeteorologia(fechaAyer, informacion[1], dirCsv, variables)
            dataMet = dataMet.drop('fecha', axis=1)
            for value in estaciones:
                print(value)
                option =update4hours(value, contaminant, informacion[0], dirData, dirTrain, dirCsv, dirFestivos, variables, fechaAyer)
                #option = 0
                if option == 0:
                    data = baseContaminantes(informacion[0], value, contaminant)
                    if data.empty:
                        data = dataBackup
                        data = data.fillna(value=-1)
                        data = filterData(data, dirData + value + "_" + contaminant + ".csv")
                        data = data.fillna(value=-1)
                        valPred = prediccion(value, data, dirData, dirTrain, contaminant)
                        print("Informacion insuficiente para la prediccion")
                        #guardarPrediccion(value, informacion[0], [-1], contaminant);
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
                    print('update 4 hours')
        else:
            anteAyer = informacion[1] - timedelta(days=1)
            nameCsv = variables[0]+"_"+str(anteAyer.year)+ "-"+ numString(anteAyer.month)+ "-"+numString(anteAyer.day)+".csv";
            fechaAnteAyer = str(anteAyer.year) + "-" + numString(anteAyer.month)+"-"+numString(anteAyer.day)
            dataMet = unionMeteorologia(fechaAnteAyer, anteAyer, dirCsv, variables)
            dataMet = dataMet.drop('fecha', axis=1)
            for value in estaciones:
                print(value)
                option = update4hours(value, contaminant, informacion[0], dirData, dirTrain, dirCsv,dirFestivos, variables, fechaAnteAyer)
                #option = 0
                if option == 0:
                    data = baseContaminantes(informacion[0], value, contaminant)
                    if data.empty:
                        data = dataBackup
                        data = data.fillna(value=-1)
                        data = filterData(data, dirData + value + "_" + contaminant + ".csv")
                        data = data.fillna(value=-1)
                        valPred = prediccion(value, data, dirData, dirTrain, contaminant)
                        print("Informacion insuficiente para la prediccion")
                        #guardarPrediccion(value, informacion[0], [-1],contaminant)
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
                    print('update 4 hours')
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
    columnContaminant = findTable2(contaminant)
    prediccion1 = pre.desNorm(prediccion, estacion, contaminant, dirData, columnContaminant + '_')
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
        fechaComplete = fechaComplete + timedelta(days=1)
        fechaM = str(fechaComplete.year) + '-' + numString(fechaComplete.month) + '-'+numString(fechaComplete.day)+' '+numString(fechaComplete.hour)+':00:00';
        filterData = data[(data['fecha'] == fechaM)]
        if filterData.empty:
            fechaComplete = fechaComplete - timedelta(days=1)
            fechaM = str(fechaComplete.year) + '-' + numString(fechaComplete.month) + '-'+numString(fechaComplete.day)+' '+numString(fechaComplete.hour)+':00:00';
            filterData = data[(data['fecha'] == fechaM)]
        filterData = filterData.reset_index(drop = True)
    return filterData


def unionTotalMeteorologia(fecha, dirCsv, variables, fechaInicio, fechaFinal):
    fechaInicio = datetime.strptime(fechaInicio, '%Y-%m-%d %H:%M:%S')
    fechaFinal = datetime.strptime(fechaFinal, '%Y-%m-%d %H:%M:%S')
    #fechaInicio = fechaInicio + timedelta(days=1)
    #fechaFinal = fechaFinal + timedelta(days=1)
    fechaInicio= str(fechaInicio.year) + '-' + numString(fechaInicio.month) + '-' + numString(fechaInicio.day)+' '+numString(fechaInicio.hour)+':00:00'
    fechaFinal= str(fechaFinal.year) + '-' + numString(fechaFinal.month) + '-' + numString(fechaFinal.day)+' '+numString(fechaFinal.hour)+':00:00'
    data = df.read_csv(dirCsv + "U10_" + fecha + ".csv")
    #variables.pop(0)
    for i in variables:
        name = i + "_" + fecha + ".csv"
        dataTemp = df.read_csv(dirCsv + name)
        data = data.merge(dataTemp, how='left', on='fecha')
        data = data[(data['fecha']>= fechaInicio) & (data['fecha']<= fechaFinal)]
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


def totalUnionData(data,dirFestivos):
    dataFestivos = df.read_csv(dirFestivos)
    dataFestivos = dataFestivos.drop(labels='Unnamed: 0', axis=1)
    dataFestivos2 = convertDates(dataFestivos)
    totalData = data.merge(dataFestivos2, how='left', on='fecha')
    return totalData


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
    if estacion == 'SFE':
        fecha = fecha + timedelta(days = 1)
        fecha1 = fecha + timedelta(hours = 6)
        fechaActual = str(fecha1.year) + '-' + str(fecha1.month) + '-' + str(fecha1.day+1)+' '+str(fecha1.hour)+':00:00'
        rept = fd.rev_data(estacion,fechaActual,findT(contaminant))
        if rept == 0:
            fd.saveData(estacion, fechaActual, Valor, findT(contaminant))
        else:
            print('valor repetido')
    elif estacion == 'NEZ':
        fecha = fecha + timedelta(days=1)
        fecha = fecha + timedelta(hours = 11)
        fechaActual = str(fecha.year) + '-' + str(fecha.month) + '-' + str(fecha.day+1)+' '+str(fecha.hour)+':00:00'
        rept = fd.rev_data(estacion,fechaActual,findT(contaminant))
        if rept == 0:
            fd.saveData(estacion, fechaActual, Valor, findT(contaminant))
        else:
            print('valor repetido')
    elif estacion == 'TAH':
        fecha = fecha + timedelta(days=1)
        fecha = fecha + timedelta(hours=15)
        fechaActual = str(fecha.year) + '-' + str(fecha.month) + '-' + str(fecha.day+1)+' '+str(fecha.hour)+':00:00'
        rept = fd.rev_data(estacion,fechaActual,findT(contaminant))
        if rept == 0:
            fd.saveData(estacion, fechaActual, Valor, findT(contaminant))
        else:
            print('valor repetido')
    elif estacion == 'UAX':
        fecha = fecha + timedelta(days=1)
        fecha = fecha + timedelta(hours=13)
        fechaActual = str(fecha.year) + '-' + str(fecha.month) + '-' + str(fecha.day+1)+' '+str(fecha.hour)+':00:00'
        rept = fd.rev_data(estacion,fechaActual,findT(contaminant))
        if rept == 0:
            fd.saveData(estacion, fechaActual, Valor, findT(contaminant))
        else:
            print('valor repetido')
    else:
        fecha = fecha + timedelta(days=1)
        fechaActual = str(fecha.year) + '-' + str(fecha.month) + '-' + str(fecha.day+1)+' '+str(fecha.hour)+':00:00'
        rept = fd.rev_data(estacion,fechaActual,findT(contaminant))
        if rept == 0:
            fd.saveData(estacion, fechaActual, Valor, findT(contaminant))
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


def back(dirData, contaminant):
    if contaminant == 'PM10':
        temp = df.read_csv(dirData + 'TAH_' + contaminant + '.csv')
    else:
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
    if num == 0:
        return "00"
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
    data = df.concat([data,weekD], axis=1)
    #data['weekday'] = weekD
    sinWeekD = df.DataFrame(sinWday, columns=['sinWeekday'])
    data = df.concat([data,sinWeekD], axis=1)
    #data['sinWeekday'] = sinWeekD
    dataYear = df.DataFrame(years, columns=['year'])
    data = df.concat([data,dataYear], axis=1)
    #data['year'] = dataYear
    # dataSinYear = df.DataFrame(sinYears, columns= ['sinYear'])print(data);
    # data['sinYear'] = dataSinYear
    dataMonths = df.DataFrame(months, columns=['month'])
    data = df.concat([data,dataMonths], axis=1)
    #data['month'] = dataMonths
    dataSinMonths = df.DataFrame(sinMonths, columns=['sinMonth'])
    data = df.concat([data,dataSinMonths], axis=1)
    #data['sinMonth'] = dataSinMonths
    dataDay = df.DataFrame(days, columns=['day'])
    data = df.concat([data,dataDay], axis=1)
    #data['day'] = dataDay
    dataSinDay = df.DataFrame(sinDays, columns=['sinDay'])
    data = df.concat([data,dataSinDay], axis=1)
    #data['sinDay'] = dataSinDay
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


def update4hours(estacion, contaminant, fecha, dirData, dirTrain, dirCsv,dirFestivos, variables, fechaString):
    """
    function to make the last 4 hours of forecast

    :param estacion: name of the weather station
    :type estacion: String
    :param contaminant: name of the pollutant
    :type contaminant: String
    :param fecha: current day
    :type fecha: datetime
    :param dirData: address of the files with training information
    :type dirData: String
    :param dirTrain: address of the training files of the neural network
    :type dirTrain: String
    :param dirCsv: Address of processed meteorology archives
    :type dirCsv : String
    :param dirFestivos: address of the file with the holidays
    :type dirFestivos: String
    :param variables: meteorological variables
    :type variables: list(Strings)
    """
    fechaB = fecha
    fecha = fecha + timedelta(days=1)
    fecha2 = fecha - timedelta(hours = 2)
    fechaInicio = fecha - timedelta(hours= 5)
    fechaActual = str(fechaB.year) + '-' + numString(fechaB.month) + '-' + numString(fechaB.day)+' '+numString(fechaB.hour)+':00:00'
    fechai = str(fechaInicio.year) + '-' + numString(fechaInicio.month) + '-' + numString(fechaInicio.day)+' '+numString(fechaInicio.hour)+':00:00'
    nameC = findT(contaminant)
    dataForecast= fd.get_forecast(nameC,estacion)
    print(dataForecast)
    if dataForecast.empty:
        print('NO hay datos para la prediccion')
        return 0
    else:
        fechaUltima = dataForecast['fecha'][0]
        if estacion == 'SFE':
            fechaUltima = fechaUltima -timedelta(hours=6)
        elif estacion == 'TAH':
            fechaUltima = fechaUltima - timedelta(hours=15)
        elif estacion == 'UAX':
            fechaUltima = fechaUltima - timedelta(hours=13)
        elif estacion == 'NEZ':
            fechaUltima = fechaUltima - timedelta(hours=11)
    fechaUltima = fechaUltima + timedelta(seconds=40)
    if fechaUltima < fecha2:
        print('retrasado')
        fechaUltima = fechaUltima -  timedelta(days=1)
        fechaInicio= str(fechaUltima.year) + '-' + numString(fechaUltima.month) + '-' + numString(fechaUltima.day)+' '+numString(fechaUltima.hour)+':00:00'
        fechaFin = fecha2 - timedelta(days=1)
        fechafin_str = str(fechaFin.year) + '-' + numString(fechaFin.month) + '-' + numString(fechaFin.day)+' '+numString(fechaFin.hour)+':00:00'
        data = fd.readData(fechaInicio,fechaActual,[estacion],contaminant)
        data = data.drop_duplicates(keep='first')
        dataMet = unionTotalMeteorologia(fechaString, dirCsv, variables,fechaInicio, fechaActual)
        if data.empty and (fechaFin - fechaUltima) >  timedelta(hours=4):
            print('climatologia')
            useClimatology(contaminant, estacion, fechaUltima, fechaFin, dataMet,dirData,dirTrain, dirFestivos)
            #dataCorrelacion(contaminant, estacion, fechaUltima, fechaFin, dataMet,dirData,dirTrain, dirFestivos)
            return 1
        elif data.empty and (fechaFin - fechaUltima) <=  timedelta(hours=4):
            print('Climatologia cada 4 hrs.')
            return 0
        elif data.empty:
            print('No hay datos para la prediccion')
            return 0
            #useClimatology(contaminant, estacion, fechaUltima, fechaFin, dataMet, dirData, dirTrain)
        else:
            data = data.reset_index(drop=True)
            data = separateDate(data)
            data = totalUnionData(data, dirFestivos)
            data = df.concat([data, dataMet], axis=1, join='inner')
            #data =  data.merge(dataMet, how='left', on='fecha')
            data = filterData(data, dirData + estacion + "_" + contaminant + ".csv")
            data = data.fillna(value=-1)
            index = data.index.values
            arrayPred = []
            for x in index:
                pred = data.ix[x].values
                valPred = pred[2:]
                valNorm = pre.normalize(valPred, estacion, contaminant, dirData)
                arrayPred.append(convert(valNorm))
            result = pre.prediction(estacion, contaminant, arrayPred, dirTrain, dirData)
            columnContaminant = findTable2(contaminant)
            real = pre.desNorm(result, estacion, contaminant, dirData, columnContaminant+ '_')
            for xs in range(len(real)):
                fechaPronostico = data['fecha'].iloc[xs].values
                fechaPronostico = datetime.strptime(fechaPronostico[1], '%Y-%m-%d %H:%M:%S')
                fechaPronostico = fechaPronostico - timedelta(days=1)
                pronostico = real[xs]
                guardarPrediccion(estacion, fechaPronostico, [pronostico],contaminant)
            return 1
    else:
        print('corriente')
        return 0


def useClimatology(contaminant, estacion, fechaInicio, fechaFinal, dataMet,dirData,dirTrain,dirFestivos):
    """
    function to make the forecast using climatologies

    :param contaminant: name of the pollutant
    :type contaminant: String
    :param estacion: name of the weather station
    :type estacion: String
    :param fechaInicio: range of data wit wich the vaues of tue query are extracted
    :type fechaInicio: datetime
    :param fechaFinal: range of data wit wich the vaues of tue query are extracted
    :type fechaFinal: datetime
    :param dataMet: dataframe with the climatological information
    :type dataMet: DataFrame
    """
    data = fd.get_climatology(fechaInicio, fechaFinal, estacion)
    data = makeDates(fechaInicio,fechaFinal,data)
    #sys.out
    data = data.reset_index(drop=True)
    data = separateDate(data)
    data = totalUnionData(data, dirFestivos)
    data = df.concat([data, dataMet], axis=1, join='inner')
    #data = data.merge(dataMet, how='left', on='fecha')
    data = data.fillna(value=-1)
    data = filterData(data, dirData + estacion + "_" + contaminant + ".csv")
    data = data.fillna(value=-1)
    index = data.index.values
    arrayPred = []
    for x in index:
        pred = data.ix[x].values
        valPred = pred[2:]
        valNorm = pre.normalize(valPred, estacion, contaminant, dirData)
        arrayPred.append(convert(valNorm))
    result = pre.prediction(estacion, contaminant, arrayPred, dirTrain, dirData)
    columnContaminant = findTable2(contaminant)
    real = pre.desNorm(result, estacion, contaminant, dirData, columnContaminant+ '_')
    fechaPronostico = fechaInicio
    for xs in real:
        guardarPrediccion(estacion, fechaPronostico, [xs], contaminant)
        fechaPronostico = fechaPronostico + timedelta(hours=1)
    print('Climatologia:' + estacion)


def dataCorrelacion(contaminant, estacion, fechaInicio, fechaFin, dataMet,dirData,dirTrain, dirFestivos):
    print('COrrelacion')
    data_Corr = df.read_csv('/ServerScript/AirQualityModel/ContaminationForecast/Data/Correlacion_table.csv', index_col=0)
    corr_est = data_Corr[estacion].sort_values(ascending=False)
    estacion_corr = corr_est.index[1]
    data = fd.readData_corr(fechaInicio, fechaFin, [estacion_corr], contaminant)
    if data.empty:
        useClimatology(contaminant, estacion, fechaUltima, fechaFin, dataMet,dirData,dirTrain, dirFestivos)
    else:
        data = data.drop_duplicates(keep='first')
        data = data.reset_index(drop=True)
        index_values = data.columns.values[1:]
        for xs in index_values:
            data.rename(columns={xs:xs.replace(estacion_corr.lower(), estacion.lower())}, inplace = True)
        data = separateDate(data)
        data = totalUnionData(data, dirFestivos)
        data = df.concat([data, dataMet], axis=1, join='inner')
        print(data)
        #data =  data.merge(dataMet, how='left', on='fecha')
        data = filterData(data, dirData + estacion + "_" + contaminant + ".csv")
        data = data.fillna(value=-1)
        index = data.index.values
        arrayPred = []
        for x in index:
            pred = data.ix[x].values
            valPred = pred[2:]
            print(valPred)
            valNorm = pre.normalize(valPred, estacion, contaminant, dirData)
            arrayPred.append(convert(valNorm))
        result = pre.prediction(estacion, contaminant, arrayPred, dirTrain, dirData)
        columnContaminant = findTable2(contaminant)
        real = pre.desNorm(result, estacion, contaminant, dirData, columnContaminant+ '_')
        for xs in range(len(real)):
            fechaPronostico = data['fecha'].iloc[xs].values
            fechaPronostico = datetime.strptime(fechaPronostico[1], '%Y-%m-%d %H:%M:%S')
            pronostico = real[xs]
            guardarPrediccion(estacion, fechaPronostico, [pronostico],contaminant)


def makeDates(fechaInicio, fechaFinal, data):
    dates=[]
    dates.append(fechaInicio)
    while fechaInicio <= fechaFinal:
        fechaInicio = fechaInicio + timedelta(hours=1)
        dates.append(fechaInicio)
    frameDates = df.DataFrame(dates, columns=['fecha'])
    data = data.drop('hora', axis=1)
    frameDates = df.concat([frameDates, data], axis=1)
    return frameDates


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



def init():
    contaminant = str(sys.argv[1])
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
    #contaminant = config.get('automatic_System', 'contaminant')
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
    #for i in range(23, 24):
        #nameNetcdf = "wrfout_d02_"
        #hoy= datetime.strptime("2018-02-20 " + str(i) + ":00:00",'%Y-%m-%d %H:%M:%S')
        #dayer = datetime.strptime("2018-02-19 " + str(i) + ":00:00",'%Y-%m-%d %H:%M:%S')
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
