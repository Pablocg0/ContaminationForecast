
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
metri = [];



def totalPredection(est,dirData,dirrDataC,dirGraficas,dirTrain):
    for x in est:
       print(x);
       trial(x,dirData,dirrDataC,dirGraficas,dirTrain);

def totalPredectionNoNorm():
    for x in est:
       print(x);
       trialNoNormalized(x);  

def trial(station,dirData,dirrDataC,dirGraficas,dirTrain):
    sta = station
    name = sta +'_'+contaminant;
    temp = df.read_csv(dirrDataC + name+'.csv'); #we load the data in the Variable data
    temp = temp.fillna(value=-1.0)
    data =temp[(temp['fecha']<= '2017/01/01') & (temp['fecha']>= '2016/12/31')];
    data = data.reset_index(drop=True)
    data = filterData(data,dirData+name+'.csv');
    data = data.fillna(value=-1.0)
    tempBuild = df.read_csv(dirrDataC+name+'_pred.csv'); #we load the data in the Variable build
    tempBuild = tempBuild.fillna(value = -1.0)
    build = tempBuild[(tempBuild['fecha']<= '2017/01/01') & (tempBuild['fecha']>= '2016/12/31')];
    build = build.reset_index(drop=True);
    build = build.fillna(value=-1.0);
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
        valNorm= pre.normalize(valPred,sta,contaminant,dirData);
        arrayPred.append(convert(valNorm));
    result = pre.prediction(sta,contaminant,arrayPred,dirTrain,dirData);
    real = desNorm(result,sta,contaminant,dirData);
    metri.append(metricas(inf,real,station));
    plt.figure(figsize=(22.2,11.4))
    plt.plot(inf,'g--', label='Valor observado.');
    plt.plot(real, 'ro-',label='Pronostico 24h NN.');
    plt.title(nombreEst(station) +' ('+station+') comparación de '+ contaminant+' observado vs red neuronal (2017)',fontsize=20);
    plt.xlabel('Fecha',fontsize= 11);
    plt.ylabel('Partes por millon (PPM)',fontsize=11);
    plt.legend(loc ='best');
    #plt.xticks(location,labels,fontsize=8,rotation=80);
    plt.xticks(location,labels,fontsize=11);
    #plt.xlim(0,600)
    plt.savefig(dirGraficas+station+ '.png');  
    plt.show();
    plt.clf();
    plt.close()
    gError(inf,real,location,labels,station,dirGraficas)
    graSubPlot(inf,real,station,location,dirGraficas,labels)


def filterData(data, dirData):
    temp = df.read_csv(dirData);
    listColumns = list(temp.columns);
    data = data.loc[:,listColumns];
    return data;

def gError(real,pred,location,labels,station,dirGraficas):
    valError = [];
    suma = 0; 
    tam = len(real);
    for i in range(tam):
        ve = abs(real[i] - pred[i]);
        valError.append(ve);
    mape = (suma/len(real)) *100
    plt.figure(figsize=(22.2,11.4))
    plt.plot(valError, 'r-',label='Error');
    plt.title('Error en la prediccion de la estacion '+nombreEst(station) +' ('+station+')(2017)',fontsize=20);
    plt.xlabel('Fecha',fontsize=11);
    plt.ylabel('Error');
    plt.legend(loc ='best');
    plt.xticks(location,labels,fontsize=11);
    plt.savefig(dirGraficas+station+ '_Error.png');
    plt.show();
    plt.clf();
    plt.close()

def graSubPlot(obs,calcu,station,location,dirGraficas,labels):
    plt.figure(figsize=(22.2,11.4))
    plt.subplot(2, 1, 1)
    plt.plot(obs, 'g-', label='Valor observado.')
    plt.title(nombreEst(station) +' ('+station+') comparación de '+ contaminant+' observado vs red neuronal (2017)',fontsize=20);
    plt.ylabel('Partes por millon (PPM)',fontsize=11);
    plt.legend(loc ='best');
    plt.xticks(location,labels,fontsize=11);
    plt.subplot(2, 1, 2)
    plt.plot(calcu, 'r--',label='Pronostico 24h NN.');
    plt.xlabel('Fecha', fontsize=15);
    plt.ylabel('Partes por millon (PPM)',fontsize=11);
    plt.legend(loc ='best');
    plt.xticks(location,labels,fontsize=11);
    plt.savefig(dirGraficas+station+ '_scatter.png');
    plt.show();
    plt.clf();
    plt.close()

def saveMetric(dirGraficas):
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
    one =datetime.strptime(dates[0],'%Y-%m-%d %H:%M:%S')
    m = one.month;
    for x in dates:
        d =datetime.strptime(x,'%Y-%m-%d %H:%M:%S')
        if d.hour == 0 and  d.month == m:
            #f = str(d.year) +'/'+ deMonth(d.month)+'/'+str(d.day);
            f = deMonth(d.month);
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

def desNorm(data,station,contaminant,dirData):
    real=[];
    #mini = min(data);
    #maxi = max(data);
    #print(mini)
    #print(maxi)
    nameC = 'cont_otres_'+station.lower();
    #nameC= 'cont_otres'
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



def init(dirData,dirrDataC,dirGraficas,dirTrain):
    est =['AJM','MGH','CCA','SFE','UAX','CUA','NEZ','CAM','LPR','SJA','IZT','SAG','TAH','ATI','FAC','UIZ','MER','PED','TLA','XAL'];
    est1 =['CHO']
    est2 =['BJU']
    totalPredection(est,dirData,dirrDataC,dirGraficas,dirTrain);
    totalPredection(est1,dirData,dirrDataC,dirGraficas,dirTrain);
    totalPredection(est2,dirData,dirrDataC,dirGraficas,dirTrain);
    saveMetric(dirGraficas);

