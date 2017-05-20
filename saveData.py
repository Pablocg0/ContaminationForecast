from Utilites.FormatData import FormatData as fd
from Utilites.Utilites import converToArray as ut

est =['AJM','ATI','BJU','CAM','CCA','CHO','CUA','FAC','IZT','LPR','MER','MGH','NEZ','PED','SAG','SFE','SJA','TAH','TLA','UAX','UIZ','XAL'];
startDate =['2015/01/01','2013/01/26','1992/11/09','2011/07/01','2014/08/01','2007/07/20','1994/01/02','1990/08/07','2007/07/20','2011/07/05','1986/11/01','2015/01/01','2011/07/27','1986/01/17','1986/02/20','2012/02/20','2011/07/01','1994/01/02','1986/11/01','2012/02/20','1990/05/16','1986/11/22'];
contaminant = 'O3';
endDate = '2017/02/01';

i = 0;
while i <= 21:
    print(est[i]);
    nameD = est[i]+'_'+contaminant+'.csv';
    nameB = est[i]+'_'+contaminant+'_pred.csv';
    data = fd.readData(startDate[i],endDate,[est[i]],contaminant);
    build = fd.buildClass2(data,[est[i]],contaminant,24,startDate[i],endDate);
    print(data);
    data.to_csv('data/'+nameD, sep= '\t',encoding = 'utf-8');
    build.to_csv('data/'+nameB, sep= '\t',encoding = 'utf-8');
    i += 1;
