from datetime import datetime, timedelta
import matplotlib
import numpy as np
matplotlib.use('agg')
import matplotlib.pyplot as plt
import pandas as df
import seaborn as sns


est =['AJM','MGH','CCA','SFE','UAX','CUA','NEZ','CAM','LPR','SJA','IZT','SAG','TAH','ATI','FAC','UIZ','MER','PED','TLA','XAL','CHO','BJU'];
#est = ['LPR'];
dirr = '../data/DatosCC/';
contaminant = 'O3';

def information():
    anio = [];
    columnas = [];
    numIndex = [];
    for value in est:
        name = dirr + value + '_'+contaminant+'.csv';
        data = df.read_csv(name);
        a = anios(data)
        anio.append(a);
        column = data.columns
        columnas.append(len(column));
        inde = data.index;
        numIndex.append(len(inde));
    info = df.DataFrame(est, columns=['estacion']);
    cAnio = df.DataFrame(anio,columns=['anio']);
    cColum =df.DataFrame(columnas,columns=['columnas']);
    cIndex = df.DataFrame(numIndex,columns=['renglones']);
    info['anio'] = cAnio;
    info['columnas']= cColum;
    info['renglones']= cIndex;
    info.groupby('estacion').mean().loc[:,['anio','columnas']].plot(kind='bar', colormap='winter',figsize=(12.2,6.4),title='Numero de años y columnas con las que se entrena cada estacion.');
    plt.savefig("../Graficas/Informacion/estAnios.png", dpi=600);
    plt.show()
    plt.close()
    info.groupby('estacion').mean().loc[:,['renglones']].plot(kind='bar', colormap='winter',figsize=(12.2,6.4), title ='Numero renglones que tiene cada estacion');
    plt.savefig("../Graficas/Informacion/estReng.png", dpi=600);
    plt.show()
    plt.close()
    info.to_csv('../Graficas/Informacion/infEstaciones.cvs',encoding = 'utf-8',index=False);
    estImg();


def estImg():
    for value in est:
        print(value);
        name = dirr + value + '_'+contaminant+'.csv';
        data = df.read_csv(name);
        nameColumn= data.columns
        nColumn = nameColumn.tolist()
        nColumn.remove('fecha');
        colormap(name,value,nColumn);


def anios(data):
    anios = data['fecha'].values
    actual = 2017
    for value in anios:
        valueAnio = datetime.strptime(value,'%Y-%m-%d %H:%M:%S');
        if valueAnio.year < actual:
            actual = valueAnio.year;
    return 2016 -actual

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

def colormap(name,est,nameColumn):
    title = 'Imagen de los datos de la estacion '+ nombreEst(est);
    data = df.read_csv(name,index_col='fecha');
    plt.figure(figsize=(12.2,8.4))
    plt.title(title);
    plt.xticks(fontsize=8)
    ax = sns.heatmap(data,vmin = -1,vmax = -0.99,yticklabels=False,xticklabels=nameColumn, cbar=False, mask = data !=-1);
    plt.savefig("../Graficas/Informacion/Imagen_"+est+".png", dpi=600);
    plt.show();
    plt.close()


information();
