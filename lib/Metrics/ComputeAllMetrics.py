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
    plt.plot(error)
    plt.show()
    # ******** MAE *********
    mse = np.mean(np.abs(error))
    print("MAE: ", mse)

    # ******** MSE *********
    mse = np.mean(error**2)
    print("MSE: ", mse)

    # ******** RMSE *********
    rmse = np.sqrt(mse)
    print("RMSE: ", rmse)

    # ******** Index of Agreement *********
    a = np.sum(np.abs(pred-obs))
    b = 2* np.sum(np.abs(obs - mobs))
    if a <= b:
        iagree = 1 - a/b
    else:
        iagree = b/a - 1
    print("Index of Agreement: ", iagree)

    # ******** R *********
    a = obs-mobs
    b = pred-mpred
    up = np.mean(a*b)
    down = np.sqrt(np.mean(a**2))*np.sqrt(np.mean(b**2))
    pearson = up/down
    print("Pearson Correlation Coefficient: ", pearson, " NP=",np.corrcoef(pred, obs)[0,1])

    # ******** R2 *********
    # rtwo = 1 - (np.sum(error)/np.sum(obs-mobs))
    rtwo = pearson*pearson
    print("R2: ", rtwo)


if __name__ == "__main__":
    # forecast_types = {1:'Climatologia', 2:'Normal', 3:'Meteorologia',4:'Datos Limpios'}
    forecast_types = {2:'Meteorologia'}
    for year in [2017]:
        for forecast_type in forecast_types.keys():
                print("############ Forecast type", forecast_types.get(forecast_type),"  ###########")
                # ******** All stations *********
                print("\n ****** All stations")
                print("Reading data for year ", year, " ....")
                data = getData([], year, forecast_type, all=True)
                print("Done")
                getAllMetrics(data['gt'], data['fo'])

                # ******** Best 9 stations *********
                print("\n ****** Best 9 stations")
                stations = "\'ATI','BJU','CUA','LPR','MER','PED','TLA','UIZ','XAL\'"
                print("Reading data for year ",year," ....")
                data = getData(stations, year, forecast_type)
                print("Done")
                getAllMetrics(data['gt'], data['fo'])

                # ******** Only PED *********
                print("\n ****** PED station...")
                stations = "\'PED\'"
                print("Reading data for year ",year," ....")
                data = getData(stations, year, forecast_type)
                print("Done")
                getAllMetrics(data['gt'], data['fo'])
