__author__="Olmo S. Zavala Romero"

import psycopg2
import numpy as np
from pathlib import Path
from pandas import DataFrame, Series
from pandas import read_sql
import matplotlib.pyplot as plt
from dateutil.parser import parse
from ComputeAllMetrics import *

def getClimatology(id_est, id_cont):
    #For Posgresql only
    try:
        conn = psycopg2.connect("dbname='contingencia' user='soloread' host='132.248.8.238' password='SH3<t!4e'")
    except:
        print("Failed to connect to database")

    try:
        cur = conn.cursor();
        # In this case it reads from all the stations
        if all:
            sql_query = "SELECT * FROM climatologia WHERE id_est='{}' AND id_cont='{}'".format(id_est, id_cont)

        data = read_sql(sql_query, conn)

    except Exception as e:
        print("Something failed!!!!!!!!!", str(e))
        conn.close()
        return []

    conn.close()
    return data

def plotClimatology(stations, cont):

    for id_cont in cont:
        for id_est in stations:
            data = getClimatology(id_est, id_cont)
            y = data['val']
            x = np.array([data['mes'][idx]*24 + int(str(data['hora'][idx])[0:2]) for idx in range(len(data))])
            sort_idx = np.argsort(x)
            plt.plot(x[sort_idx],y[sort_idx])

        plt.title('All stations cont: {}'.format(id_cont))
        plt.savefig('imgs/Climatologia_{}.png'.format(id_cont))
        plt.show()

def getDateRange(table, id_est, date_start_date, date_end):
    #For Posgresql only
    try:
        conn = psycopg2.connect("dbname='contingencia' user='soloread' host='132.248.8.238' password='SH3<t!4e'")
    except:
        print("Failed to connect to database")

    try:
        cur = conn.cursor();
        # In this case it reads from all the stations
        if all:
            sql_query = "SELECT * FROM {} " \
                        "WHERE fecha BETWEEN date '{}' AND date '{}'" \
                        " AND id_est = '{}' ORDER BY fecha".format(table, date_start_date, date_end, id_est)

        data = read_sql(sql_query, conn)

    except Exception as e:
        print("Something failed!!!!!!!!!", str(e))
        conn.close()
        return []

    conn.close()
    return data

def plotByDateRange(stations, cont, tables):
    month = np.arange(1,12)

    for c_m in month:
        start_date = '2017-{m:02d}-01'.format(m=c_m)
        end_date = '2017-{m:02d}-01'.format(m=c_m+1)
        for ii, table in enumerate(tables):
            for id_est in stations:
                print("{} -- {}".format(table, id_est))
                data = getDateRange(table, id_est, start_date, end_date)
                f = plt.figure( figsize=(40, 10) )
                y = data['val']
                x = data['fecha']
                sort_idx = np.argsort(x)
                plt.plot(x[sort_idx],y[sort_idx])
                plt.grid()
                plt.title('{}:{} From {} to {}'.format(table, id_est, start_date, end_date))
                plt.savefig('imgs/{}/ByRange_{}-{}_{}.png'.format(cont[ii], start_date, end_date, id_est))
                plt.show()

if __name__ == "__main__":

    stations = ['UAX', 'CUA', 'SFE', 'SJA', 'SAG', 'BJU', 'PED', 'TAH', 'IZT', 'CCA', 'ATI', 'UIZ', 'MGH', 'LPR', 'CAM', 'NEZ', 'FAC', 'AJM', 'TLA', 'CHO', 'MER', 'XAL']
    cont =   ['SO2', 'NOX', 'PMCO', 'PM10', 'PM2.5', 'NO', 'O3', 'CO', 'NO2']
    tables = ['cont_sodos', 'cont_nox', 'cont_pmco', 'cont_pmdiez','cont_pmdoscinco', 'cont_no', 'cont_otres', 'cont_co', 'cont_nodos' ]

    # plotClimatology(stations, tables)
    # plotByDateRange(stations, cont, tables)

    forecast_types = {1:'Climatologia', 2:'Normal', 3:'Meteorologia',4:'Datos Limpios'}
    months = np.arange(1,12)
    for id_est in stations:
        print("****** Getting data {} *******".format(id_est))
        # Meteorolgia using 3
        data = getData("'{}'".format(id_est), 2017, 3, all=False)
        print("****** Station {} *******".format(id_est))
        for c_m in months:
            print("Month {}".format(c_m))
            start_date = '2017-{m:02d}-01'.format(m=c_m)
            end_date= '2017-{m:02d}-01'.format(m=c_m+1)
            idx = (data['date_gt'] > start_date) & (data['date_gt'] < end_date)
            subset = data.ix[idx]

            print("Making plot....")
            f = plt.figure( figsize=(40, 10) )
            gt = subset['gt']
            fo = subset['fo']
            x = subset['date_gt']
            plt.plot(x,gt)
            plt.plot(x,fo)
            plt.grid()
            plt.title('{} Month {} From {}-{}'.format(id_est, c_m, start_date, end_date))
            plt.legend(['GT', 'FO'], loc='upper right')
            plt.savefig('imgs/Forecast/{}-{m:02d}_2017.png'.format(id_est, m=c_m))
            plt.show()
            print("Done ....")

