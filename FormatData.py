import numpy as np
from sqlCont import SqlCont
from oztools import ContIOTools

startDate='2009/02/20';
endDate='2009/02/23';
oztool = ContIOTools()
contaminants = oztool.getContaminants();
tables_contaminants = oztool.getTables();
tables_contaminants.extend(oztool.getMeteoTables());
estations=['MER','TAX','TLA'];

#Auxiliary function to fill the ndarray
#Receives 3 parameters
#allData is the ndarray where the information will be store
#table is the ndarray where the information will be extracted
#column is the column in the allData
def completeTable(allData,table,column):
    cont = 0;
    for list in table:
        for x in list:
            allData[cont,column]= x
            cont= cont +1;
    return allData;


#function to extract information from the database
#startDate and endDate range of dates with which the values of the query are extracted
#estations set the stations to get the values
def readData(startDate, endDate, estations):
    sizeData = len(tables_contaminants)*len(estations)+1;
    conexion= SqlCont();
    conn = conexion.getPostgresConn();
    cur=conn.cursor();
    cons="""SELECT fecha FROM {0} WHERE id_est ='{1}' AND fecha >= '{2}' AND fecha <= '{3}';""".format(tables_contaminants[1],estations[0],startDate, endDate);
    cur.execute(cons);
    date= cur.fetchall();
    limit = len(date);
    allData = np.ones((limit,sizeData))*-1;
    tempData = np.array(date);
    cont = 1;
    for x in tables_contaminants:
        for y in estations:
            sql ="""SELECT val FROM {0} WHERE id_est = '{1}' AND fecha >= '{2}' AND fecha <= '{3}';""".format(x,y, startDate, endDate);
            cur.execute(sql);
            value = cur.fetchall();
            temValue =  np.array(value);
            tempAllData = completeTable(allData, temValue,cont)
            cont = cont +1;
            allData = tempAllData;
    conn.commit();
    cur.close();
    #print allData;
    return allData;

#readData(startDate,endDate,estations);


#function to extract information from the database
#estations set the stations to get the values
#contaminant
#delta number of hour that will add to the time in the consultation
def builClass(estation,contaminant,delta):
    contaminantV= oztool.findTable(contaminant);
    conexion = SqlCont();
    conn = conexion.getPostgresConn();
    cur= conn.cursor();
    sql="""SELECT fecha + interval '{0} hour' FROM {1} WHERE id_est ='{2}' AND fecha >= '{3}' AND fecha <= '{4}';""".format(delta,contaminantV,estation,startDate, endDate);
    cur.execute(sql);
    tempDates = cur.fetchall();
    size = len(tempDates);
    build = np.ones((size,2))*-1;
    dates = np.array(tempDates);
    cont = 0;
    for list in dates:
        for x in list:
            sql2 = """SELECT val FROM {0} WHERE id_est ='{1}' AND fecha ='{2}';""".format(contaminantV,estation,x);
            cur.execute(sql2);
            tempValues = cur.fetchall();
            values = np.array(tempValues);
            if len(values)!=0:
                build[cont,1] = values[0,0];
                cont=  cont +1;
            else:
                build[cont,1]= -1;
                cont = cont +1;
    conn.commit();
    cur.close();
    #print build;
    return build;

#builClass('TAX','NOX',36);
