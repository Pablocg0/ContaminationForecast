import FormatData
import re
import numpy as np
from oztools import ContIOTools

def converToArray(alldata,contaminant):
    """
    Function that returns in a single column the columns have a specific name
    :param alldata: matrix with all the data of the database
    :type alldata: DataFrame
    :param contaminant: Name of pollutant to look for
    :type contaminant: string
    :return: column with all data of the pollutant
    :rtype; float32
    """
    oztool = ContIOTools()
    name = oztool.findTable(contaminant)
    c = np.ones((len(alldata.index),1));
    columns= alldata.columns;
    patron = re.compile(name+'_.*');
    index =0;
    for x in columns:
        if patron.match(x) != None:
            temp = alldata[x];
            for i in temp:
                if np.isnan(i):
                    c[index,0]= -1;
                    index = index +1;
                else:
                    c[index,0]= i;
                    index = index +1;
    return c;


def converToArray2(c):
    on = np.ones((c.shape[0],));
    index = 0;
    for x in c:
        if np.isnan(x):
            on[index]= -1;
            index = index +1;
        else:
            on[index]= x;
            index = index +1;
    return on;

def normalize_cols(m):
    """
    Function for the normalize column
    :param m: column to Normalize
    :type m : float32
    :return : standard column
    :rtype : float32
    """
    col_max = m.max(axis=0)
    col_min = m.min(axis=0)
    return (m-col_min) / (col_max - col_min)

def normalize_array(data):
    d = data;
    n = np.ones((d.shape));
    x = d.shape;
    column =x[1];
    i =0;
    while i <column:
        col_max = d[:,i].max(axis=0)
        col_min = d[:,i].min(axis=0)
        if col_max-col_min != 0.0:
            d[:,i]= normalize_cols(converToArray2(d[:,i]));
            i = i+1;
        else:
            i = i+1;
    return d;
