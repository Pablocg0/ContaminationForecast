from Utilites.Utilites import prepro as an
from Utilites.FormatData import FormatData as fd
from tests.neuralNetwork import train as nn
import pandas as df


est =['AJM','ATI','BJU','CAM','CCA','CHO','CUA','FAC','IZT','LPR','MER','MGH','NEZ','PED','SAG','SFE','SJA','TAH','TLA','UAX','UIZ','XAL'];
contaminant = 'O3';


def trainNeuralNetworks():
    """
    Function to train the neuralNetwork of the 23 stations,
    save the training on file trainData/[nameStation].csv
    """
    i=0;
    while i <= 2:
        station = est[i];
        print(station);
        name = station +'_'+contaminant; #name the file with the data
        data = df.read_csv('data/'+name+'.csv'); #we load the data in the Variable data
        build = df.read_csv('data/'+name+'_pred.csv'); #we load the data in the Variable build
        xy_values = an(data,build, contaminant); # preprocessing
        nn(xy_values[0],xy_values[1],xy_values[2],1000,station,contaminant); #The neural network is trained
        i+=1;

trainNeuralNetworks();
