import pandas as df
import numpy as np
import shutil
import os

est = ['AJM','MGH','CCA','SFE','NEZ','CAM','LPR','SJA','IZT','SAG','TAH','FAC'];
estComplete = ['UAX','CUA','ATI','UIZ','MER','PED','TLA','XAL'];
dirDataComp = ['data/DatosCP/','data/DatosLP/','data/DatosCC/','data/DatosLC/'];
#dirDataSave = ['data/DatosCPM/','data/DatosLPM/','data/DatosCCM/','data/DatosLCM/'];
dirDataSave = ['data/DatosCPB/','data/DatosLPB/','data/DatosCCB/','data/DatosLCB/'];
dirDataMet = 'data/DatosCM/';
contaminant = 'O3';


def originDir():
    for x in range(len(dirDataComp)):
        bootstrap(dirDataComp[x],dirDataSave[x]);

def unionData(origin,save):
    for value in est:
        dirData = origin + value + '_'+ contaminant+'.csv';
        data = df.read_csv(dirData);
        for xs in estComplete:
            dirSave = save + value + '_'+ contaminant+'.csv';
            dirComple = dirDataMet + xs + '_' + contaminant+'.csv';
            dataC = df.read_csv(dirComple);
            dataC = dataC.drop(['weekday','sinWeekday','year','month','sinMonth','day','sinDay','valLab'],axis=1);
            data = data.merge(dataC,how='left',on='fecha');
        maxAndMinValues(data,value,contaminant,save)
        shutil.copy(origin+value + '_'+ contaminant+'_pred.csv',save+value + '_'+ contaminant+'_pred.csv');
        data.to_csv(dirSave,encoding = 'utf-8',index=False);

def copyComplete():
    for x in range(len(dirDataComp)):
        for value in estComplete:
            shutil.copy(dirDataComp[x]+value + '_'+ contaminant+'_pred.csv',dirDataSave+value + '_'+ contaminant+'_pred.csv');
            shutil.copy(dirDataComp[x]+value + '_'+ contaminant+'.csv',dirDataSave+value + '_'+ contaminant+'.csv');
            shutil.copy(dirDataComp[x]+value + '_'+ contaminant+'_MaxMin.csv',dirDataSave+value + '_'+ contaminant+'_MaxMin.csv');

def maxAndMinValues(data,station,contaminant,save):
    """
    Function to obtain the maximun and minumum values and save them in a file
    :param data: DataFrame that contains the data from where the maximun ans minumum values will be extracted
    :type data: DataFrame
    :param station: name the station
    :type station : string
    :param contaminant: name the contaminant
    :type contaminant : string
    """
    nameD = station+'_'+contaminant+'_MaxMin'+'.csv';
    Index = data.columns;
    myIndex =Index.values
    myIndex = myIndex[1:]
    x_vals = data.values;
    x = x_vals.shape;
    columns = x[1];
    x_vals= x_vals[:,1:columns];
    minx = x_vals.min(axis=0)
    maxx = x_vals.max(axis=0);
    mixmax = df.DataFrame(minx , columns = ['MIN'],index = myIndex);
    dMax = df.DataFrame(maxx, columns= ['MAX'],index=myIndex);
    mixmax['MAX']= dMax;
    mixmax.to_csv(save+nameD,encoding = 'utf-8');


def bootstrap(origin,save):
    for value in est:
        print(value)
        dirData = origin + value + '_'+ contaminant+'.csv';
        dirPred = origin + value + '_'+ contaminant+'_pred.csv';
        data = df.read_csv(dirData);
        pred = df.read_csv(dirPred);
        data = data.merge(pred,how='left',on='fecha');
        dataOzono = data['cont_otres_'+ value.lower()];
        mean =dataOzono.mean(axis=0);
        std = dataOzono.std(axis=0);
        print(mean);
        print(std);
        dataBoot = data[data['cont_otres_'+value.lower()]>std]
        d = df.concat([data,dataBoot], axis =0);
        prediccion = df.DataFrame(d['fecha'],columns=['fecha']);
        valPred = df.DataFrame(d['cont_otres_'+value+'_delta'],columns=['cont_otres_'+value+'_delta']);
        prediccion['cont_otres_'+value+'_delta'] = valPred;
        d= d.drop('cont_otres_'+value+'_delta',axis=1);
        d = d.reset_index();
        d = d.drop('index',axis=1);
        prediccion = prediccion.reset_index();
        prediccion = prediccion.drop('index',axis=1);
        maxAndMinValues(d,value,contaminant,save);
        d.to_csv(save + value + '_'+ contaminant+'.csv',encoding = 'utf-8',index=False);
        prediccion.to_csv(save + value + '_'+ contaminant+'_pred.csv',encoding = 'utf-8',index=False);
        break

def createFile():
    est =['AJM','MGH','CCA','SFE','UAX','CUA','NEZ','CAM','LPR','SJA','CHO','IZT','SAG','TAH','ATI','FAC','UIZ','MER','PED','TLA','BJU','XAL'];
    dirData = ['data/DatosCPB/','data/DatosLPB/','data/DatosCCB/','data/DatosLCB/'];
    dirGraficas= ['Graficas/Predicciones/GraficasCPB/','Graficas/Predicciones/GraficasLPB/','Graficas/Predicciones/GraficasCCB/','Graficas/Predicciones/GraficasLCB/'];
    dirTrain = ['trainData/TrainCPB/','trainData/TrainLPB/','trainData/TrainCCB/','trainData/TrainLCB/'];
    for val in range(len(dirData)):
        if not os.path.exists(dirData[val]): os.makedirs(dirData[val]);
        if not os.path.exists(dirGraficas[val]): os.makedirs(dirGraficas[val]);
        if not os.path.exists(dirTrain[val]): os.makedirs(dirTrain[val]);
        for i in range(len(est)):
            r = dirTrain[val]+est[i];
            if not os.path.exists(r): os.makedirs(r);

createFile();
#bootstrap('data/','data/')
originDir();
copyComplete();
