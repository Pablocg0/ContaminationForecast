from netCDF4 import Dataset
import netCDF4 as nc4
import NewBBOX as ne
from os import listdir


def conver1D(array):
    array1D = [];
    total = [];
    i = 0
    for i in range(24):
        tempData = array[i]
        for x in tempData:
            for s in x:
                array1D.append(s);
        total.append(array1D)
    return total;

def makeCsv(net):
    variables=['Uat10','Vat10','PREC2'];

    LON = net.variables['Longitude'][:];
    LAT = net.variables['Latitude'][:];
    TIME = net.variables['Time'][:];

    LONsize = len(LON);
    LATsize = len(LAT);
    TIMEsize = len(TIME);

    minlat=19.4284700;
    maxlat=20;
    minlon=-99.1276600;
    maxlon=-98;

    celda = [];
    var_cut=[];
    for i in variables:
        var= net.variables[i][:]
        celda.append(var);
        result = ne.NewBBOX(var,LON,LAT,LONsize,LATsize,minlat,maxlat,minlon,maxlon);
        var_cut.append(result[0]);

    for x in var_cut:
        temp= conver1D(x);
        print(len(temp[0]));


def readFiles():
    for x in listdir('/home/pablo/DATA/')
    print(x);
