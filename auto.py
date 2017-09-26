from Utilites.Utilites import prepro as an
from NNSystem.neuralNetwork import train as nn
from NNSystem.neuralNetworkGpu import train as nng
from NNSystem.neuralNetworkGpuMax import train as nngm
import pandas as df


#est =['AJM','MGH','CCA','SFE','UAX','CUA','NEZ','CAM','LPR','SJA','CHO','IZT','SAG','TAH','ATI','FAC','UIZ','MER','PED','TLA','BJU','XAL'];
est =['AJM','MGH','CCA','SFE','UAX','CUA','NEZ','CAM','LPR','SJA','IZT','SAG','TAH','ATI','FAC','UIZ','MER','PED','TLA','XAL'];
contaminant = 'O3';
dirr = 'data/unionGeo/DatosCC/'


def trainNeuralNetworks(est):
    """
    Function to train the neuralNetwork of the 23 stations,
    save the training on file trainData/[nameStation].csv
    """
    tam = len(est) -1
    i=0;
    while i <= tam:
        station = est[i];
        print(station);
        name = station +'_'+contaminant; #name the file with the data
        data = df.read_csv(dirr+name+'.csv'); #we load the data in the Variable data
        build = df.read_csv(dirr+name+'_pred.csv'); #we load the data in the Variable build
        data = data[data['fecha']<'2015/12/31'];
        build = build[build['fecha']<'2015/12/31'];
        #print(data)
        #print(build)
        #break
        data = data.fillna(value=-1);
        xy_values = an(data,build, contaminant); # preprocessing
        nng(xy_values[0],xy_values[1],xy_values[2],1000,station,contaminant); #The neural network is trained
        i+=1;

def trainNeuralNetworksNoNormalized():
    """
    Function to train the neuralNetwork of the 23 stations,
    save the training on file trainData/[nameStation].csv
    """
    tam = len(est) -1
    i=0;
    while i <= tam:
        station = est[i];
        print(station);
        name = station +'_'+contaminant; #name the file with the data
        data = df.read_csv('data/'+name+'.csv'); #we load the data in the Variable data
        build = df.read_csv('data/'+name+'_pred.csv'); #we load the data in the Variable build
        xy_values = an(data,build, contaminant); # preprocessing
        maxx = obtMax(station,contaminant);
        nngm(xy_values[0],xy_values[1],xy_values[2],1000,station,contaminant,maxx); #The neural network is trained
        i+=1;

def trainOne():
    """
    Function to train the neuralNetwork of the 1 stations,
    save the training on file trainData/[nameStation].csv
    """
    station= 'allData';
    name = station +'_'+contaminant; #name the file with the data
    data = df.read_csv('data/'+name+'.csv'); #we load the data in the Variable data
    build = df.read_csv('data/'+name+'_pred.csv'); #we load the data in the Variable build
    xy_values = an(data,build, contaminant); # preprocessing
    nng(xy_values[0],xy_values[1],xy_values[2],1000,station,contaminant); #The neural network is trained

def obtMax(station,contaminant):
    nameC = 'cont_otres_'+station.lower();
    name = station+'_'+contaminant;
    values = df.read_csv(dirr+name+'_MaxMin.csv');
    index = values.columns[0];
    va = values[(values[index]==nameC)];
    maxx = va['MAX'].values[0];
    return maxx;




est1 =['CHO']
est2 =['BJU']
trainNeuralNetworks(est);
trainNeuralNetworks(est1);
trainNeuralNetworks(est2);


#trainNeuralNetworksNoNormalized()
#trainOne();
