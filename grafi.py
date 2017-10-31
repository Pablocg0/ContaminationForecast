import matplotlib.pyplot as plt
import numpy as np
import pandas as df


est =['AJM','MGH','CCA','SFE','UAX','CUA','NEZ','CAM','LPR','SJA','CHO','IZT','SAG','TAH','ATI','FAC','UIZ','MER','PED','TLA','BJU','XAL'];
numData =[845640,864594,961948,1521774,1783860,1889524,1876004,2108268,1433559,1741428,2291952,2544880,2488482,2361008,1205828,2569320,2717010,2643030,2608362,2541240,605232,2586654]
mape = [43.4844288066917,84.3841226313309,60.9279895884326,49.9786365825837,71.7688542779909,16.8099395612298,76.9027117895575,119.205165208362,26.5064569477445,102.152198460566,59.3888245888028,71.3211449069258,83.8103296349196,55.0681342239171,18.8996607231345,64.4542808370095,22.8371847306584,26.915012015363,17.938889674463,20.4457902603368,24.6707594248916,19.4579375516325]


# fig, ax1 = plt.subplots()
# t = np.arange(22)
# ax1.bar(t,numData,0.35,color='r');
# ax1.set_xlabel('Estaciones');
# plt.xticks(t+ 0.35 / 2, ('AJM','MGH','CCA','SFE','UAX','CUA','NEZ','CAM','LPR','SJA','CHO','IZT','SAG','TAH','ATI','FAC','UIZ','MER','PED','TLA','BJU','XAL'));
# ax1.set_ylabel('Numero de datos', color='r')
# ax1.tick_params('y', colors='r')
#
# ax2 = ax1.twinx()
# ax2.bar(t+0.35,mape,0.35, color='b')
# ax2.set_ylabel('Porcentaje de error', color='b')
# ax2.tick_params('y', colors='b')


def readCsv(dirr, dirrData):
    columns = [];
    correlacion = [];
    #data = df.read_csv(dirr);
    dataMet = df.read_csv(dirr+ 'Metricas.csv');
    correlacion = dataMet['IndiceCorrelacion'].values;
    est = dataMet['estacion'];
    for x in est:
        temp = df.read_csv(dirrData + x + '_03.csv')
        columns.append(len(temp.index));
    print(est)
    print(correlacion)
    print(columns)
    fig, ax1 = plt.subplots()
    fig.figure(figsize=(22.2,11.4));
    t = np.arange(22)
    ax1.bar(t,columns,0.35,color='r');
    ax1.set_xlabel('Estaciones');
    #plt.xticks(t+ 0.35 / 2, ('AJM','MGH','CCA','SFE','UAX','CUA','NEZ','CAM','LPR','SJA','CHO','IZT','SAG','TAH','ATI','FAC','UIZ','MER','PED','TLA','BJU','XAL'));
    plt.xticks(t+ 0.35 / 2, est);
    ax1.set_ylabel('Numero de datos', color='r')
    ax1.tick_params('y', colors='r')
    ax2 = ax1.twinx()
    ax2.bar(t+0.35,correlacion,0.35, color='b')
    ax2.set_ylabel('Indice de correlacion', color='b')
    ax2.tick_params('y', colors='b')
    fig.tight_layout()
    plt.savefig(dirr+'correlacionVsDatos.png');
    plt.show()





readCsv('Graficas/Predicciones/GraficasCC/','data/DatosCC/')
