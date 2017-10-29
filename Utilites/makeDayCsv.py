from datetime import datetime, timedelta
from pandas import concat
import pandas as df
import numpy as np

"""
Function to create csv file with the holidays from 1996 to 2016 from another cvs file
0 = laboral
1 = oficial
2 = sep
"""

def readCsv():
    """
    Function to create csv file with the holidays from 1996 to 2016 from another cvs file
    """
    dataTemp =df.read_csv('data.csv');
    dataTemp = dataTemp.drop(labels=['Unnamed: 0','Unnamed: 1','Unnamed: 23', 'Unnamed: 24'],axis=1);
    data = fillTable(dataTemp);
    data.to_csv('../data/Festivos.csv', encoding='utf-8');



def fillTable(dataTemp):
    """
    Function to create the csv file with the holidays in the necessary format
    to add them to the other data of the neural network.
    :param dataTemp: Information from the original cvs
    :type dataTemp: DataFrame
    :return: DataFrame
    """
    column = dataTemp.columns;
    #print(anio.values);
    value = column[0];
    valAnio = dataTemp[value]
    anioC = hours24(valAnio.values);
    listt = makeDates(value);
    data = df.DataFrame(listt, columns=['fecha']);
    dataVal = df.DataFrame(anioC, columns = ['valLab']);
    data['valLab']= dataVal;
    i = 1;
    while i < len(column):
        value = column[i];
        valAnio = dataTemp[value]
        anioC = hours24(valAnio.values);
        listt = makeDates(value);
        dataComp = df.DataFrame(listt, columns=['fecha']);
        dataVal = df.DataFrame(anioC, columns = ['valLab']);
        dataComp['valLab']= dataVal;
        data= df.concat([data,dataComp], axis=0);
        i += 1;
    data = data.reset_index();
    data = data.drop(labels='index',axis=1)
    return data;


def hours24(anio):
    """
    Function to put the value of a given date in each hour of the day
    :param anio: Value to repeat for 24 hours
    :type anio: int
    :return : int array
    """
    anioComplete = [];
    for v in anio:
        for i in range(24):
            anioComplete.append(v);
    return anioComplete;



def makeDates(anio):
    """
    Function to create the dates
    :param anio: start year
    :type anio: int
    :return datetime array
    """
    listDates = [];
    date = anio+'-01-01 00:00:00';
    dateInit = datetime.strptime(date,'%Y-%m-%d %H:%M:%S');
    listDates.append(dateInit);
    val  = int(anio);
    while val == int(anio):
        dateInit = dateInit + timedelta(hours = 1);
        val = dateInit.year
        listDates.append(dateInit);
    listDates.pop();
    return listDates;

def make18():
    data = df.read_csv('../data/Festivos.csv');
    fecha = makeDates('2018');
    f = df.DataFrame(fecha, columns=['fecha']);
    zeros = np.zeros(len(f.index));
    dZ = df.DataFrame(zeros, columns = ['valLab']);
    f['valLab'] = dZ;
    festivosOficiales =['01-01','01-06','02-05','03-19','04-01','05-01','09-16','11-19','12-01','12-25']
    for  i in festivosOficiales:
        temp = f[(f.fecha >= '2018-'+i+' 00:00:00') & (f.fecha <= '2018-'+i+' 23:00:00')]
        f.loc[temp.index,'valLab'] = 1
    vac = f[(f.fecha >= '2018-01-02 00:00:00') & (f.fecha <= '2018-01-05 23:00:00')]
    f.loc[vac.index,'valLab'] = 2
    vac = f[(f.fecha >= '2018-03-26 00:00:00') & (f.fecha <= '2018-04-06 23:00:00')]
    f.loc[vac.index,'valLab'] = 2
    vac = f[(f.fecha >= '2018-06-25 00:00:00') & (f.fecha <= '2018-08-23 23:00:00')]
    f.loc[vac.index,'valLab'] = 2
    vac = f[(f.fecha >= '2018-12-24 00:00:00') & (f.fecha <= '2018-12-31 23:00:00')]
    f.loc[vac.index,'valLab'] = 2
    dataC = df.concat([data,f])
    dataC = dataC.reset_index(drop=True);
    dataC.to_csv('../data/Festivos.csv', encoding='utf-8');

make18();
#readCsv();
