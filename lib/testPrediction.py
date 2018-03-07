'''
File name : testPrediction.py
Author: Pablo Camacho Gonzalez
Python version: 3.6.4
Date last modified: 27/02/2018
'''


from datetime import datetime, timedelta
import prediction as pre
from Utilites.metricas import metricas
import pandas as df
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from time import time


loss_vec = []
metri = []


def totalPredection(est, dirData, dirrDataC, dirGraficas, dirTrain, contaminant,columnContaminant, fechaInicio, fechaFin):
    """
    function to send to do the forecast of a station and graph it

    :param station: name the station
    :type station: String
    :param dirData: address of the files with training information
    :type dirData: String
    :param dirGraficas: address where the graphics are saved
    :type dirGraficas: String
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
        trial(x, dirData, dirrDataC, dirGraficas, dirTrain, contaminant, columnContaminant, fechaInicio, fechaFin)


def trial(station, dirData, dirrDataC, dirGraficas, dirTrain, contaminant, columnContaminant, fechaInicio, fechaFin):
    """
    function to make the forecast of a whole year and graph it

    :param station: name the station
    :type station: String
    :param dirData: address of the files with training information
    :type dirData: String
    :param dirGraficas: address where the graphics are saved
    :type dirGraficas: String
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
    tempBuild = df.read_csv(dirrDataC + name + '_pred.csv')  # we load the data in the Variable build
    tempBuild = tempBuild.fillna(value=-1.0)
    build = tempBuild[(tempBuild['fecha'] <= fechaFin) & (tempBuild['fecha'] >= fechaInicio)];
    build = build.reset_index(drop=True)
    build = build.fillna(value=-1.0)
    l = xlabel(data)
    labels = l[0]
    location = l[1]
    print(labels)
    if (station == 'SAG') | (station == 'UIZ'):
        #loc = labels.index('Marzo')
        #lugar = location[loc] + 1
        #nombre = labels[loc]
        nombre = 'anio'
    else:
        print('no mes')
        #loc = labels.index('Marzo')
        #lugar = location[loc] + 1
        #nombre = labels[loc]
        nombre = 'anio'
    arrayPred = []
    nameColumn = columnContaminant +'_'+ sta + '_delta'
    inf = build[nameColumn].values
    index = data.index.values
    for x in index:
        pred = data.ix[x].values
        valPred = pred[1:]
        valNorm = pre.normalize(valPred, sta, contaminant, dirData)
        arrayPred.append(convert(valNorm))
    result = pre.prediction(sta, contaminant, arrayPred, dirTrain, dirData)
    real = desNorm(result, sta, contaminant, dirData, columnContaminant)
    #metri.append(metricas(inf, real, station))
    plt.figure(figsize=(22.2, 11.4))
    plt.plot(inf, color='tomato', linestyle="solid", marker='o', label='Valor observado.');
    plt.plot(real, color='darkgreen', linestyle='solid', marker='o', label='Pronóstico 24h NN.');
    plt.title(nombreEst(station) + ' (' + station + ') comparación de ' + contaminant+' observado vs red neuronal' + ' para la primer semana de ' + nombre + ' 2016' ,fontsize=25, y=1.1 )
    plt.xlabel('Fecha', fontsize=18)
    #n = 'Primera semana de '+nombre
    #plt.xlabel(n,fontsize=22);
    plt.ylabel('Partes por millon (PPM)', fontsize=22)
    plt.legend(loc='best')
    plt.grid(True, axis='both', alpha= 0.3, linestyle="--", which="both")
    # plt.xticks(location,labels,fontsize=8,rotation=80)
    plt.xticks(location,labels,fontsize=16,rotation=80)
    #plt.xlim(lugar,lugar+144);
    plt.axhspan(20, 40, color='lightgray', alpha=0.3)
    plt.axhspan(60, 80, color='lightgray', alpha=0.3)
    plt.axhspan(100, 120, color='lightgray', alpha=0.3)
    plt.gca().spines['bottom'].set_color('dimgray')
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(dirGraficas + station + '_' + nombre + '.png')
    plt.show();
    plt.clf();
    plt.close()
    #gError(inf, real, location, labels, station, dirGraficas)
    # graSubPlot(inf,real,station,location,dirGraficas,labels)


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


def gError(real, pred, location, labels, station, dirGraficas):
    """
    function to graph the forecast error

    :param real: observed value
    :type real: array float32
    :param pred: caculated values
    :type pred: array float32
    :param location: place where the labels will be placed on the axis of the graphics
    :type location: array int
    :param dirGraficas: address where the graphics are saved
    :type dirGraficas: String
    :param labels: graphics axis labels
    :type labels: array String
    """
    valError = []
    suma = 0
    tam = len(real)
    x = np.arange(tam)
    for i in range(tam):
        ve = abs(real[i] - pred[i])
        valError.append(ve)
    plt.figure(figsize=(22.2, 11.4))
    plt.plot(valError, color='maroon', linestyle='solid', label='Error')
    plt.fill_between(x, valError, 0, where=x >= 0, color='salmon')
    plt.title('Error en la prediccion de la estacion ' + nombreEst(station) + ' ('+station+')(2017)',fontsize=25,y=1.1);
    plt.xlabel('Fechas', fontsize=18)
    plt.ylabel('Error PPM', fontsize=18)
    # plt.legend(loc ='best');
    plt.xticks(location, labels, fontsize=16, rotation=80)
    plt.grid(True, axis='both', alpha=0.5, linestyle="--")
    plt.gca().spines['bottom'].set_color('lightgray')
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(dirGraficas + station + '_Error.png')
    plt.show()
    plt.clf()
    plt.close()


def graSubPlot(obs, calcu, station, location, dirGraficas, labels):
    """
    function to graph the forecast given by the neural network

    :param obs: observed value
    :type obs: array float32
    :param calcu: caculated values
    :type calcu: array float32
    :param station: name the station
    :type station: String
    :param location: place where the labels will be placed on the axis of the graphics
    :type location: array int
    :param dirGraficas: address where the graphics are saved
    :type dirGraficas: String
    :param labels: graphics axis labels
    :type labels: array String
    """
    plt.figure(figsize=(22.2, 11.4))
    plt.subplot(2, 1, 1)
    plt.plot(obs, 'g-', label='Valor observado.')
    plt.title(nombreEst(station) + ' (' + station + ') comparación de ' + contaminant+' observado vs red neuronal (2017)',fontsize=20);
    plt.ylabel('Partes por millon (PPM)', fontsize=11)
    plt.legend(loc='best')
    plt.xticks(location, labels, fontsize=11)
    plt.subplot(2, 1, 2)
    plt.plot(calcu, 'r--', label='Pronostico 24h NN.')
    plt.xlabel('Fecha', fontsize=15)
    plt.ylabel('Partes por millon (PPM)', fontsize=11)
    plt.legend(loc='best')
    plt.xticks(location, labels, fontsize=11)
    plt.savefig(dirGraficas + station + '_scatter.png')
    plt.grid(True)
    plt.show()
    plt.clf()
    plt.close()


def saveMetric(dirGraficas):
    """
    function to save the values obtained from the metrics

    :param dirGraficas: address where the graphics are saved
    :type dirGraficas: String
    """
    nameCol = ['MAPE', 'uTheils', 'Indice de Correlación', 'Agreement', 'RMSE']
    dataMet = df.DataFrame(metri, columns=['Estacion', 'MAPE', 'uTheils', 'Indice de Correlación','Agreement', 'RMSE']);
    dataMet.to_csv(dirGraficas + 'Metricas.csv', encoding='utf-8', index=False)
    print(dataMet)
    for value in nameCol:
        # dataMet.groupby('estacion').mean().loc[:,[value]].plot(kind='bar',figsize=(12.2,6.4),title=value);
        dataMet.groupby('Estacion').mean().loc[:, [value]].plot(kind='bar', figsize=(22.2,11.4),color='steelblue', fontsize=18);
        plt.title(value, size=25, y=1.1)
        plt.grid(True, axis='y', linestyle='--', alpha=0.4)
        plt.gca().spines['bottom'].set_color('lightgray')
        plt.gca().spines['left'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.legend(loc=1, bbox_to_anchor=(0.1, 1.09), frameon=None)
        plt.tight_layout()
        plt.savefig(dirGraficas + value + ".png", dpi=600)
        plt.show()
        plt.close()


def deMonth(m):
    """
    function to convert a number in the assigned month

    :param m: number of months
    :type m : int
    :return : name of the month
    :type return: String
    """
    if m == 1:
        return "Enero"
    elif m == 2:
        return "Febreo"
    elif m == 3:
        return "Marzo"
    elif m == 4:
        return "Abril"
    elif m == 5:
        return "Mayo"
    elif m == 6:
        return "Junio"
    elif m == 7:
        return "Julio"
    elif m == 8:
        return "Agosto"
    elif m == 9:
        return "Septiembre"
    elif m == 10:
        return "Octubre"
    elif m == 11:
        return "Novimebre"
    elif m == 12:
        return "Diciembre"


def xlabel(data):
    """
    function to take a date list for the axis of a graph

    :param data: dataframe with dates
    :type data: DataFrame
    """
    fechas = []
    location = []
    dates = data['fecha']
    i = 0
    one = datetime.strptime(dates[0], '%Y-%m-%d %H:%M:%S')
    m = one.month
    for x in dates:
        d = datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
        if d.hour == 0 and d.month == m:
            # f = str(d.year) +'/'+ deMonth(d.month)+'/'+str(d.day);
            f = deMonth(d.month)
            fechas.append(f)
            location.append(i)
            m += 1
        i += 1
    return [fechas, location]


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
    print(nameC)
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


def nombreEst(station):
    """
    function that returns from the full name of a station

    :param station: abbreviation of the name of the station
    :type station: String
    :return: full name of the station
    :type return: String
    """
    if station == 'AJM':
        return 'Ajusco Medio'
    elif station == 'MGH':
        return 'Miguel Hidalgo'
    elif station == 'CCA':
        return 'Centro de Ciencias de la Atmosfera'
    elif station == 'SFE':
        return 'Santa Fe'
    elif station == 'UAX':
        return 'UAM Xochimilco'
    elif station == 'CUA':
        return 'Cuajimalpa'
    elif station == 'NEZ':
        return 'Nezahualcóyotl'
    elif station == 'CAM':
        return 'Camarones'
    elif station == 'LPR':
        return 'La Presa'
    elif station == 'SJA':
        return 'San Juan Aragón'
    elif station == 'CHO':
        return 'Chalco'
    elif station == 'IZT':
        return 'Iztacalco'
    elif station == 'SAG':
        return 'San Agustín'
    elif station == 'TAH':
        return 'Tlahuac'
    elif station == 'ATI':
        return 'Atizapan'
    elif station == 'FAC':
        return 'FES Acatlán'
    elif station == 'UIZ':
        return 'UAM Iztapalapa'
    elif station == 'MER':
        return 'Merced'
    elif station == 'PED':
        return 'Pedregal'
    elif station == 'TLA':
        return 'tlalnepantla'
    elif station == 'BJU':
        return 'Benito Juárez'
    elif station == 'XAL':
        return 'Xalostoc'


def obtMax(station, contaminant, columnContaminant):
    """
    function to extract the maximum of a contaminant from a cvs file

    :param station: name the station
    :type station: String
    :param contaminant: name the pollutant
    :type contaminant: String
    :param columnContaminant: name of the pollutant in the DataFrame
    :type columnContaminant: String
    """
    nameC = columnContaminant + '_' + station.lower()
    name = station + '_' + contaminant
    values = df.read_csv(dirData + name + '_MaxMin.csv')
    index = values.columns[0]
    va = values[(values[index] == nameC)]
    maxx = va['MAX'].values[0]
    return maxx


def init(dirData, dirrDataC, dirGraficas, dirTrain, contaminant, columnContaminant, fechaInicio, fechaFin, est):
    totalPredection(est, dirData, dirrDataC, dirGraficas, dirTrain, contaminant,columnContaminant, fechaInicio, fechaFin)
    saveMetric(dirGraficas)
