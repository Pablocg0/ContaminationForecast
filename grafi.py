import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as df


#est =['AJM','MGH','CCA','SFE','UAX','CUA','NEZ','CAM','LPR','SJA','CHO','IZT','SAG','TAH','ATI','FAC','UIZ','MER','PED','TLA','BJU','XAL'];

def readCsv(dirr, dirrData):
    columns = [];
    correlacion = [];
    #data = df.read_csv(dirr);
    dataMet = df.read_csv(dirr+ 'Metricas.csv');
    dataMet = dataMet.sort_values(['Estacion']);
    correlacion = dataMet['Indice de Correlación'].values;
    est = dataMet['Estacion'];
    for x in est:
        temp = df.read_csv(dirrData + x + '_O3.csv')
        columns.append(len(temp.index));
    fig, ax1 = plt.subplots(figsize=(22.2,11.4));
    t = np.arange(22)
    plt.title('Comparacion de numero de datos vs el indice de correlacion.',fontsize= 25, y=1.1)
    ax1.bar(t,columns,0.35,color='darkblue',label='Numero de datos');
    ax1.set_xlabel('Estaciones', fontsize=18);
    ax1.grid(True,axis='y', linestyle='solid', alpha=0.5, color ='darkblue');
    plt.xticks(t+ 0.35 / 2, est);
    ax1.set_ylabel('Numero de datos', color='k', fontsize=18)
    ax1.tick_params('y', colors='k')
    ax2 = ax1.twinx()
    ax2.grid(True,axis='y', linestyle='--', alpha=0.9, color='royalblue');
    ax2.bar(t+0.35,correlacion,0.35, color='royalblue', label='Índice de correlación.')
    ax2.set_ylabel('Indice de correlación', color='k', fontsize=18)
    ax2.tick_params('y', colors='k')
    plt.xticks(t+0.35, est);
    legend_datos = mpatches.Patch(color='darkblue', label='Numero de datos');
    legend_corre = mpatches.Patch(color='royalblue', label='Índice de correlación');
    plt.legend(handles =[legend_datos,legend_corre],loc =1,bbox_to_anchor=(0.1, 1.1));
    plt.gca().spines['bottom'].set_color('lightgray');
    fig.gca().spines['left'].set_color('w');
    fig.gca().spines['top'].set_color('w');
    fig.gca().spines['right'].set_color('w');
    ax1.spines['left'].set_visible(False);
    ax1.spines['top'].set_visible(False);
    fig.tight_layout()
    plt.savefig('Graficas/Predicciones/correlacionLCB.png');
    plt.show()


readCsv('Graficas/Predicciones/GraficasLCB/','data/DatosLCB/')
