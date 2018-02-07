# coding=utf-8
class ContIOTools:
    """ This class contains helper methods to manipulate dates, get names for tables and read files by year"""

    def __init__(self):
        """Constructor of the class"""

    def getCSVfiles(self,mypath,fromY, toY):
        years = range(fromY,toY+1)
        files = []
        for year in years:
            currFile = "%s/contaminantes_%s.csv" % (mypath,year)
            files.append(currFile)

        return files

    def getMeteoFiles(self,mypath,fromY, toY):
        years = range(fromY,toY+1)
        files = []
        for year in years:
            currFile = "%s/meteorología_%s.csv" % (mypath,year)
            files.append(currFile)

        return files

    def getMeteoTables(self):
        return ['met_tmp','met_rh','met_wsp','met_wdr','met_pba']

    def getTables(self):
        return ['cont_pmco','cont_pmdoscinco' ,'cont_nox' ,'cont_codos' ,'cont_co' ,'cont_nodos' ,'cont_no' ,'cont_otres' ,'cont_sodos', 'cont_pmdiez']

    def getContaminants(self):
        return ['pmco','pm2' ,'nox' ,'co2' ,'co' ,'no2' ,'no' ,'o3' ,'so2', 'pm10']

    def getMeteoParams(self):
        return ['tmp','rh','wsp','wdr','pba']

    def findTable(self,fileName):
        if "PM2.5" in fileName:
            return "cont_pmdoscinco"

        if "PM10" in fileName:
            return "cont_pmdiez"

        if "NOX" in fileName:
            return "cont_nox"

        if "CO2" in fileName:
            return "cont_codos"

        if "PMCO" in fileName:
            return "cont_pmco"

        if "CO" in fileName:
            return "cont_co"

        if "NO2" in fileName:
            return "cont_nodos"

        if "NO" in fileName:
            return "cont_no"

        if "O3" in fileName:
            return "cont_otres"

        if "SO2" in fileName:
            return "cont_sodos"

        if "TMP" in fileName:
            return "met_tmp"

        if "RH" in fileName:
            return "met_rh"

        if "WSP" in fileName:
            return "met_wsp"

        if "WDR" in fileName:
            return "met_wdr"

        if "PBA" in fileName:
            return "met_pba"


    def findDateFormat(self,fileName):
        "Obtains the date format"
        firstData = 11
        f = open(fileName)
        values = f.readlines()[11:]
        for line in values:
            allDate = (line.rstrip().split(',')[0]).split('/')
            #print allDate
            if int(allDate[0]) > 12:
                return "DD/MM/YYY/HH24"
                break
            else:
                if int(allDate[1]) > 12:
                    return "MM/DD/YYY/HH24"
                    break
