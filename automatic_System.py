from datetime import datetime, timedelta
from Utilites.FormatData import FormatData as fd
from Utilites.Utilites import prepro as an
import time
import sys, os
import pandas as df
import numpy as np
import prediction as pre
import autoTraining as tr
from NetCDF.makeCsv import open_netcdf, checkFile

dirNetCDF = '/DATA/WRF_Operativo/2017/' #direccion de los archivos NetCDF
#dirCsv = '/data/totalData/totalCuadrantes/';
dirCsv = '/home/pablo/DATA/DataCuadrantes/' #direccion de los archivos creados apartir de los NetCDF
dirData = '/home/pablo/PollutionForecast/ContaminationForecast/data/DatosLCB/'; #Direccion de datos de entrenamiento
dirTrain = '/home/pablo/PollutionForecast/ContaminationForecast/trainData/TrainLCB/'; #Direccion de entrenamiento de la red neuronal
estaciones = ['AJM', 'MGH', 'CCA', 'SFE', 'UAX', 'CUA', 'NEZ', 'CAM','LPR','SJA','IZT','SAG','TAH','ATI','FAC','UIZ','MER','PED','TLA','XAL','CHO','BJU'];
variables=['V10','RAINC','T2', 'TH2', 'RAINNC', 'PBLH', 'SWDOWN', 'GLW'];
dataBackup = df.DataFrame;


def configuracion():
    nameNetcdf = "wrfout_d02_"
    actual = datetime.now();
    actual = actual - timedelta(hours=1)
    actualNetcdf = nameNetcdf+ str(actual.year)+ "-"+ numString(actual.month)+ "-"+numString(actual.day)+"_00.nc";
    actualCsv = variables[0]+"_"+str(actual.year)+ "-"+ numString(actual.month)+ "-"+numString(actual.day)+".csv";
    ayer = actual - timedelta(days=1)
    ayerCsv = variables[0]+"_"+str(ayer.year)+ "-"+ numString(ayer.month)+ "-"+numString(ayer.day)+".csv";
    return [actual,ayer,actualNetcdf,actualCsv,ayerCsv];

def buscarArchivo(archivo, carpeta):
    for root, dir, ficheros in os.walk(carpeta,topdown=True):
        for i in ficheros:
            if archivo in i:
                return True;
    return False;


def leerArchivo(informacion):
    dataBackup = back()
    if buscarArchivo(informacion[3],dirCsv):
        fecha= str(informacion[0].year)+"-"+numString(informacion[0].month)+"-"+numString(informacion[0].day)
        dataMet = unionMeteorologia(fecha, informacion[0]);
        dataMet = dataMet.drop('fecha',axis =1)
        for value in estaciones:
            print(value);
            data = baseContaminantes(informacion[0],value);
            if data.empty:
                data = dataBackup
                data = data.fillna(value=-1)
                data = filterData(data,dirData+value+"_O3.csv");
                data = data.fillna(value=-1)
                valPred = prediccion(value, data)
                print("Informacion insuficiente para la prediccion");
                guardarPrediccion(value,informacion[0],[-1]);
            else:
                #data = data.merge(dataMet,how='left', on='fecha');
                data = separateDate(data)
                data = unionData(data,informacion[0])
                data = df.concat([data,dataMet], axis=1);
                data = data.fillna(value=-1)
                data = filterData(data,dirData+value+"_O3.csv");
                data = data.fillna(value=-1)
                print(data)
                valPred = prediccion(value, data);
                print(valPred);
                guardarPrediccion(value,informacion[0],valPred)
    elif buscarArchivo(informacion[2],dirNetCDF) : #NetCDF
        direccioNetCDF = dirNetCDF+ str(informacion[0].month) +"_"+  deMonth(informacion[0].month) + "/"
        #stringClear = makeCsv.clearString(informacion[2]);
        data = open_netcdf(direccioNetCDF+informacion[2],informacion[2],informacion[2]);
        #checkFile(data,informacion[2],fecha,2);
        fecha= str(informacion[0].year)+"-"+numString(informacion[0].month)+"-"+numString(informacion[0].day)
        checkFile(data,informacion[2],fecha,2);
        dataMet = unionMeteorologia(fecha, informacion[0]);
        dataMet = dataMet.drop('fecha',axis =1)
        for value in estaciones:
            data = baseContaminantes(informacion[0],value);
            if data.empty :
                data = dataBackup
                data = data.fillna(value=-1)
                data = filterData(data,dirData+value+"_O3.csv");
                data = data.fillna(value=-1)
                valPred = prediccion(value, data);
                print("Informacion insuficiente para la prediccion");
                guardarPrediccion(value,informacion[0],[-1]);
            else:
                data = separateDate(data)
                data = unionData(data,informacion[0])
                data = df.concat([data,dataMet], axis=1);
                data = data.fillna(value=-1)
                data = filterData(data,dirData+value+"_O3.csv");
                data = data.fillna(value=-1)
                print(data)
                valPred = prediccion(value, data);
                print(valPred);
                guardarPrediccion(value,informacion[0],valPred)
    else:
        if buscarArchivo(informacion[4], dirCsv):
            # buscarArchivo(informacion[4]); #csv ayer
            fechaAyer= str(informacion[1].year)+"-"+numString(informacion[1].month)+"-"+numString(informacion[1].day)
            dataMet = unionMeteorologia(fechaAyer, informacion[1]);
            dataMet = dataMet.drop('fecha',axis =1)
            for value in estaciones:
                print(value);
                data = baseContaminantes(informacion[0],value);
                if data.empty :
                    data = dataBackup
                    data = data.fillna(value=-1)
                    data = filterData(data,dirData+value+"_O3.csv");
                    data = data.fillna(value=-1)
                    valPred = prediccion(value, data);
                    print("Informacion insuficiente para la prediccion");
                    guardarPrediccion(value,informacion[0],[-1]);
                else:
                    data = separateDate(data)
                    data = unionData(data,informacion[0])
                    data = df.concat([data,dataMet], axis=1);
                    data = filterData(data,dirData+value+"_O3.csv");
                    data = data.fillna(value=-1)
                    print(data)
                    valPred  = prediccion(value, data);
                    print(valPred);
                    guardarPrediccion(value,informacion[0],valPred)
        else:
            anteAyer = informacion[1] - timedelta(days=1)
            nameCsv =   variables[0]+"_"+str(anteAyer.year)+ "-"+ numString(anteAyer.month)+ "-"+numString(anteAyer.day)+".csv";
            fechaAnteAyer= str(anteAyer.year)+"-"+numString(anteAyer.month)+"-"+numString(anteAyer.day)
            dataMet = unionMeteorologia(fechaAnteAyer, anteAyer)
            dataMet = dataMet.drop('fecha',axis =1)
            for value in estaciones:
                print(value);
                data = baseContaminantes(informacion[0],value);
                if data.empty :
                    data = dataBackup
                    data = data.fillna(value=-1)
                    data = filterData(data,dirData+value+"_O3.csv");
                    data = data.fillna(value=-1)
                    valPred = prediccion(value, data);
                    print("Informacion insuficiente para la prediccion");
                    guardarPrediccion(value,informacion[0],[-1]);
                else:
                    data = separateDate(data)
                    data = unionData(data,informacion[0])
                    data = df.concat([data,dataMet], axis=1);
                    data = filterData(data,dirData+value+"_O3.csv");
                    data = data.fillna(value=-1)
                    print(data)
                    valPred  = prediccion(value, data);
                    print(valPred);
                    guardarPrediccion(value,informacion[0],valPred)
    #for x in estaciones:
        #training(informacion[1],x,dirTrain,dirData);



def prediccion(estacion,data):
    temp = data.ix[0].values;
    temp = temp[1:];
    dataPred = pre.normalize(temp,estacion,"O3",dirData);
    dataPred= convert(dataPred);
    prediccion = pre.prediction(estacion,"O3",[dataPred],dirTrain,dirData)
    print(prediccion)
    prediccion1 = pre.desNorm(prediccion,estacion,"O3",dirData);
    return prediccion1;

def convert(data):
    size = len(data);
    vl = np.ones([1,size]);
    i = 0;
    for x in data:
        vl[0,i]= x
        i+=1;
    return vl


def baseContaminantes(fecha, estacion):
    fechaActual = str(fecha.year)+'-'+numString(fecha.month)+'-'+numString(fecha.day)+' '+numString(fecha.hour)+':00:00'
    data = fd.readData(fechaActual, fechaActual, [estacion], "O3")
    return data;


def training(fechaAyer, estacion, dirTrain, dirData):
    print(estacion);
    fecha = str(fechaAyer.year)+'/'+numString(fechaAyer.month)+'/'+numString(fechaAyer.day)+' '+numString(fechaAyer.hour)+':00:00';
    fechaMet = str(fechaAyer.year)+"-"+numString(fechaAyer.month)+"-"+numString(fechaAyer.day);
    fechaBuild = str(fechaAyer.year)+"/"+numString(fechaAyer.month)+"/"+numString(fechaAyer.day);
    data = fd.readData(fecha,fecha,[estacion],"O3");
    build = fd.buildClass2(data, [estacion], "O3", 24, fechaBuild, fechaBuild)
    if data.empty:
        print("No se puede hacer el entrenamiento")
    else:
        dataMet = unionMeteorologia(fechaMet, fechaAyer)
        dataMet = dataMet.drop('fecha',axis =1)
        data = separateDate(data)
        data = unionData(data,fechaAyer)
        data = df.concat([data,dataMet], axis=1);
        data = filterData(data, dirData + estacion + "_O3.csv")
        data = data.fillna(value=-1)
        xy_values = an(data, build, 'O3')  # preprocessing
        tr.training(xy_values[0], xy_values[1], estacion, dirTrain, 'O3', dirData)


def unionMeteorologia(fecha, fechaComplete):
    data = df.read_csv(dirCsv + "U10_" + fecha + ".csv")
    for i in variables:
        name = i + "_" + fecha + ".csv"
        dataTemp = df.read_csv(dirCsv + name)
        data= data.merge(dataTemp, how='left', on='fecha')
    fechaM = str(fechaComplete.year)+'-'+numString(fechaComplete.month)+'-'+numString(fechaComplete.day)+' '+numString(fechaComplete.hour)+':00:00';
    filterData = data[(data['fecha'] == fechaM)]
    filterData = filterData.reset_index(drop=True)
    return filterData


def convertDates(data):
    fecha = data['fecha'];
    data = data.drop(labels='fecha',axis=1);
    date = []
    for i in fecha:
        datef = datetime.strptime(i,'%Y-%m-%d %H:%M:%S');
        date.append(datef);
    dataTemp = df.DataFrame(date,columns = ['fecha']);
    data['fecha']= dataTemp;
    return data;


def unionData(data, fechaComplete):
    """
    Function to join the data of the netcdf and the data of the pollutants
    :param data:pataFrame(minollutants data
    :type data: dataFrame
    :return: dataFrame
    """
    fechaM = str(fechaComplete.year)+'-'+numString(fechaComplete.month)+'-'+numString(fechaComplete.day)+' '+numString(fechaComplete.hour)+':00:00';
    dataFestivos = df.read_csv('/home/pablo/PollutionForecast/ContaminationForecast/data/Festivos.csv')
    dataFestivos = dataFestivos.drop(labels='Unnamed: 0',axis=1);
    dataFestivos2 = convertDates(dataFestivos);
    dataFestivos2 = dataFestivos2[(dataFestivos2['fecha'] == fechaM)]
    dataFestivos2 = dataFestivos2.reset_index(drop=True)
    dataFestivos2 = dataFestivos2.drop('fecha',axis =1)
    data= df.concat([data,dataFestivos2], axis=1);
    return data;



def guardarPrediccion(estacion, fecha, Valor):
    fecha = fecha + timedelta(days=1)
    fechaActual = str(fecha.year)+'-'+str(fecha.month)+'-'+str(fecha.day)+' '+str(fecha.hour)+':00:00';
    fd.saveData(estacion, fechaActual, Valor)


def filterData(data, dirData):
    temp = df.read_csv(dirData)
    listColumns = list(temp.columns)
    data = data.loc[:, listColumns]
    return data


def back():
    temp = df.read_csv(dirData + "MGH_O3.csv")
    return temp.loc[:0]


def numString(num):
    if num < 10:
        return "0" + str(num)
    else:
        return str(num)


def deMonth(m):
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
    dates = data['fecha'];
    lenght = len(dates.index);
    years = np.ones((lenght,1))*-1;
    sinYears = np.ones((lenght,1))*-1;
    months = np.ones((lenght,1))*-1;
    sinMonths = np.ones((lenght,1))*-1;
    days = np.ones((lenght,1))*-1;
    sinDays = np.ones((lenght,1))*-1;
    wDay = np.ones((lenght,1))*-1;
    sinWday = np.ones((lenght,1))*-1;
    i  =0 ;
    for x in dates:
        d =x
        #d = datetime.strptime(x,"%Y-%m-%d %H:%M:%S")
        wD= weekday(d.year,d.month,d.day);
        wDay[i]=wD[0];
        sinWday[i]=wD[1];
        years[i] = d.year;
        #sinYears[i]= np.sin(d.year);
        months[i] = d.month;
        sinMonths[i] =(1+np.sin(((d.month-1)/11)*(2*np.pi)))/2
        days[i] = d.day
        sinDays[i]= (1+np.sin(((d.day-1)/23)*(2*np.pi)))/2
        i += 1;
    weekD = df.DataFrame(wDay, columns= ['weekday'])
    data['weekday']= weekD;
    sinWeekD = df.DataFrame(sinWday, columns= ['sinWeekday'])
    data['sinWeekday']= sinWeekD;
    dataYear = df.DataFrame(years, columns= ['year'])
    data['year'] = dataYear
    #dataSinYear = df.DataFrame(sinYears, columns= ['sinYear'])print(data);
    #data['sinYear'] = dataSinYear
    dataMonths = df.DataFrame(months, columns= ['month'])
    data['month'] = dataMonths
    dataSinMonths = df.DataFrame(sinMonths, columns= ['sinMonth'])
    data['sinMonth'] = dataSinMonths
    dataDay = df.DataFrame(days, columns= ['day'])
    data['day'] = dataDay
    dataSinDay = df.DataFrame(sinDays, columns= ['sinDay'])
    data['sinDay'] = dataSinDay
    return data;

def weekday(year,month,day):
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
    a = (14-month)/12;
    a = int(a);
    y = year-a;
    m = month+12*a-2;
    week = (day+y+int(y/4)-int(y/100)+int(y/400)+int((31*m)/12))%7;
    Week = week +1;
    sinWeek = (1+np.sin(((week-1)/7)*(2*np.pi)))/2
    return [week,sinWeek]


information = configuracion()
# nameNetcdf = "wrfout_d02_"
# hoy= datetime.strptime("2017-12-12 19:00:00",'%Y-%m-%d %H:%M:%S')
# dayer = datetime.strptime("2017-09-23 19:00:00",'%Y-%m-%d %H:%M:%S')
# actualNetcdf = nameNetcdf+ str(hoy.year)+ "-"+ str(hoy.month)+ "-"+str(hoy.day)+"_00.nc";
# actualCsv = variables[0]+"_"+str(hoy.year)+ "-"+ str(hoy.month)+ "-"+str(hoy.day)+".csv";
# ayerCsv = variables[0]+"_"+str(dayer.year)+ "-"+ str(dayer.month)+ "-"+str(dayer.day)+".csv";
# test =[hoy,dayer,actualNetcdf,actualCsv,ayerCsv]
# leerArchivo(test);
leerArchivo(information)
