#from datetime import datetime, timedelta
import pandas as df
import numpy as np
#import matplotlib
#matplotlib.use('agg')
#import matplotlib.pyplot as plt
#import matplotlib.ticker as ticker
#from time import time
import shutil

est = ['AJM','MGH','CCA','SFE','NEZ','CAM','LPR','SJA','IZT','SAG','TAH','FAC','CHO','BJU'];
estComplete = ['UAX','CUA','ATI','UIZ','MER','PED','TLA','XAL'];
dirDataComp = ['data/DatosCP/','data/DatosLP/','data/DatosCC/','data/DatosLC/'];
dirDataSave = ['data/DatosCPM/','data/DatosLPM/','data/DatosCCM/','data/DatosLCM/'];
#dirDataSave = ['data/DatosCPB/','data/DatosLPB/','data/DatosCCB/','data/DatosLCB/'];
dirDataMet = 'data/DatosCM/';
contaminant = 'O3';


def originDir():
    for x in range(len(dirDataComp)):
        unionData(dirDataComp[x],dirDataSave[x]);

def unionData(origin,save):
    for value in est:
        dirData = origin + value + '_'+ contaminant+'.csv';
        data = df.read_csv(dirData);
        for xs in estComplete:
            print(origin + xs);
            dirSave = save + value + '_'+ contaminant+'.csv';
            dirComple = dirDataMet + xs + '_' + contaminant+'.csv';
            dataC = df.read_csv(dirComple);
            dataC = dataC.drop(['weekday','sinWeekday','year','month','sinMonth','day','sinDay','valLab'],axis=1);
            data = data.merge(dataC,how='left',on='fecha');
        print(dirSave);
        data = data.fillna(value=-1);
        maxAndMinValues(data,value,contaminant,save)
        shutil.copy(origin+value + '_'+ contaminant+'_pred.csv',save+value + '_'+ contaminant+'_pred.csv')
        data.to_csv(dirSave,encoding = 'utf-8',index=False);



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
    if minx == -1 :
        minx = 0;
    mixmax = df.DataFrame(minx , columns = ['MIN'],index = myIndex);
    dMax = df.DataFrame(maxx, columns= ['MAX'],index=myIndex);
    mixmax['MAX']= dMax;
    mixmax.to_csv(save+nameD,encoding = 'utf-8');

def copyComplete():
    for x in range(len(dirDataComp)):
        for value in estComplete:
            shutil.copy(dirDataComp[x]+value + '_'+ contaminant+'_pred.csv',dirDataSave[x]+value + '_'+ contaminant+'_pred.csv');
            shutil.copy(dirDataComp[x]+value + '_'+ contaminant+'.csv',dirDataSave[x]+value + '_'+ contaminant+'.csv');
            shutil.copy(dirDataComp[x]+value + '_'+ contaminant+'_MaxMin.csv',dirDataSave[x]+value + '_'+ contaminant+'_MaxMin.csv');


def bootstrap(origin,save):
    for value in sta:
        dirData = origin + value + '_'+ contaminant+'.csv';
        data = df.read_csv(dirData);
        dataOzono = data['cont_otres_'+ value.lower()];


copyComplete();
originDir();

