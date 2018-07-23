import sys, string
__author__="Olmo S. Zavala Romero"

import psycopg2
import numpy as np
from pathlib import Path
from pandas import DataFrame, Series
from pandas import read_sql
import matplotlib.pyplot as plt

def nicePrint(colnames, rows):
    for i in range(len(colnames)):
        print(colnames[i], " , ")

    for i in range(3):
        print(rows[i][:])

def getData(stations, year, forecast_type, all=False):
    #For Posgresql only
    try: 
        conn = psycopg2.connect("dbname='contingencia' user='soloread' host='132.248.8.238' password='SH3<t!4e'")
    except:
        print("Failed to connect to database")

    try:
        cur = conn.cursor();
        # In this case it reads from all the stations
        if all:
            sql_query = Path('SQL/GetDataMainAll.sql').read_text()
        else: # Here the stations should come as parameter
            sql_query = Path('SQL/GetDataMain.sql').read_text()
            sql_query = sql_query.replace('STATIONS', str(stations))
        sql_query = sql_query.replace('TYPEFOR', str(forecast_type))

        sql_query = sql_query.replace('YEAR', str(year))
        data = read_sql(sql_query, conn, parse_dates={'date_gt':'YYYY-MM-DD HH:MM:SS'})

    except Exception as e:
        print("Something failed!!!!!!!!!", str(e))
        print("Closing connection...")
        conn.close()
        return []

    print("Done, closing connection...")
    conn.close()
    return data

def getAllMetrics(obs, pred):
    error = obs - pred # Error
    mobs = np.mean(obs) # Mean observed
    mpred = np.mean(pred) # Mean predicted
    # ******** MAE *********
    mse = np.mean(np.abs(error))

    # ******** MSE *********
    mse = np.mean(error**2)

    # ******** RMSE *********
    rmse = np.sqrt(mse)

    # ******** Index of Agreement *********
    a = np.sum(np.abs(pred-obs))
    b = 2* np.sum(np.abs(obs - mobs))
    if a <= b:
        iagree = 1 - a/b
    else:
        iagree = b/a - 1

    # ******** R *********
    a = obs-mobs
    b = pred-mpred
    up = np.mean(a*b)
    down = np.sqrt(np.mean(a**2))*np.sqrt(np.mean(b**2))
    pearson = up/down

    # ******** R2 *********
    # rtwo = 1 - (np.sum(error)/np.sum(obs-mobs))
    rtwo = pearson*pearson

    print("MSE: ", mse)
    print("RMSE: ", rmse)
    print("R2: ", rtwo)
    print("Index of Agreement: ", iagree)
    print("Pearson Correlation Coefficient: ", pearson, " NP=",np.corrcoef(pred, obs)[0,1])

    return [mse, rmse, iagree, pearson, rtwo]

def plotByStation(data, title, stations):
    '''Computes all the metrics from the paper by station'''

    print("******************")
    corr_coef = np.zeros(len(stations))
    idx_agreement = np.zeros(len(stations))
    rmse_all = np.zeros(len(stations))
    rsquared = np.zeros(len(stations))
    for i, station in enumerate(stations):

        idx = data['id_est'] == station
        obs = data.ix[idx]['gt'].values
        pred = data.ix[idx]['fo'].values

        [mse, rmse, iagree, pearson, rtwo] = getAllMetrics(obs,pred)

        corr_coef[i] = pearson
        rsquared[i] = rtwo
        rmse_all[i] = np.sqrt(mse)
        idx_agreement[i] = iagree

    generalPlot(stations,corr_coef,'{} Pearson Correlation Coefficient '.format(title))
    generalPlot(stations,rmse_all,'{} RMSE'.format(title))
    generalPlot(stations,rsquared,'{} R^2'.format(title))
    generalPlot(stations,idx_agreement,'{} Index of agreement'.format(title))

def generalPlot(x,y,title, figsize=[9,5]):
    f = plt.figure(figsize=figsize)
    plt.bar(x, y)
    plt.title(title)
    plt.ylim([min(y)-.05, max(y)+.02])
    plt.savefig('imgs/Final_Figures/{}.png'.format(title.replace(' ','_')))
    plt.show()

if __name__ == "__main__":
    # forecast_types = {1:'Climatologia', 2:'Normal (TensorFlow)', 3:'Normal (Keras)',4:'Datos Limpios', 5:'Correlacion (Keras)'}
    forecast_types = {3:'Keras'}
    for year in [2017]:
        for forecast_type in forecast_types.keys():
                print("############ Forecast type", forecast_types.get(forecast_type),"  ###########")
                # ******** All stations *********
                print("\n ****** All stations")
                print("Reading data for year ", year, " ....")
                data = getData([], year, forecast_type, all=True)
                print("Done")
                ## All data has ben read
                # getAllMetrics(data['gt'], data['fo'])

                stations = data['id_est'].unique()
                plotByStation(data, 'All stations', stations)

                # ******** Best 9 stations *********
                print("\n ****** Best 9 stations")
                stations = "\'ATI','BJU','CUA','LPR','MER','PED','TLA','UIZ','XAL\'"
                print("Reading data for year ",year," ....")
                data = getData(stations, year, forecast_type)
                print("Done")
                getAllMetrics(data['gt'], data['fo'])

                stations = ['ATI','BJU','CUA','LPR','MER','PED','TLA','UIZ','XAL']
                plotByStation(data, 'Top 9', stations)

                # ******** Only PED *********
                print("\n ****** PED station...")
                stations = "\'PED\'"
                print("Reading data for year ",year," ....")
                data = getData(stations, year, forecast_type)
                print("Done")
                getAllMetrics(data['gt'], data['fo'])
