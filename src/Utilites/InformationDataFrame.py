'''
File name : InformationDataFrame.py
Author: Pablo Camacho Gonzalez
Python version: 3.6.4
Date last modified: 27/02/2018
'''

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
    """
    function to create a graph of the columns and lines that has information
    each station in the  Red Automática de Monitoreo Atmosférico (RAMA)
    """
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
        numIndex.append(len(inde)*len(column));
    info = df.DataFrame(est, columns=['estacion']);
    cAnio = df.DataFrame(anio,columns=['anio']);
    cColum =df.DataFrame(columnas,columns=['columnas']);
    cIndex = df.DataFrame(numIndex,columns=['NumDatos']);
    info['anio'] = cAnio;
    info['columnas']= cColum;
    info['NumDatos']= cIndex;
    info.groupby('estacion').mean().loc[:,['anio','columnas']].plot(kind='bar', colormap='winter',figsize=(12.2,6.4),title='Numero de años y columnas con las que se entrena cada estacion.');
    plt.savefig("../Graficas/Informacion/estAnios.png", dpi=600);
    plt.show()
    plt.close()
    info.groupby('estacion').mean().loc[:,['NumDatos']].plot(kind='bar', colormap='winter',figsize=(12.2,6.4), title ='Numero renglones que tiene cada estacion');
    plt.savefig("../Graficas/Informacion/estReng.png", dpi=600);
    plt.show()
    plt.close()
    info.to_csv('../Graficas/Informacion/infEstaciones.cvs',encoding = 'utf-8',index=False);
    estImg();


def estImg():
    """
    function to create a heatmap
    """
    for value in est:
        print(value);
        name = dirr + value + '_'+contaminant+'.csv';
        data = df.read_csv(name);
        nameColumn= data.columns
        nColumn = nameColumn.tolist()
        nColumn.remove('fecha');
        colormap(name,value,nColumn);


def anios(data):
    """
    function to extract the number of years of data that a dataframe

    :param data: DataFrame
    :type data: DataFrame
    :return: numbers of years
    :return type: int
    """
    anios = data['fecha'].values
    actual = 2017
    for value in anios:
        valueAnio = datetime.strptime(value,'%Y-%m-%d %H:%M:%S');
        if valueAnio.year < actual:
            actual = valueAnio.year;
    return 2016 -actual


def nombreEst(station):
    """
    function that returns from the full name of a station

    :param station: abbreviation of the name of the station
    :type station: String
    :return: full name of the station
    :type return: String
    """
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


def nameC(nameColumn):
    """
    function that returns from the abbreviation name of a columns

    :param station: full name of the column
    :type station: String
    :return: abbreviation name of the column
    :type return: String
    """
    names = []
    for val in nameColumn:
        if 'cont_pmco' in val:
            names.append('pmco')
        elif 'cont_pmdoscinco' in val:
            names.append('pmdoscinco')
        elif 'cont_nox' in val:
            names.append('nox')
        elif 'cont_codos' in val:
            names.append('codos')
        elif 'cont_co' in val:
            names.append('co')
        elif 'cont_nodos' in val:
            names.append('nodos')
        elif 'cont_no' in val:
            names.append('no')
        elif 'cont_otres' in val:
            names.append('otres')
        elif 'cont_sodos' in val:
            names.append('sodos')
        elif 'cont_pmdiez' in val:
            names.append('pmdiez')
        else:
            names.append(val)
    return names


def colormap(name, est, nameColumn):
    """
    function to create a heatmap

    :param name: station name
    :type name: String
    :param est: station
    :type est: String
    :param nameColumn : list with the name of the dataframe columns
    :type nameColumn: String list
    """
    nameColumn = nameC(nameColumn)
    title = 'Imagen de los datos de la estacion '+ nombreEst(est);
    data = df.read_csv(name,index_col='fecha');
    plt.figure(figsize=(12.2,8.4))
    plt.title(title);
    plt.xticks(fontsize=8)
    ax = sns.heatmap(data,vmin = -1,vmax = -0.99,yticklabels=False,xticklabels=nameColumn, cbar=False, mask = data !=-1);
    plt.savefig("../Graficas/Informacion/Imagen_"+est+".png", dpi=600);
    plt.show();
    plt.close()


#information()
