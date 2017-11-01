
import auto as au
import testPrediction as tp

datos = ['data/DatosCC/','data/DatosCP/','data/DatosLP/','data/DatosLC/','data/DatosCPM/','data/DatosLPM/','data/DatosCCM/','data/DatosLCM/','data/DatosCPB/','data/DatosLPB/','data/DatosCCB/','data/DatosLCB/','data/DatosLC16/']
datosComp = ['data/DatosCC/','data/DatosCP/','data/DatosCP/','data/DatosCC/','data/DatosCPM/','data/DatosCPM/','data/DatosCCM/','data/DatosCCM/','data/DatosCPB/','data/DatosCPB/','data/DatosCCB/','data/DatosCCB/','data/DatosLC16/']
train = ['trainData/TrainCC/','trainData/TrainCP/','trainData/TrainLP/','trainData/TrainLC/','trainData/TrainCPM/','trainData/TrainLPM/','trainData/TrainCCM/','trainData/TrainLCM/','trainData/TrainCPB/','trainData/TrainLPB/','trainData/TrainCCB/','trainData/TrainLCB/','trainData/TrainGCM/']
graficas = ['Graficas/Predicciones/GraficasCC/','Graficas/Predicciones/GraficasCP/','Graficas/Predicciones/GraficasLP/','Graficas/Predicciones/GraficasLC/','Graficas/Predicciones/GraficasCPR/','Graficas/Predicciones/GraficasLPR/','Graficas/Predicciones/GraficasCCR/','Graficas/Predicciones/GraficasLCR/','Graficas/Predicciones/GraficasCPB/','Graficas/Predicciones/GraficasLPB/','Graficas/Predicciones/GraficasCCB/','Graficas/Predicciones/GraficasLCB/','Graficas/Predicciones/GraficasGCM/']
est =['AJM','MGH','CCA','SFE','UAX','CUA','NEZ','CAM','LPR','SJA','IZT','SAG','TAH','ATI','FAC','UIZ','MER','PED','TLA','XAL'];

op = 1;
numEs=11;
numE =3;
print(datos[numEs]);
if op == 1:
    #tp.init(datos[0],datosComp[0],graficas[numEs],train[numEs])
    tp.init(datos[numE],datosComp[numE],graficas[numEs],train[numEs])
elif op == 2:
    est1 =['CHO']
    est2 =['BJU']
    au.trainNeuralNetworks(est,datos[numE],train[numEs]);
    au.trainNeuralNetworks(est1,datos[numE],train[numEs]);
    au.trainNeuralNetworks(est2,datos[numE],train[numEs]);

