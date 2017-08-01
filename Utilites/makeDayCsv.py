from datetime import datetime, timedelta
from pandas import concat
import pandas as df
import numpy as np

"""
0 = laboral
1= oficial
2 = sep
"""

def readCsv():
    #listDates = makeDates();
    #print(listDates);
    dataTemp =df.read_csv('data.csv');
    dataTemp = dataTemp.drop(labels=['Unnamed: 0','Unnamed: 1','Unnamed: 23', 'Unnamed: 24'],axis=1);
    data = fillTable(dataTemp);
    data.to_csv('Festivos.csv', encoding='utf-8');
    #print(dataTemp);



def fillTable(dataTemp):
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
        dataTotal= df.concat([data,dataComp], axis=0);
        i += 1;
    dataTotal = dataTotal.reset_index();
    dataTotal = dataTotal.drop(labels='index',axis=1)
    return dataTotal;


def hours24(anio):
    anioComplete = [];
    for v in anio:
        for i in range(24):
            anioComplete.append(v);
    return anioComplete;



def makeDates(anio):
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


#makeDates();
readCsv();
