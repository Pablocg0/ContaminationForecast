'''
File name : makeDayCsv.py
Author: Pablo Camacho Gonzalez
Python version: 3.6.4
Date last modified: 27/02/2018
'''



from datetime import datetime, timedelta
from pandas import concat
import pandas as df
import numpy as np

"""
Function to create csv file with the holidays from 1996 to 2016 from another cvs file
0 = laboral
1 = oficial
2 = sep
"""

def transformToProperFormat(input_file, output_file):
    """
    Function to create csv file with the holidays from 1996 to 2016 from another cvs file
    """
    print("Transforming file...")
    dataTemp =df.read_csv(input_file)
    #  Drops unnecessary columns
    dataTemp = dataTemp.drop(labels=['Unnamed: 0','Unnamed: 1','Unnamed: 23', 'Unnamed: 24'],axis=1)
    # Fill the table with the proper format
    data = fillTable(dataTemp)
    # Saves the file
    data.to_csv(output_file, encoding='utf-8', index=False)
    print("Done")

def fillTable(dataTemp):
    """
    Function to create the csv file with the holidays in the necessary format
    to add them to the other data of the neural network.

    :param dataTemp: Information from the original cvs
    :type dataTemp: DataFrame
    :return: DataFrame
    """
    # Read the columns
    column = dataTemp.columns
    firstYear = column[0]
    valuePerDay = dataTemp[firstYear]
    valuePerHour = repeat24hours(valuePerDay.values)
    listt = makeDates(firstYear)
    # Creates the output DF with the dates as index
    data = df.DataFrame(listt, columns=['fecha'])
    dataVal = df.DataFrame(valuePerHour, columns = ['valLab'])
    data['valLab'] = dataVal
    i = 1
    while i < len(column):
        firstYear = column[i]
        valuePerDay = dataTemp[firstYear]
        valuePerHour = repeat24hours(valuePerDay.values)
        listt = makeDates(firstYear)
        dataComp = df.DataFrame(listt, columns=['fecha'])
        dataVal = df.DataFrame(valuePerHour, columns = ['valLab'])
        dataComp['valLab']= dataVal
        data= df.concat([data,dataComp], axis=0)
        i += 1
    data = data.reset_index()
    data = data.drop(labels='index',axis=1)
    return data


def repeat24hours(year):
    """
    Function to put the firstYear of a given date in each hour of the day

    :param year: Value to repeat for 24 hours
    :type year: int
    :return : int array
    """
    completeYear = []
    for v in year:
        for i in range(24):
            completeYear.append(v)
    return completeYear


def makeDates(year):
    """
    This function creates all the 'hourly' dates for one year

    :param year: start year
    :type year: int
    :return datetime array
    """
    listDates = []
    date = year+'-01-01 00:00:00'
    dateInit = datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
    listDates.append(dateInit)
    val = int(year)
    while val == int(year):
        dateInit = dateInit + timedelta(hours = 1)
        val = dateInit.year
        listDates.append(dateInit)
    listDates.pop()
    return listDates

def makeHolidaysFromArray(year, official_holidays, input_file, output_file):
    '''
    Function th create the holidays of the year 2018
    :param year: For which year
    :param offHolidays:
    :return:
    '''
    data = df.read_csv(input_file)
    fecha = makeDates(year)
    f = df.DataFrame(fecha, columns=['fecha'])
    zeros = np.zeros(len(f.index))
    dZ = df.DataFrame(zeros, columns = ['valLab'])
    f['valLab'] = dZ
    for i in official_holidays:
        temp = f[(f.fecha >= F'{year}-'+i+' 00:00:00') & (f.fecha <= F'{year}-'+i+' 23:00:00')]
        f.loc[temp.index,'valLab'] = 1
    vac = f[(f.fecha >= F'{year}-01-02 00:00:00') & (f.fecha <= F'{year}-01-05 23:00:00')]
    f.loc[vac.index,'valLab'] = 2
    vac = f[(f.fecha >= F'{year}-03-26 00:00:00') & (f.fecha <= F'{year}-04-06 23:00:00')]
    f.loc[vac.index,'valLab'] = 2
    vac = f[(f.fecha >= F'{year}-06-25 00:00:00') & (f.fecha <= F'{year}-08-23 23:00:00')]
    f.loc[vac.index,'valLab'] = 2
    vac = f[(f.fecha >= F'{year}-12-24 00:00:00') & (f.fecha <= F'{year}-12-31 23:00:00')]
    f.loc[vac.index,'valLab'] = 2
    dataC = df.concat([data,f])
    dataC = dataC.reset_index(drop=True)
    dataC.to_csv(output_file, encoding='utf-8',index=False)


if __name__== '__main__':

    # Generate the proper CSV format from a list of holidays per year file
    input_file = '../../Data/FestivosByYear.csv'
    output_file = '../../Data/Festivos.csv'
    transformToProperFormat(input_file, output_file)

    # Makes the proper CSV for the year 2018, from the holidays
    year = '2018'
    input_file = '../../Data/Festivos.csv'
    output_file = F'../../Data/Festivos{year}Merged.csv'
    official_holidays=['01-01','01-06','02-05','03-19','04-01','05-01','09-16','11-19','12-01','12-25']
    makeHolidaysFromArray(year, official_holidays, input_file, output_file)
