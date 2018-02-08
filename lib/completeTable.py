import pandas as df
import shutil
import os
import configparser


def originDir(dirDataComp, dirDataSave, nameContaminant, est, contaminant, porcentaje):
    """
    function to send a list of function to apply bootstrap

    :param dirDataComp: file address
    :type dirDataComp : string
    :param dirDataSave: address where the files are saved
    :type dirDataSave: String
    :param nameContaminant: name of the pollutant in the database
    :type nameContaminant: String
    :param est: name the station
    :type est: String
    :param contaminant: name the pollutant
    :type contaminant: String
    """
    for x in range(len(dirDataComp)):
        bootstrap(dirDataComp[x], dirDataSave[x], nameContaminant, contaminant, est, porcentaje)


def unionData(origin, save, est, estComplete, contaminant):
    """
    Function to join the data of the netcdf and the data of the pollutants

    :param data: DataFrame pollutants data
    :type data: dataFrame
    :return: dataFrame
    """
    print(origin)
    for value in est:
        dirData = origin + value + '_' + contaminant + '.csv'
        data = df.read_csv(dirData)
        for xs in estComplete:
            print(xs)
            dirSave = save + value + '_' + contaminant + '.csv'
            dirComple = origin + xs + '_' + contaminant + '.csv'
            dataC = df.read_csv(dirComple)
            dataC = dataC.drop(['weekday', 'sinWeekday', 'year', 'month', 'sinMonth','day','sinDay','valLab'],axis=1);
            data = data.merge(dataC, how='left', on='fecha')
        data = data.fillna(value=-1)
        maxAndMinValues(data, value, contaminant, save)
        shutil.copy(origin + value + '_' + contaminant + '_pred.csv', save + value + '_'+ contaminant+'_pred.csv');
        data.to_csv(dirSave, encoding='utf-8', index=False)


def copyComplete(estComplete, dirDataComp, dirDataSave, contaminant):
    """
    function to copy files from one folder to another

    :param dirDataComp: file address
    :type dirDataComp : string
    :param dirDataSave: address where the files are saved
    :type dirDataSave: String
    :param contaminant: name the pollutant
    :type contaminant: String
    """
    for x in range(len(dirDataComp)):
        for value in estComplete:
            shutil.copy(dirDataComp[x] + value + '_' + contaminant + '_pred.csv', dirDataSave[x]+value + '_'+ contaminant+'_pred.csv');
            shutil.copy(dirDataComp[x] + value + '_' + contaminant + '.csv', dirDataSave[x]+value + '_'+ contaminant+'.csv');
            shutil.copy(dirDataComp[x] + value + '_' + contaminant + '_MaxMin.csv',dirDataSave[x]+value + '_'+ contaminant+'_MaxMin.csv');


def maxAndMinValues(data, station, contaminant, save):
    """
    Function to obtain the maximun and minumum values and save them in a file

    :param data: DataFrame that contains the data from where the maximun ans minumum values will be extracted
    :type data: DataFrame
    :param station: name the station
    :type station : string
    :param contaminant: name the contaminant
    :type contaminant : string
    """
    nameD = station + '_' + contaminant + '_MaxMin' + '.csv'
    Index = data.columns
    myIndex = Index.values
    myIndex = myIndex[1:]
    x_vals = data.values
    x = x_vals.shape
    columns = x[1]
    x_vals = x_vals[:, 1:columns]
    minx = x_vals.min(axis=0)
    maxx = x_vals.max(axis=0)
    mixmax = df.DataFrame(minx, columns=['MIN'], index=myIndex)
    dMax = df.DataFrame(maxx, columns=['MAX'], index=myIndex)
    mixmax['MAX'] = dMax
    mixmax.to_csv(save + nameD, encoding='utf-8')


def bootstrap(origin, save, nameContaminant, contaminant, est, porcentaje):
    """
    function to apply bootstrapt in a dataframe

    :param origin:
    :param save:
    :param nameContaminant: name of the pollutant in the database
    :type nameContaminant: String
    :param est: name the station
    :type est : string
    :param contaminant: name the contaminant
    :type contaminant : string
    """
    for value in est:
        print(origin + value)
        dirData = origin + value + '_' + contaminant + '.csv'
        dirPred = origin + value + '_' + contaminant + '_pred.csv'
        if os.path.exists(dirData):
            data = df.read_csv(dirData)
            pred = df.read_csv(dirPred)
            data = data.merge(pred, how='left', on='fecha')
            dataOzono = data[nameContaminant + value.lower()]
            mean = dataOzono.mean(axis=0)
            std = dataOzono.std(axis=0)
            dataBoot = data[data[nameContaminant + value.lower()] > (std*porcentaje)]
            d = df.concat([data, dataBoot], axis=0)
            prediccion = df.DataFrame(d['fecha'], columns=['fecha'])
            valPred = df.DataFrame(d[nameContaminant + value + '_delta'], columns=[nameContaminant +value+'_delta'])
            prediccion[nameContaminant + value + '_delta'] = valPred
            d = d.drop(nameContaminant + value + '_delta', axis=1)
            d = d.reset_index()
            d = d.drop('index', axis=1)
            prediccion = prediccion.reset_index()
            prediccion = prediccion.drop('index', axis=1)
            maxAndMinValues(d, value, contaminant, save)
            d.to_csv(save + value + '_' + contaminant + '.csv', encoding='utf-8', index=False)
            prediccion.to_csv(save + value + '_' + contaminant + '_pred.csv', encoding ='utf-8', index=False)


def createFile():
    est = ['AJM', 'MGH', 'CCA', 'SFE', 'UAX', 'CUA', 'NEZ', 'CAM', 'LPR', 'SJA', 'CHO', 'IZT', 'SAG', 'TAH','ATI','FAC','UIZ','MER','PED','TLA','BJU','XAL'];
    dirData = ['data/unionGeo/DatosCC/', 'data/unionGeo/DatosLC/', 'data/unionGeo/DatosCP/','data/unionGeo/DatosLP/'];
    dirGraficas = ['Graficas/Predicciones/unionGeo/GraficasCC/', 'Graficas/Predicciones/unionGeo/GraficasCP/','Graficas/Predicciones/unionGeo/GraficasLC/','Graficas/Predicciones/unionGeo/GraficasLP/'];
    dirTrain = ['trainData/unionGeo/TrainCP/', 'trainData/unionGeo/TrainLP/', 'trainData/unionGeo/TrainCC/','trainData/unionGeo/TrainLC/'];
    for val in range(len(dirData)):
        if not os.path.exists(dirData[val]):
            os.makedirs(dirData[val])
        if not os.path.exists(dirGraficas[val]):
            os.makedirs(dirGraficas[val])
        if not os.path.exists(dirTrain[val]):
            os.makedirs(dirTrain[val])
        for i in range(len(est)):
            r = dirTrain[val] + est[i]
            if not os.path.exists(r):
                os.makedirs(r)


def init():
    estComplete = []
    config = configparser.ConfigParser()
    config.read('confSaveData.conf')
    dirDataComp = config.get('completeTable', 'dirDataComp')
    dirDataSave = config.get('completeTable', 'dirDataSave')
    contaminant = config.get('completeTable', 'contaminant')
    nameContaminant = config.get('completeTable', 'nameContaminant')
    porcentaje = config.get('completeTable', 'porcentaje')
    est = config.get('completeTable','est')
    dirDataComp = dirDataComp.split()
    dirDataSave = dirDataSave.split()
    contaminant = contaminant.split()
    nameContaminant = nameContaminant.split()
    est = est.split()
    tam = len(contaminant) - 1
    for xs in range(tam):
        originDir([dirDataComp[xs]], [dirDataSave[xs]], nameContaminant[xs], est, contaminant[xs], porcentaje)
        #copyComplete(estComplete, dirDataComp, dirDataSave, contaminant)


#init()
