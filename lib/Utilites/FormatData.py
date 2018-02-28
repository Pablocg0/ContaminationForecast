'''
File name : FormatData.py
Author: Pablo Camacho Gonzalez
Python version: 3.6.4
Date last modified: 28/02/2018
'''

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from Utilites.sqlCont import SqlCont
from Utilites.oztools import ContIOTools
from datetime import datetime, timedelta

class FormatData(object):
    """docstring for FormatData"""

    def __init__(self, arg):
        """Constructor of the class"""

    def readData(startDate,endDate,estations,contaminant):
        """
        Function to extract information from the database.

        :param startDate: range of data wit wich the vaues of tue query are extracted.
        :type startDate: timedata
        :param endDate : range of data wit wich the vaues of tue query are extracted.
        :type endDate: timedata
        :param estations: set the stations to get the values.
        :type estations : list with the stations
        :return : allData  all data that was taken from the database.
        :rtype: DataFrame
        """
        oztool = ContIOTools();
        tables_contaminants = oztool.getTables();
        cont = oztool.findTable(contaminant)
        conexion = SqlCont();
        conn = conexion.getPostgresConn();
        cur=conn.cursor();
        #conexion for the database
        allData= pd.read_sql_query("""SELECT fecha FROM {0} WHERE id_est ='{1}' AND fecha >= '{2}' AND fecha <= '{3}' ORDER BY fecha ASC;""".format(cont,estations[0],startDate, endDate), conn);
        #query the dates in the gives range
        numberows = len(allData.index)#Numbers the data given by the previous query
        for x in estations:
            for y in tables_contaminants:
                name = y+'_'+x; #name the column in the DataFrame
                tempDataValues = pd.read_sql_query("""SELECT fecha, val  as {0} FROM {1} WHERE id_est = '{2}' AND fecha >= '{3}' AND fecha <= '{4}'ORDER BY fecha ASC;""".format(name,y,x, startDate, endDate),conn);
                #query the values in the gives rangefrom Utilites.FormatData import FormatData as fdfrom Utilites.FormatData import FormatData as fd
                if tempDataValues.empty:
                    #if the query is empty fill it will -1
                    #tempData = pd.DataFrame(np.ones((numberows,1))*-1,columns= [name]);
                    #allData[name]= tempData;
                    pass;
                elif not tempDataValues.empty:
                    allData = allData.merge(tempDataValues,how='left',on='fecha')
                    #allData[name]=tempDataValues[y+'_'+x.lower()];
        conn.commit();
        cur.close();
        #The connection to the database is closed
        #allData=allData.dropna(how = 'any');
        #return allData.fillna(value=-1);
        return allData;


    def buildClass(allData,estation,contaminant,delta):
        """
        Function so that every date in the allData table is added n hours and get the value that belongs to it.

        :param allData: is data extracted  the function readData
        :type allData: DataFrame.
        :param estation: station from wich the data will be taken.
        :type estation: string.
        :param contaminant: contaminant from wich the data will be taken.
        :type contaminant: string.
        :param delta : number of hours added to the original.
        :type delta: int, float
        :return: build
        :rtype: DataFrame
        """
        oztool = ContIOTools();
        conexion = SqlCont();
        conn = conexion.getPostgresConn();
        cur= conn.cursor();
        #conexion database
        tableContaminant = oztool.findTable(contaminant);# name the contaminant in the database
        fechas = allData['fecha']
        build= pd.DataFrame(fechas,columns=['fecha']);
        cont = len(build.index)-1;
        values = np.ones((cont+1,1))*-1;
        #building the DataFrame, the first column is the date
        x =0;
        for xv in estation:
            name = tableContaminant+'_'+ xv + '_delta';#name the column in the DataFrame
            while x <= cont :
                #Construction of the second column having the pollutant value
                time=build.ix[x,'fecha'];
                time = time + timedelta(hours=delta);#You add the delta to the date
                sql = """SELECT val FROM {0} WHERE id_est ='{1}' AND fecha ='{2}';""".format(tableContaminant,xv,time);
                cur.execute(sql);
                temp=cur.fetchall();
                tempValue = np.array(temp);
                if len(tempValue)!=0:
                    #If the query is empty it puts -1 in the value of the column
                    values[x,0]=tempValue[0,0];
                    x=x+1;
                else:
                    values[x,0]=np.nan;
                    x=x+1;
                temBuild= pd.DataFrame(values,columns=[name]);
            x=0;
            build[name]= temBuild;
        conn.commit();
        cur.close();
        #The connection to the database is closed
        build.dropna();
        return build.fillna(value=-1);


    def buildClass2(allData, estation, contaminant, delta, startDate, endDate):
        """
        Function so that every date in the allData table is added n hours and get the value that belongs to it.

        :param allData: is data extracted  the function readData
        :type allData: DataFrame.
        :param estation: station from wich the data will be taken.
        :type estation: string.
        :param contaminant: contaminant from wich the data will be taken.
        :type contaminant: string.
        :param delta : number of hours added to the original.
        :type delta: int, float
        :return: build
        :rtype: DataFrame
        """
        oztool = ContIOTools()
        conexion = SqlCont()
        conn = conexion.getPostgresConn()
        cur= conn.cursor();
        #conexion database
        tableContaminant = oztool.findTable(contaminant);# name the contaminant in the database
        fechas = allData['fecha']
        build= pd.DataFrame(fechas,columns=['fecha']);
        cont = len(build.index);
        values = np.ones((cont,1))*-1;
        start  = datetime.strptime(startDate,'%Y/%m/%d')
        end = datetime.strptime(endDate,'%Y/%m/%d')
        startDelta = start + timedelta(hours=delta);#You add the delta to the date
        endDelta = end + timedelta(hours=delta);#You add the delta to the date
        for xv in estation:
            name = tableContaminant+'_'+ xv + '_delta';#name the column in the DataFrame
            sql = pd.read_sql_query("""SELECT fecha, val FROM {0} WHERE id_est ='{1}' AND fecha >= '{2}' AND fecha <= '{3}' ORDER BY fecha ASC;""".format(tableContaminant,xv,startDelta,endDelta),conn);
            valPredic = sql['val'];
            if  valPredic.empty:
                temBuild= pd.DataFrame(values,columns=[name]);
                build[name]= temBuild;
            else:
                build[name]= valPredic;
        conn.commit();
        cur.close();
        #The connection to the database is closed
        return build;


    def get_forecast(nameContaminant, estacion):
        """
        function that brings from the database the last prediction saved

        :param nameContaminant: name of the pollutant
        :type nameContaminant: SyntaxWarning
        :param estacion: name of the weather station
        :type estacion:  String
        :return: DataFrame
        """
        oztool = ContIOTools()
        conexion =  SqlCont()
        conn = conexion.getPostgresConn()
        cur = conn.cursor()
        nameTable = nameContaminant
        tempDataValues = pd.read_sql_query("""SELECT * FROM {0} WHERE id_est = '{1}' ORDER BY fecha DESC LIMIT 1; """.format(nameTable,estacion),conn);
        conn.commit()
        cur.close()
        return tempDataValues


    def get_climatology(fechaInicio, fechaFinal, estacion):
        """
        function to bring the climatology data stored in the database

        :param fechaInicio: range of data wit wich the vaues of tue query are extracted.
        :type fechaInicio: datetime
        :param fechaFinal: range of data wit wich the vaues of tue query are extracted.
        :type fechaFinal: datetime
        :param estacion: set the stations to get the values
        :type estacion: String
        :return:  all data that was taken from the database.
        """
        month_init = fechaInicio.month
        month_fin = fechaFinal.month
        hour_init =  datetime.strptime(str(fechaInicio.hour)+ ':00:00', '%H:%M:%S' )
        hour_fin = datetime.strptime(str(fechaFinal.hour) + ':00:00', '%H:%M:%S')
        oztool = ContIOTools()
        conexion =  SqlCont()
        conn = conexion.getPostgresConn()
        cur = conn.cursor()
        tempData = pd.read_sql_query("""SELECT hora FROM climatologia WHERE id_est = '{0}' AND mes >= {1} AND mes <= {2} AND hora >= '{3}' AND hora <= '{4}' AND id_tabla = '{5}';""".format(estacion, month_init, month_fin, hour_init, hour_fin, 'cont_otres'), conn)
        contaminants = oztool.getTables()
        for xs in contaminants:
            temp = pd.read_sql_query("""SELECT hora, val FROM climatologia WHERE id_est = '{0}' AND mes >= {1} AND mes <= {2} AND hora >= '{3}' AND hora <= '{4}' AND id_tabla = '{5}';""".format(estacion, month_init, month_fin, hour_init, hour_fin, xs), conn)
            temp.rename(columns={'fecha':'fecha','val': xs+'_'+estacion.lower()}, inplace= True)
            if temp.empty:
                pass
            else:
                tempData = tempData.merge(temp, how='left', on='hora')
        conn.commit()
        cur.close()
        return tempData


    def saveData(estacion, fecha, Valor, contaminant):
        """
        function to save the prediction in the database

        :param estacion: name of the station to which the prediction belongs
        :type estacion: string
        :param fecha: prediction date
        :type fecha: date
        :param valor: prediction value
        :type valor: float32
        """
        table = contaminant
        oztool = ContIOTools();
        conexion = SqlCont();
        conn = conexion.getPostgresConn();
        cur= conn.cursor();
        #conexion database
        sql = """INSERT INTO {0}(fecha,val,id_est) VALUES (\'{1}\',{2},\'{3}\');""".format(table,fecha,Valor[0],estacion);
        cur.execute(sql)
        conn.commit()
        cur.close()
