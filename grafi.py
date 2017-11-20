import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as df


est =['AJM','MGH','CCA','SFE','UAX','CUA','NEZ','CAM','LPR','SJA','CHO','IZT','SAG','TAH','ATI','FAC','UIZ','MER','PED','TLA','BJU','XAL'];

def readCsv(dirr, dirrData):
    columns = [];
    correlacion = [];
    #data = df.read_csv(dirr);
    dataMet = df.read_csv(dirr+ 'Metricas.csv');
    correlacion = dataMet['IndiceCorrelacion'].values;
    est = dataMet['estacion'];
    for x in est:
        temp = df.read_csv(dirrData + x + '_O3.csv')
        columns.append(len(temp.index));
    fig, ax1 = plt.subplots(figsize=(22.2,11.4));
    t = np.arange(22)
    plt.title('Comparacion de numero de datos vs el indice de correlacion.',fontsize= 25)
    ax1.bar(t,columns,0.35,color='mediumseagreen');
    ax1.set_xlabel('Estaciones');
    plt.xticks(t+ 0.35 / 2, est);
    ax1.set_ylabel('Numero de datos', color='mediumseagreen')
    ax1.tick_params('y', colors='mediumseagreen')
    ax2 = ax1.twinx()
    ax2.bar(t+0.35,correlacion,0.35, color='royalblue')
    ax2.set_ylabel('Indice de correlación', color='royalblue')
    ax2.tick_params('y', colors='royalblue')
    fig.tight_layout()
    plt.savefig('Graficas/Predicciones/correlacionLCB1.png');
    plt.show()


readCsv('Graficas/Predicciones/GraficasLCB/','data/DatosLCB/')
