import pandas as df
import numpy as np
import shutil
import os

est = ['AJM','MGH','CCA','SFE','NEZ','CAM','LPR','SJA','IZT','SAG','TAH','FAC','CHO','BJU'];
estComplete = ['UAX','CUA','ATI','UIZ','MER','PED','TLA','XAL'];
dirDataComp = ['data/DatosCP/','data/DatosLP/','data/DatosCC/','data/DatosLC/'];
#dirDataSave = ['data/DatosCPM/','data/DatosLPM/','data/DatosCCM/','data/DatosLCM/'];
dirDataSave = ['data/DatosCPB/','data/DatosLPB/','data/DatosCCB/','data/DatosLCB/'];
#dirDataSave = ['data/unionGeo/DatosCC/','data/unionGeo/DatosLC/','data/unionGeo/DatosCP/','data/unionGeo/DatosLP/'];
dirDataMet = 'data/DatosCM/';
contaminant = 'O3';


def originDir():
    for x in range(len(dirDataComp)):
        bootstrap(dirDataComp[x],dirDataSave[x]);

def unionData(origin,save):
    print(origin)
    for value in est:
        dirData = origin + value + '_'+ contaminant+'.csv';
        data = df.read_csv(dirData);
        for xs in estComplete:
            print(xs)
            dirSave = save + value + '_'+ contaminant+'.csv';
            dirComple = origin + xs + '_' + contaminant+'.csv';
            dataC = df.read_csv(dirComple);
            dataC = dataC.drop(['weekday','sinWeekday','year','month','sinMonth','day','sinDay','valLab'],axis=1);
            data = data.merge(dataC,how='left',on='fecha');
        data = data.fillna(value=-1)
        maxAndMinValues(data,value,contaminant,save)
        shutil.copy(origin+value + '_'+ contaminant+'_pred.csv',save+value + '_'+ contaminant+'_pred.csv');
        data.to_csv(dirSave,encoding = 'utf-8',index=False);

def copyComplete():
    for x in range(len(dirDataComp)):
        for value in estComplete:
            shutil.copy(dirDataComp[x]+value + '_'+ contaminant+'_pred.csv',dirDataSave[x]+value + '_'+ contaminant+'_pred.csv');
            shutil.copy(dirDataComp[x]+value + '_'+ contaminant+'.csv',dirDataSave[x]+value + '_'+ contaminant+'.csv');
            shutil.copy(dirDataComp[x]+value + '_'+ contaminant+'_MaxMin.csv',dirDataSave[x]+value + '_'+ contaminant+'_MaxMin.csv');

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
        print(origin+value)
        dirData = origin + value + '_'+ contaminant+'.csv';
        dirPred = origin + value + '_'+ contaminant+'_pred.csv';
        data = df.read_csv(dirData);
        pred = df.read_csv(dirPred);
        data = data.merge(pred,how='left',on='fecha');
        dataOzono = data['cont_otres_'+ value.lower()];
        mean =dataOzono.mean(axis=0);
        std = dataOzono.std(axis=0);
        dataBoot = data[data['cont_otres_'+value.lower()]>std]
        d = df.concat([data,dataBoot], axis =0);
        print(len(d.index.tolist()));
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


def unionGeo(origin,save):
    print('TAH')
    data = df.read_csv(origin+'TAH_O3.csv');
    dataCo = df.read_csv(origin+'UAX_O3.csv');
    pred = df.read_csv(origin+'TAH_O3_pred.csv');
    pred.rename(columns={'cont_otres_TAH_delta':'delta'},inplace =True);
    data = data.merge(pred,how='left',on='fecha');
    predCo =  df.read_csv(origin+'UAX_O3_pred.csv');
    predCo.rename(columns={'cont_otres_UAX_delta':'delta'},inplace =True);
    dataCo = dataCo.merge(predCo,how='left',on='fecha');
    dataComplete = df.concat([data,dataCo],ignore_index=True).drop_duplicates(['fecha']).reset_index(drop=True);
    prediccion = df.DataFrame(dataComplete['fecha'],columns=['fecha']);
    prediccion['cont_otres_TAH_delta'] = dataComplete['delta'];
    dataComplete= dataComplete.drop('delta',axis=1);
    dataComplete = dataComplete.reset_index();
    dataComplete = dataComplete.drop('index',axis=1);
    prediccion = prediccion.reset_index();
    prediccion = prediccion.drop('index',axis=1);
    maxAndMinValues(dataComplete,'TAH',contaminant,save);
    dataComplete = dataComplete.fillna(value =-1);
    prediccion = prediccion.fillna(value = -1);
    dataComplete.to_csv(save +'TAH'+ '_'+ contaminant+'.csv',encoding = 'utf-8',index=False);
    prediccion.to_csv(save +'TAH'+ '_'+ contaminant+'_pred.csv',encoding = 'utf-8',index=False);
    print('CHO')
    data = df.read_csv(origin+'CHO_O3.csv');
    dataCo = df.read_csv(origin+'UAX_O3.csv');
    pred = df.read_csv(origin+'CHO_O3_pred.csv');
    pred.rename(columns={'cont_otres_CHO_delta':'delta'},inplace =True);
    data = data.merge(pred,how='left',on='fecha');
    predCo =  df.read_csv(origin+'UAX_O3_pred.csv');
    predCo.rename(columns={'cont_otres_UAX_delta':'delta'},inplace =True);
    dataCo = dataCo.merge(predCo,how='left',on='fecha');
    dataComplete = df.concat([data,dataCo],ignore_index=True).drop_duplicates(['fecha'],keep='last').reset_index(drop=True);
    prediccion = df.DataFrame(dataComplete['fecha'],columns=['fecha']);
    prediccion['cont_otres_CHO_delta'] = dataComplete['delta'];
    dataComplete= dataComplete.drop('delta',axis=1);
    dataComplete = dataComplete.reset_index();
    dataComplete = dataComplete.drop('index',axis=1);
    prediccion = prediccion.reset_index();
    prediccion = prediccion.drop('index',axis=1);
    maxAndMinValues(dataComplete,'CHO',contaminant,save);
    dataComplete = dataComplete.fillna(value =-1);
    prediccion = prediccion.fillna(value = -1);
    dataComplete.to_csv(save +'CHO'+ '_'+ contaminant+'.csv',encoding = 'utf-8',index=False);
    prediccion.to_csv(save +'CHO'+ '_'+ contaminant+'_pred.csv',encoding = 'utf-8',index=False);
    print('FAC')
    data = df.read_csv(origin+'FAC_O3.csv');
    dataCo = df.read_csv(origin+'TLA_O3.csv');
    pred = df.read_csv(origin+'FAC_O3_pred.csv');
    pred.rename(columns={'cont_otres_FAC_delta':'delta'},inplace =True);
    data = data.merge(pred,how='left',on='fecha');
    predCo =  df.read_csv(origin+'TLA_O3_pred.csv');
    predCo.rename(columns={'cont_otres_TLA_delta':'delta'},inplace =True);
    dataCo = dataCo.merge(predCo,how='left',on='fecha');
    dataCo2 = df.read_csv(origin+'ATI_O3.csv');
    predCo2 =  df.read_csv(origin+'ATI_O3_pred.csv');
    predCo2.rename(columns={'cont_otres_ATI_delta':'delta'},inplace =True);
    dataCo2 = dataCo2.merge(predCo2,how='left',on='fecha');
    dataComplete2 = df.concat([data,dataCo,dataCo2],ignore_index=True).drop_duplicates(['fecha'],keep='last').reset_index(drop=True);
    prediccion = df.DataFrame(dataComplete2['fecha'],columns=['fecha']);
    prediccion['cont_otres_FAC_delta'] = dataComplete2['delta']
    dataComplete2 = dataComplete2.drop('delta',axis=1);
    dataComplete2 = dataComplete2.reset_index();
    dataComplete2 = dataComplete2.drop('index',axis=1);
    prediccion = prediccion.reset_index();
    prediccion = prediccion.drop('index',axis=1);
    maxAndMinValues(dataComplete2,'FAC',contaminant,save);
    dataComplete2 = dataComplete2.fillna(value =-1);
    prediccion = prediccion.fillna(value = -1);
    dataComplete2.to_csv(save +'FAC'+ '_'+ contaminant+'.csv',encoding = 'utf-8',index=False);
    prediccion.to_csv(save +'FAC'+ '_'+ contaminant+'_pred.csv',encoding = 'utf-8',index=False);
    print('NEZ')
    data = df.read_csv(origin+'NEZ_O3.csv');
    dataCo = df.read_csv(origin+'UIZ_O3.csv');
    pred = df.read_csv(origin+'NEZ_O3_pred.csv');
    pred.rename(columns={'cont_otres_NEZ_delta':'delta'},inplace =True);
    data = data.merge(pred,how='left',on='fecha');
    predCo =  df.read_csv(origin+'UIZ_O3_pred.csv');
    predCo.rename(columns={'cont_otres_UIZ_delta':'delta'},inplace =True);
    dataCo = dataCo.merge(predCo,how='left',on='fecha')
    dataComplete = df.concat([data,dataCo],ignore_index=True).drop_duplicates(['fecha'],keep='last').reset_index(drop=True);
    prediccion = df.DataFrame(dataComplete['fecha'],columns=['fecha']);
    prediccion['cont_otres_NEZ_delta'] = dataComplete['delta']
    dataComplete= dataComplete.drop('delta',axis=1);
    dataComplete = dataComplete.reset_index();
    dataComplete = dataComplete.drop('index',axis=1);
    prediccion = prediccion.reset_index();
    prediccion = prediccion.drop('index',axis=1);
    maxAndMinValues(dataComplete,'NEZ',contaminant,save);
    dataComplete = dataComplete.fillna(value =-1);
    prediccion = prediccion.fillna(value = -1);
    dataComplete.to_csv(save +'NEZ'+ '_'+ contaminant+'.csv',encoding = 'utf-8',index=False);
    prediccion.to_csv(save +'NEZ'+ '_'+ contaminant+'_pred.csv',encoding = 'utf-8',index=False);
    print('CAM')
    data = df.read_csv(origin+'CAM_O3.csv');
    dataCo = df.read_csv(origin+'LPR_O3.csv');
    pred = df.read_csv(origin+'CAM_O3_pred.csv');
    pred.rename(columns={'cont_otres_CAM_delta':'delta'},inplace =True);
    data = data.merge(pred,how='left',on='fecha');
    predCo =  df.read_csv(origin+'LPR_O3_pred.csv');
    predCo.rename(columns={'cont_otres_LPR_delta':'delta'},inplace =True);
    dataCo = dataCo.merge(predCo,how='left',on='fecha')
    dataCo2 = df.read_csv(origin+'XAL_O3.csv');
    predCo2 =  df.read_csv(origin+'XAL_O3_pred.csv');
    predCo2.rename(columns={'cont_otres_XAL_delta':'delta'},inplace =True);
    dataCo2 = dataCo2.merge(predCo2,how='left',on='fecha')
    dataComplete2 = df.concat([data,dataCo,dataCo2],ignore_index=True).drop_duplicates(['fecha'],keep='last').reset_index(drop=True);
    prediccion = df.DataFrame(dataComplete2['fecha'],columns=['fecha']);
    prediccion['cont_otres_CAM_delta'] = dataComplete2['delta']
    dataComplete2 = dataComplete2.drop('delta',axis=1);
    dataComplete2 = dataComplete2.reset_index();
    dataComplete2 = dataComplete2.drop('index',axis=1);
    prediccion = prediccion.reset_index();
    prediccion = prediccion.drop('index',axis=1);
    maxAndMinValues(dataComplete2,'CAM',contaminant,save);
    dataComplete2 = dataComplete2.fillna(value =-1);
    prediccion = prediccion.fillna(value = -1);
    dataComplete2.to_csv(save +'CAM'+ '_'+ contaminant+'.csv',encoding = 'utf-8',index=False);
    prediccion.to_csv(save +'CAM'+ '_'+ contaminant+'_pred.csv',encoding = 'utf-8',index=False);
    print('SFE')
    data = df.read_csv(origin+'SFE_O3.csv');
    dataCo = df.read_csv(origin+'CUA_O3.csv');
    pred = df.read_csv(origin+'SFE_O3_pred.csv');
    pred.rename(columns={'cont_otres_SFE_delta':'delta'},inplace =True);
    data = data.merge(pred,how='left',on='fecha');
    predCo =  df.read_csv(origin+'CUA_O3_pred.csv');
    predCo.rename(columns={'cont_otres_CUA_delta':'delta'},inplace =True);
    dataCo = dataCo.merge(predCo,how='left',on='fecha')
    dataCo2 = df.read_csv(origin+'PED_O3.csv');
    predCo2 =  df.read_csv(origin+'PED_O3_pred.csv');
    predCo2.rename(columns={'cont_otres_PED_delta':'delta'},inplace =True);
    dataCo2 = dataCo2.merge(predCo2,how='left',on='fecha')
    dataComplete2 = df.concat([data,dataCo,dataCo2],ignore_index=True).drop_duplicates(['fecha'],keep='last').reset_index(drop=True);
    prediccion = df.DataFrame(dataComplete2['fecha'],columns=['fecha']);
    prediccion['cont_otres_SFE_delta'] = dataComplete2['delta']
    dataComplete2 = dataComplete2.drop('delta',axis=1);
    dataComplete2 = dataComplete2.reset_index();
    dataComplete2 = dataComplete2.drop('index',axis=1);
    prediccion = prediccion.reset_index();
    prediccion = prediccion.drop('index',axis=1)
    maxAndMinValues(dataComplete2,'SFE',contaminant,save);
    dataComplete2 = dataComplete2.fillna(value =-1);
    prediccion = prediccion.fillna(value = -1);
    dataComplete2.to_csv(save +'SFE'+ '_'+ contaminant+'.csv',encoding = 'utf-8',index=False);
    prediccion.to_csv(save +'SFE'+ '_'+ contaminant+'_pred.csv',encoding = 'utf-8',index=False);
    est = ['AJM','CCA','BJU'];
    dataCo = df.read_csv(origin+'PED_O3.csv');
    predCo = df.read_csv(origin+'PED_O3_pred.csv');
    predCo.rename(columns={'cont_otres_PED_delta':'delta'},inplace =True);
    dataCo = dataCo.merge(predCo,how='left',on='fecha')
    print(len(dataCo.index))
    for x in est :
        data = df.read_csv(origin+ x + '_O3.csv');
        pred = df.read_csv(origin+x+'_O3_pred.csv');
        pred.rename(columns={'cont_otres_'+x+'_delta':'delta'},inplace =True);
        data = data.merge(pred,how='left',on='fecha');
        dataComplete= df.concat([data,dataCo],ignore_index=True).drop_duplicates(['fecha'],keep='last').reset_index(drop=True);
        print(x)
        prediccion = df.DataFrame(dataComplete['fecha'],columns=['fecha']);
        prediccion['cont_otres_'+x+'_delta'] = dataComplete['delta']
        dataComplete= dataComplete.drop('delta',axis=1);
        dataComplete = dataComplete.reset_index();
        dataComplete = dataComplete.drop('index',axis=1);
        prediccion = prediccion.reset_index();
        prediccion = prediccion.drop('index',axis=1);
        maxAndMinValues(dataComplete,x,contaminant,save);
        dataComplete = dataComplete.fillna(value =-1);
        prediccion = prediccion.fillna(value = -1);
        dataComplete.to_csv(save +x+ '_'+ contaminant+'.csv',encoding = 'utf-8',index=False);
        prediccion.to_csv(save +x+ '_'+ contaminant+'_pred.csv',encoding = 'utf-8',index=False);
    est = ['SAG','LPR'];
    dataCo = df.read_csv(origin+'XAL_O3.csv');
    predCo = df.read_csv(origin+'XAL_O3_pred.csv');
    predCo.rename(columns={'cont_otres_XAL_delta':'delta'},inplace =True);
    dataCo = dataCo.merge(predCo,how='left',on='fecha')
    print(len(dataCo.index))
    for x in est :
        data = df.read_csv(origin+ x + '_O3.csv');
        pred = df.read_csv(origin+x+'_O3_pred.csv');
        pred.rename(columns={'cont_otres_'+x+'_delta':'delta'},inplace =True);
        data = data.merge(pred,how='left',on='fecha');
        dataComplete= df.concat([data,dataCo],ignore_index=True).drop_duplicates(['fecha'],keep='last').reset_index(drop=True);
        print(x)
        prediccion = df.DataFrame(dataComplete['fecha'],columns=['fecha']);
        prediccion['cont_otres_'+x+'_delta'] = dataComplete['delta']
        dataComplete= dataComplete.drop('delta',axis=1);
        dataComplete = dataComplete.reset_index();
        dataComplete = dataComplete.drop('index',axis=1);
        prediccion = prediccion.reset_index();
        prediccion = prediccion.drop('index',axis=1);
        maxAndMinValues(dataComplete,x,contaminant,save);
        dataComplete = dataComplete.fillna(value =-1);
        prediccion = prediccion.fillna(value = -1);
        dataComplete.to_csv(save +x+ '_'+ contaminant+'.csv',encoding = 'utf-8',index=False);
        prediccion.to_csv(save +x+ '_'+ contaminant+'_pred.csv',encoding = 'utf-8',index=False);
    est = ['SJA','IZT','MGH'];
    dataCo = df.read_csv(origin+'MER_O3.csv');
    predCo = df.read_csv(origin+'MER_O3_pred.csv');
    predCo.rename(columns={'cont_otres_MER_delta':'delta'},inplace =True);
    dataCo = dataCo.merge(predCo,how='left',on='fecha')
    print(len(dataCo.index))
    for x in est :
        data = df.read_csv(origin+ x + '_O3.csv');
        pred = df.read_csv(origin+x+'_O3_pred.csv');
        pred.rename(columns={'cont_otres_'+x+'_delta':'delta'},inplace =True);
        data = data.merge(pred,how='left',on='fecha');
        dataComplete= df.concat([data,dataCo],ignore_index=True).drop_duplicates(['fecha'],keep='last').reset_index(drop=True);
        print(x)
        prediccion = df.DataFrame(dataComplete['fecha'],columns=['fecha']);
        prediccion['cont_otres_'+x+'_delta'] = dataComplete['delta']
        dataComplete= dataComplete.drop('delta',axis=1);
        dataComplete = dataComplete.reset_index();
        dataComplete = dataComplete.drop('index',axis=1);
        prediccion = prediccion.reset_index();
        prediccion = prediccion.drop('index',axis=1);
        maxAndMinValues(dataComplete,x,contaminant,save);
        dataComplete = dataComplete.fillna(value =-1);
        prediccion = prediccion.fillna(value = -1);
        dataComplete.to_csv(save +x+ '_'+ contaminant+'.csv',encoding = 'utf-8',index=False);
        prediccion.to_csv(save +x+ '_'+ contaminant+'_pred.csv',encoding = 'utf-8',index=False);

def createFile():
    est =['AJM','MGH','CCA','SFE','UAX','CUA','NEZ','CAM','LPR','SJA','CHO','IZT','SAG','TAH','ATI','FAC','UIZ','MER','PED','TLA','BJU','XAL'];
    dirData = ['data/unionGeo/DatosCC/','data/unionGeo/DatosLC/','data/unionGeo/DatosCP/','data/unionGeo/DatosLP/'];
    dirGraficas= ['Graficas/Predicciones/unionGeo/GraficasCC/','Graficas/Predicciones/unionGeo/GraficasCP/','Graficas/Predicciones/unionGeo/GraficasLC/','Graficas/Predicciones/unionGeo/GraficasLP/'];
    dirTrain = ['trainData/unionGeo/TrainCP/','trainData/unionGeo/TrainLP/','trainData/unionGeo/TrainCC/','trainData/unionGeo/TrainLC/'];
    for val in range(len(dirData)):
        if not os.path.exists(dirData[val]): os.makedirs(dirData[val]);
        if not os.path.exists(dirGraficas[val]): os.makedirs(dirGraficas[val]);
        if not os.path.exists(dirTrain[val]): os.makedirs(dirTrain[val]);
        for i in range(len(est)):
            r = dirTrain[val]+est[i];
            if not os.path.exists(r): os.makedirs(r);

#createFile();
#bootstrap('data/','data/')
originDir();
#unionGeo();
copyComplete();

