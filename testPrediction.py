
from datetime import datetime, timedelta
import prediction as pre
import predictionMax as prem
from Utilites.metricas import metricas
import pandas as df
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from time import time


contaminant = 'O3';
loss_vec= [];
est =['AJM','MGH','CCA','SFE','UAX','CUA','NEZ','CAM','LPR','SJA','IZT','SAG','TAH','ATI','FAC','UIZ','MER','PED','TLA','XAL'];
startDate =['2015/01/01','2015/01/01','2014/08/01','2012/02/20','2012/02/20','2011/10/01','2011/07/27','2011/07/01','2011/07/01','2011/07/01','2007/07/20','1995/01/01','1995/01/01','1994/01/02','1993/01/01','1987/05/31','1986/01/16','1986/01/16','1986/01/15','1986/01/10'];
#est =['AJM','MGH','CCA','SFE','UAX','CUA','NEZ','CAM','LPR','SJA','CHO','IZT','SAG','TAH','ATI','FAC','UIZ','MER','PED','TLA','BJU','XAL'];
#startDate =['2015/01/01','2015/01/01','2014/08/01','2012/02/20','2012/02/20','2011/10/01','2011/07/27','2011/07/01','2011/07/01','2011/07/01','2007/07/20','2007/07/20','1995/01/01','1995/01/01','1994/01/02','1993/01/01','1987/05/31','1986/01/16','1986/01/16','1986/01/15','1986/01/12','1986/01/10'];
dirrDataC = 'data/DatosCP/';
dirData  = 'data/DatosLP/';
dirGraficas = 'Graficas/Predicciones/GraficasLP/'
metri = [];



def totalPredection(est):
    for x in est:
       print(x);
       trial(x);

def totalPredectionNoNorm():
    for x in est:
       print(x);
       trialNoNormalized(x);

def trial(station):
    sta = station
    name = sta +'_'+contaminant;
    temp = df.read_csv(dirrDataC + name+'.csv'); #we load the data in the Variable data
    data =temp[(temp['fecha']<= '2016/01/01') & (temp['fecha']>= '2015/12/31')];
    data = filterData(data,dirData+name+'.csv');
    tempBuild = df.read_csv(dirrDataC+name+'_pred.csv'); #we load the data in the Variable build
    build = tempBuild[(tempBuild['fecha']<= '2016/01/01') & (tempBuild['fecha']>= '2015/12/31')];
    build = build.fillna(value=0);
    l = xlabel(data)
    labels=l[0];
    location =l[1];
    arrayPred = []
    nameColumn ='cont_otres_' + sta+'_delta';
    inf= build[nameColumn].values
    index = data.index.values
    for x in index:
        pred = data.ix[x].values
        valPred = pred[1:];
        valNorm= pre.normalize(valPred,sta,contaminant);
        arrayPred.append(convert(valNorm));
    result = pre.prediction(sta,contaminant,arrayPred);
    real = desNorm(result,sta,contaminant);
    metri.append(metricas(inf,real,station));
    plt.figure(figsize=(12.2,6.4))
    plt.plot(inf,'g-', label='Valor observado.');
    plt.plot(real, 'r--',label='Pronostico 24h NN.');
    plt.title(nombreEst(station) +' ('+station+') comparación de '+ contaminant+' observado vs red neuronal');
    plt.xlabel('Fecha');
    plt.ylabel('Partes por millon (PPM)');
    plt.legend(loc ='best');
    #plt.xticks(location,labels,fontsize=8,rotation=80);
    plt.xticks(location,labels,fontsize=9);
    #plt.xlim(0,600)
    plt.savefig(dirGraficas+station+ '.png');
    plt.show();
    plt.clf();
    plt.close()
    gError(inf,real,location,labels,station)


def filterData(data, dirData):
    temp = df.read_csv(dirData);
    listColumns = list(temp.columns);
    data = data.loc[:,listColumns];
    return data;

def gError(real,pred,location,labels,station):
    valError = [];
    tam = len(real);
    for i in range(tam):
        ve = abs(real[i] - pred[i]);
        valError.append(ve);
    plt.figure(figsize=(12.2,6.4));
    plt.plot(valError, 'r-',label='Error');
    plt.title('Error en la prediccion de la estacion '+nombreEst(station) +' ('+station+')');
    plt.xlabel('Fecha');
    plt.ylabel('Error');
    plt.legend(loc ='best');
    plt.xticks(location,labels,fontsize=9);
    plt.savefig(dirGraficas+station+ '_Error.png');
    plt.show();
    plt.clf();
    plt.close()

def saveMetric():
    nameCol = ['MAPE','uTheils','IndiceCorrelacion','agreement']
    dataMet = df.DataFrame(metri, columns=['estacion','MAPE','uTheils','IndiceCorrelacion','agreement']);
    dataMet.to_csv(dirGraficas+'Metricas.csv',encoding = 'utf-8',index=False);
    print(dataMet);
    for value in nameCol:
        dataMet.groupby('estacion').mean().loc[:,[value]].plot(kind='bar',figsize=(12.2,6.4),title=value);
        plt.savefig(dirGraficas+value+".png", dpi=600);
        plt.show()
        plt.close()


def trialNoNormalized(station):
    sta = station
    name = sta +'_'+contaminant;
    temp = df.read_csv('data/'+name+'.csv'); #we load the data in the Variable data
    data =temp[(temp['fecha']<= '2016/01/01') & (temp['fecha']>= '2015/12/31')];
    tempBuild = df.read_csv('data/'+name+'_pred.csv'); #we load the data in the Variable build
    build = tempBuild[(tempBuild['fecha']<= '2016/01/01') & (tempBuild['fecha']>= '2015/12/31')];
    maxx = obtMax(station,contaminant);
    l = xlabel(data)
    labels=l[0];
    location =l[1];
    arrayPred = []
    nameColumn ='cont_otres_' + sta+'_delta';
    inf= build[nameColumn].values
    index = data.index.values
    for x in index:
        pred = data.ix[x].values
        valPred = pred[1:];
        #valNorm= pre.normalize(valPred,sta,contaminant);
        arrayPred.append(convert(valPred));
    result = prem.prediction(sta,contaminant,arrayPred,maxx);
    real = desNorm(result,sta,contaminant);
    plt.figure(figsize=(12.2,6.4))
    plt.plot(inf,'g-', label='Real value');
    plt.plot(real, 'r-',label='NN Predection');
    plt.title(nombreEst(station) +' '+ contaminant);
    plt.xlabel('Days');
    plt.ylabel('PPM');
    plt.legend(loc ='best');
    plt.xticks(location,labels,fontsize=8,rotation=80);
    #plt.xlim(0,600)
    plt.savefig('Graficas/Predicciones/Prediction'+station+ '.png');
    plt.show();
    plt.clf();
    plt.close()


def trialAllData():
    station= 'allData'
    sta = 'allData'
    name = sta +'_'+contaminant;
    temp = df.read_csv('data/'+name+'.csv'); #we load the data in the Variable data
    data =temp[(temp['fecha']<= '2016/01/01') & (temp['fecha']>= '2015/12/31')];
    tempBuild = df.read_csv('data/'+name+'_pred.csv'); #we load the data in the Variable build
    build = tempBuild[(tempBuild['fecha']<= '2016/01/01') & (tempBuild['fecha']>= '2015/12/31')];
    l = xlabel(data)
    labels=l[0];
    location =l[1];
    build=d[1];
    arrayPred = []
    nameColumn ='cont_otres_' + 'AJM'+'_delta';
    inf= build[nameColumn].values
    index = data.index.values
    for x in index:
        pred = data.ix[x].values
        valPred = pred[1:];
        valNorm= pre.normalize(valPred,sta,contaminant);
        arrayPred.append(convert(valNorm));
    result = pre.prediction(sta,contaminant,arrayPred);
    real = desNorm(result,sta,contaminant);
    plt.figure(figsize=(12.2,6.4))
    plt.plot(inf,'g-', label='Real value');
    plt.plot(real, 'r--',label='NN Prediction');
    plt.title(nombreEst('AJM') +' '+ contaminant);
    plt.xlabel('Days');
    plt.ylabel('PPM');
    plt.legend(loc ='best');
    #plt.xticks(location,labels,fontsize=6,rotation=70);
    plt.xticks(location,labels,fontsize=8);
    #plt.xlim(0,600)
    plt.savefig('Graficas/Predicciones/Prediction'+station+ '.png');
    plt.show();
    plt.clf();

def deMonth(m):
    if m == 1:
        return "Ene";
    elif m == 2:
        return "Feb";
    elif m == 3:
        return "Mar";
    elif m == 4:
        return "Abr";
    elif m == 5:
        return "May";
    elif m == 6:
        return "Jun";
    elif m == 7:
        return "Jul";
    elif m == 8:
        return "Ago";
    elif m == 9:
        return "Sep";
    elif m == 10:
        return "Oct";
    elif m == 11:
        return "Nov";
    elif m == 12:
        return "Dic";


def xlabel(data):
    fechas = [];
    location=[];
    dates = data['fecha'];
    i =0;
    m = 1;
    for x in dates:
        d =datetime.strptime(x,'%Y-%m-%d %H:%M:%S')
        if d.hour == 0 and  d.month == m:
            f = str(d.year) +'/'+ deMonth(d.month)+'/'+str(d.day);
            fechas.append(f);
            location.append(i);
            m +=1;
        i+=1;
    return [fechas,location];



def convert(data):
    size = len(data);
    vl = np.ones([1,size]);
    i = 0;
    for x in data:
        vl[0,i]= x
        i+=1;
    return vl

def desNorm(data,station,contaminant):
    real=[];
    #mini = min(data);
    #maxi = max(data);
    #print(mini)
    #print(maxi)
    nameC = 'cont_otres_'+station.lower();
    name = station+'_'+contaminant;
    values = df.read_csv(dirData+name+'_MaxMin.csv');
    index = values.columns[0];
    va = values[(values[index]==nameC)];
    maxx = va['MAX'].values[0];
    minn = va['MIN'].values[0];
    #print(maxx)
    #print(minn)
    for x in data:
        realVal = (x*(maxx-minn))+minn
        real.append(realVal);
    return real;


def nombreEst(station):
    if station == 'AJM':
        return 'Ajusco Medio';
    elif station == 'MGH':
        return 'Miguel Hidalgo';
    elif station == 'CCA':
        return 'Centro de Ciencias de la Atmosfera';
    elif station == 'SFE':
        return 'Santa Fe';
    elif station == 'UAX':
        return 'UAM Xochimilco';
    elif station == 'CUA':
        return 'Cuajimalpa';
    elif station == 'NEZ':
        return 'Nezahualcóyotl';
    elif station == 'CAM':
        return 'Camarones';
    elif station == 'LPR':
        return 'La Presa';
    elif station == 'SJA':
        return 'San Juan Aragón';
    elif station == 'CHO':
        return 'Chalco';
    elif station == 'IZT':
        return 'Iztacalco';
    elif station == 'SAG':
        return 'San Agustín';
    elif station == 'TAH':
        return 'Tlahuac';
    elif station == 'ATI':
        return 'Atizapan';
    elif station == 'FAC':
        return 'FES Acatlán';
    elif station == 'UIZ':
        return 'UAM Iztapalapa';
    elif station == 'MER':
        return 'Merced';
    elif station == 'PED':
        return 'Pedregal';
    elif station == 'TLA':
        return 'tlalnepantla';
    elif station == 'BJU':
        return 'Benito Juárez';
    elif station == 'XAL':
        return 'Xalostoc';

def obtMax(station,contaminant):
    nameC = 'cont_otres_'+station.lower();
    name = station+'_'+contaminant;
    values = df.read_csv(dirData+name+'_MaxMin.csv');
    index = values.columns[0];
    va = values[(values[index]==nameC)];
    maxx = va['MAX'].values[0];
    return maxx;


est1 =['CHO']
est2 =['BJU']
#desNorm(est[1],contaminant);
#trial();
totalPredection(est);
totalPredection(est1);
totalPredection(est2);
saveMetric();
#totalPredectionNoNorm();
#trialAllData();
