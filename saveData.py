from Utilites.FormatData import FormatData as fd
from Utilites.Utilites import converToArray as ut
import pandas as df
import os
import numpy as np
from datetime import datetime

est =['AJM','ATI','BJU','CAM','CCA','CHO','CUA','FAC','IZT','LPR','MER','MGH','NEZ','PED','SAG','SFE','SJA','TAH','TLA','UAX','UIZ','XAL'];
startDate =['2015/01/01','2013/01/26','1992/11/09','2011/07/01','2014/08/01','2007/07/20','1994/01/02','1990/08/07','2007/07/20','2011/07/05','1986/11/01','2015/01/01','2011/07/27','1986/01/17','1986/02/20','2012/02/20','2011/07/01','1994/01/02','1986/11/01','2012/02/20','1990/05/16','1986/11/22'];
contaminant = 'O3';
endDate = '2017/02/01';

def saveData():
    """
    Function for the save data in the type file .csv
    """
    if not os.path.exists('data'): os.makedirs('data');
    if not os.path.exists('trainData'): os.makedirs('trainData');
    i=0;
    while i<=21:
        r = 'trainData/'+est[i];
        if not os.path.exists(r): os.makedirs(r);
        i+=1;
    i = 0;
    #we create the necesary folders to save the files in case of not existing
    while i <= 21:
        print(est[i]);
        nameD = est[i]+'_'+contaminant+'.csv';
        nameB = est[i]+'_'+contaminant+'_pred.csv';
        data = fd.readData(startDate[i],endDate,[est[i]],contaminant);
        build = fd.buildClass2(data,[est[i]],contaminant,24,startDate[i],endDate);
        print(data);
        data.to_csv('data/'+nameD, sep= '\t',encoding = 'utf-8');# save the data in file "data/[station_contaminant].csv"
        build.to_csv('data/'+nameB, sep= '\t',encoding = 'utf-8');# save the data in file "data/[station_contaminant_pred].csv]
        i += 1;


def maxAndMinValues(data,station,contaminant):
    """
    Function to obtain the maximun and minumum values and save them in a file
    :param data: DataFrame that contains the data from where the maximun ans minumum values will be extracted
    :type data: DataFrame
    :param station: name the station
    :type station : string
    :param contaminant: name the contaminant
    :type contaminant : string
    """
    nameD = station+'_'+contaminant+'_MaxMin'+'.csv';
    x_vals = data.values;
    x = x_vals.shape;
    columns = x[1];
    x_vals= x_vals[:,1:columns];
    minx = x_vals.min(axis=0);
    maxx = x_vals.max(axis=0);
    mixmax = df.DataFrame(minx , columns = ['MIN'],index=['pmco','pm2' ,'nox' ,'co2' ,'co' ,'no2' ,'no' ,'o3' ,'so2', 'pm10']);
    dMax = df.DataFrame(maxx, columns= ['MAX'],index=['pmco','pm2' ,'nox' ,'co2' ,'co' ,'no2' ,'no' ,'o3' ,'so2', 'pm10']);
    mixmax['MAX']= dMax;
    mixmax.to_csv('data/'+nameD, sep= '\t',encoding = 'utf-8');
    print(mixmax);


def separateDate(data):
    """
    Function to separate the date in year, month ,day and the function sine of each one of them
    :parama data: DataFrame that contains the dates
    :type data: DataFrame
    """
    dates = data['date'];
    lenght = len(dates);
    years = np.ones((lenght,1))*-1;
    sinYears = np.ones((lenght,1))*-1;
    months = np.ones((lenght,1))*-1;
    sinMonths = np.ones((lenght,1))*-1;
    days = np.ones((lenght,1))*-1;
    sinDays = np.ones((lenght,1))*-1;
    i  =0 ;
    for x in dates:
        d = datetime.strptime(x, "%Y-%m-%d")
        years[i] = d.year;
        sinYears[i]= np.sin(d.year);
        months[i] = d.month
        sinMonths[i] = np.sin(d.month)
        days[i] = d.day
        sinDays[i]= np.sin(d.day);
        i += 1;
    dataYear = df.DataFrame(years, columns= ['year'])
    data['year'] = dataYear
    dataSinYear = df.DataFrame(sinYears, columns= ['sinYear'])
    data['sinYear'] = dataSinYear
    dataMonths = df.DataFrame(months, columns= ['month'])
    data['month'] = dataMonths
    dataSinMonths = df.DataFrame(sinMonths, columns= ['sinMonth'])
    data['sinMonth'] = dataSinMonths
    dataDay = df.DataFrame(days, columns= ['day'])
    data['day'] = dataDay
    dataSinDay = df.DataFrame(sinDays, columns= ['sinDay'])
    data['sinDay'] = dataSinDay
    print(data);

def sep(data):
    falso =data['fecha']
    d = falso.values
    print(d);
    dates = df.DataFrame(falso, columns=['fecha', 'hora']);
    print(dates['fecha']);

contaminant = 'O3';
station = 'AJM'
name = station +'_'+contaminant;
data = df.read_csv('data/'+name+'.csv', delim_whitespace =True)
separateDate(data);
#maxAndMinValues(data,station,contaminant);
