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
