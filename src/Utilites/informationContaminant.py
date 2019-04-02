'''
File name : informationContaminant.py
Author: Pablo Camacho Gonzalez
Python version: 3.6.4
Date last modified: 27/02/2018
'''

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sqlCont import SqlCont
from oztools import ContIOTools
from datetime import datetime, timedelta


est = ['AJM', 'MGH', 'CCA', 'SFE', 'UAX', 'CUA', 'NEZ', 'CAM', 'LPR', 'SJA', 'IZT','SAG','TAH','ATI','FAC','UIZ','MER','PED','TLA','XAL','CHO','BJU']
oztool = ContIOTools()
tables = oztool.getTables()
print(tables)
conexion = SqlCont()
conn = conexion.getPostgresConn()
cur = conn.cursor()
for xs in tables:
    fecha = []
    nameEst = []
    print('[saveData_' + xs + ']')
    for ys in est:
        data = pd.read_sql_query("""SELECT fecha FROM {0} WHERE id_est='{1}' ORDER BY fecha ASC FETCH FIRST 1 ROW ONLY;""".format(xs , ys), conn)
        if not data.empty:
            ts = pd.to_datetime(str(data.iloc[0].values[0]))
            fechaString = ts.strftime('%Y-%m-%d')
            fecha.append(fechaString)
            nameEst.append(ys)
    print(fecha)
    print(nameEst)
conn.commit()
cur.close()
