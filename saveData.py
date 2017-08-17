from Utilites.FormatData import FormatData as fd
from Utilites.Utilites import converToArray as ut
from datetime import datetime, timedelta
import pandas as df
import os
import matplotlib.pyplot as plt
import numpy as np



contaminant = 'O3';
endDate = '2016/12/31';


def saveData(listEstations,startDate):
    """
    Function for the save data in the type file .csv
    """
    createFile();
    est = listEstations;
    tam = len(est) -1
    i = 0;
    while i <=tam:#21
        print(est[i]);
        print(startDate[i])
        nameDelta = 'cont_otres_'+ est[i]+'_delta';
        nameD = est[i]+'_'+contaminant+'.csv';
        nameB = est[i]+'_'+contaminant+'_pred.csv';
        tempData = fd.readData(startDate[i],endDate,[est[i]],contaminant);
        tempBuild = fd.buildClass2(tempData,[est[i]],contaminant,24,startDate[i],endDate);
        temAllData= tempData.dropna(axis=1, how='all');
        allD = temAllData.dropna(axis=0,how='any');
        allD = temAllData.fillna(value=-1);
        allD = allD.reset_index();
        allD= allD.drop(labels='index',axis=1);
        allData = allD.merge(tempBuild,how='left',on='fecha');
        build = df.DataFrame(allData['fecha'],columns=['fecha']);
        val = df.DataFrame(allData[nameDelta],columns=[nameDelta]);
        build[nameDelta]= val;
        data = allData.drop(labels=nameDelta, axis=1);
        data = data.reset_index();
        build = build.reset_index();
        #data = fd.readData(startDate[i],endDate,[est[i]],contaminant);
        #build = fd.buildClass2(data,[est[i]],contaminant,24,startDate[i],endDate);
        build = build.drop(labels='index',axis=1);
        data = data.drop(labels='index',axis=1);
        dataTemp = separateDate(data);
        dataTemp2 = unionData(dataTemp);
        maxAndMinValues(dataTemp2,est[i],contaminant)
        data = dataTemp2;
        build = filterData(data,build);
        data.to_csv('data/'+nameD,encoding = 'utf-8',index=False);# save the data in file "data/[station_contaminant].csv"
        build.to_csv('data/'+nameB,encoding = 'utf-8', index=False);# save the data in file "data/[station_contaminant_pred].csv]
        i += 1;

def saveData2(listEstations,startDate):
    """
    Function for the save data in the type file .csv
    """
    createFile();
    est = listEstations;
    tam = len(est) -1
    i = 0;
    while i <=tam:#21
        print(est[i]);
        print(startDate[i])
        nameDelta = 'cont_otres_'+ est[i]+'_delta';
        nameD = est[i]+'_'+contaminant+'.csv';
        nameB = est[i]+'_'+contaminant+'_pred.csv';
        tempData = fd.readData(startDate[i],endDate,[est[i]],contaminant);
        tempBuild = fd.buildClass2(tempData,[est[i]],contaminant,24,startDate[i],endDate);
        temAllData= tempData.dropna(axis=1, how='all');
        #allD = temAllData.dropna(axis=0,how='any');
        allD = temAllData.fillna(value=-1);
        allD = allD.reset_index();
        allD= allD.drop(labels='index',axis=1);
        allData = allD.merge(tempBuild,how='left',on='fecha');
        build = df.DataFrame(allData['fecha'],columns=['fecha']);
        val = df.DataFrame(allData[nameDelta],columns=[nameDelta]);
        build[nameDelta]= val;
        data = allData.drop(labels=nameDelta, axis=1);
        data = data.reset_index();
        build = build.reset_index();
        #data = fd.readData(startDate[i],endDate,[est[i]],contaminant);
        #build = fd.buildClass2(data,[est[i]],contaminant,24,startDate[i],endDate);
        build = build.drop(labels='index',axis=1);
        data = data.drop(labels='index',axis=1);
        dataTemp = separateDate(data);
        dataTemp2 = unionData(dataTemp);
        maxAndMinValues(dataTemp2,est[i],contaminant)
        data = dataTemp2;
        build = filterData(data,build);
        data.to_csv('data/'+nameD,encoding = 'utf-8',index=False);# save the data in file "data/[station_contaminant].csv"
        build.to_csv('data/'+nameB,encoding = 'utf-8', index=False);# save the data in file "data/[station_contaminant_pred].csv]
        i += 1;




def filterData(data,build):
    datesTemp = df.DataFrame(data['fecha'],columns=['fecha']);
    build = build.merge(datesTemp,how='right',on='fecha');
    return build;


def createFile():
    #we create the necesary folders to save the files in case of not existing
    est =['AJM','MGH','CCA','SFE','UAX','CUA','NEZ','CAM','LPR','SJA','CHO','IZT','SAG','TAH','ATI','FAC','UIZ','MER','PED','TLA','BJU','XAL'];
    if not os.path.exists('data'): os.makedirs('data');
    if not os.path.exists('trainData'): os.makedirs('trainData');
    i=0;
    while i<=21:#21
        r = 'trainData/'+est[i];
        if not os.path.exists(r): os.makedirs(r);
        i+=1;

def allSaveData():
    """
    Function for the save data in the type file .csv
    """
    nameD = 'allData'+'_'+contaminant+'.csv';
    nameB = 'allData'+'_'+contaminant+'_pred.csv';
    data = fd.readData(startDate[0],endDate,est,contaminant);
    build = fd.buildClass2(data,[est[0]],contaminant,24,startDate[0],endDate);
    print('listo')
    dataTemp = separateDate(data);
    maxAndMinValues(dataTemp,'allData',contaminant)
    data = dataTemp;
    print('listo2')
    data.to_csv('data/'+nameD,encoding = 'utf-8',index=False);# save the data in file "data/[station_contaminant].csv"
    build.to_csv('data/'+nameB,encoding = 'utf-8', index=False);# save the data in file "data/[station_contaminant_pred].csv]


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
    Index = data.columns;
    myIndex =Index.values
    myIndex = myIndex[1:]
    x_vals = data.values;
    x = x_vals.shape;
    columns = x[1];
    x_vals= x_vals[:,1:columns];
    minx = x_vals.min(axis=0)
    maxx = x_vals.max(axis=0);
    #myIndex = ['pmco','pm2' ,'nox' ,'co2' ,'co' ,'no2' ,'no' ,'o3' ,'so2', 'pm10','weekday','sinWeekday','year','month','sinMonths','day','sinDay'];
    mixmax = df.DataFrame(minx , columns = ['MIN'],index = myIndex);
    dMax = df.DataFrame(maxx, columns= ['MAX'],index=myIndex);
    mixmax['MAX']= dMax;
    mixmax.to_csv('data/'+nameD,encoding = 'utf-8');


def separateDate(data):
    """
    Function to separate the date in year, month ,day and the function sine of each one of them
    :parama data: DataFrame that contains the dates
    :type data: DataFrame
    """
    dates = data['fecha'];
    lenght = len(dates.index);
    years = np.ones((lenght,1))*-1;
    sinYears = np.ones((lenght,1))*-1;
    months = np.ones((lenght,1))*-1;
    sinMonths = np.ones((lenght,1))*-1;
    days = np.ones((lenght,1))*-1;
    sinDays = np.ones((lenght,1))*-1;
    wDay = np.ones((lenght,1))*-1;
    sinWday = np.ones((lenght,1))*-1;
    i  =0 ;
    for x in dates:
        d =x
        #d = datetime.strptime(x,"%Y-%m-%d %H:%M:%S")
        wD= weekday(d.year,d.month,d.day);
        wDay[i]=wD[0];
        sinWday[i]=wD[1];
        years[i] = d.year;
        #sinYears[i]= np.sin(d.year);
        months[i] = d.month
        sinMonths[i] =(1+np.sin(((d.month-1)/11)*(2*np.pi)))/2
        days[i] = d.day
        sinDays[i]= (1+np.sin(((d.day-1)/23)*(2*np.pi)))/2
        i += 1;
    weekD = df.DataFrame(wDay, columns= ['weekday'])
    data['weekday']= weekD;
    sinWeekD = df.DataFrame(sinWday, columns= ['sinWeekday'])
    data['sinWeekday']= sinWeekD;
    dataYear = df.DataFrame(years, columns= ['year'])
    data['year'] = dataYear
    #dataSinYear = df.DataFrame(sinYears, columns= ['sinYear'])print(data);
    #data['sinYear'] = dataSinYear
    dataMonths = df.DataFrame(months, columns= ['month'])
    data['month'] = dataMonths
    dataSinMonths = df.DataFrame(sinMonths, columns= ['sinMonth'])
    data['sinMonth'] = dataSinMonths
    dataDay = df.DataFrame(days, columns= ['day'])
    data['day'] = dataDay
    dataSinDay = df.DataFrame(sinDays, columns= ['sinDay'])
    data['sinDay'] = dataSinDay
    return data;


def weekday(year,month,day):
    """
    Function to take day of the week using the congruence of Zeller , 1 is Sunday
    :param year: year of the date
    :type year: int
    :param month: month of the date
    :type month: int
    :param day: day of the date
    :type day:int
    :return: int, 1 is Sunday
    """
    a = (14-month)/12;
    a = int(a);
    y = year-a;
    m = month+12*a-2;
    week = (day+y+int(y/4)-int(y/100)+int(y/400)+int((31*m)/12))%7;
    Week = week +1;
    sinWeek = (1+np.sin(((week-1)/7)*(2*np.pi)))/2
    return [week,sinWeek]

def convertDates(data):
    fecha = data['fecha'];
    data = data.drop(labels='fecha',axis=1);
    date = []
    for i in fecha:
        datef = datetime.strptime(i,'%Y-%m-%d %H:%M:%S');
        date.append(datef);
    dataTemp = df.DataFrame(date,columns = ['fecha']);
    data['fecha']= dataTemp;
    return data;

def unionData(data):
    """
    Function to join the data of the netcdf and the data of the pollutants
    :param data:pataFrame(minollutants data
    :type data: dataFrame
    :return: dataFrame
    """
    dataFestivos = df.read_csv('data/Festivos.csv')
    dataFestivos = dataFestivos.drop(labels='Unnamed: 0',axis=1);
    dataFestivos2 = convertDates(dataFestivos);
    data= data.merge(dataFestivos2, how = 'left', on='fecha');
    #variables=['Uat10','Vat10','PREC2'];
    variables=['U10','V10','RAINC'];
    netcdf = 'data/totalData/';
    for i in variables:
        netcdf += i +'_total.csv';
        dataNet = df.read_csv(netcdf);
        dataNet2 = convertDates(dataNet)
        data = data.merge(dataNet2,how='left',on='fecha');
        netcdf = 'data/totalData/';
    allD = data.dropna(axis=0,how='any');
    #allD = data.fillna(value=-1);
    allD = allD.reset_index();
    allD= allD.drop(labels='index',axis=1);
    return allD;


est =['AJM','MGH','CCA','SFE','UAX','CUA','NEZ','CAM','LPR','SJA','IZT','SAG','TAH','ATI','FAC','UIZ','MER','PED','TLA','XAL'];
startDate =['2015/01/01','2015/01/01','2014/08/01','2012/02/20','2012/02/20','2011/10/01','2011/07/27','2011/07/01','2011/07/01','2011/07/01','2007/07/20','1995/01/01','1995/01/01','1994/01/02','1993/01/01','1987/05/31','1986/01/16','1986/01/16','1986/01/15','1986/01/10'];
#startDate =['2015/01/01','2015/01/01','2014/08/01','2012/02/20','2012/02/20','2011/10/01','2011/07/27','2011/07/01','2011/07/01','2011/07/01','2007/07/20','2007/07/20','1995/01/01','1995/01/01','1994/01/02','1993/01/01','1987/05/31','1986/01/16','1986/01/16','1986/01/15','1986/01/12','1986/01/10'];
est1 =['CHO']
est2 =['BJU']
startDate1=['2007/07/20']
startDate2=['1986/01/12']
saveData(est,startDate);
saveData2(est1,startDate1)
saveData2(est2,startDate2)
#allSaveData();
