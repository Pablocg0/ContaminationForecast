import auto as au
import testPrediction as tp

datos = ['data/DatosCC/','data/DatosCP/','data/DatosLP/','data/DatosLC/','data/DatosCPM/','data/DatosLPM/','data/DatosCCM/','data/DatosLCM/','data/DatosCPB/','data/DatosLPB/','data/DatosCCB/','data/DatosLCB/','data/DatosLC16/']
datosComp = ['data/DatosCC/','data/DatosCP/','data/DatosCP/','data/DatosCC/','data/DatosCPM/','data/DatosCPM/','data/DatosCCM/','data/DatosCCM/','data/DatosCPB/','data/DatosCPB/','data/DatosCCB/','data/DatosCCB/','data/DatosLC16/']
train = ['trainData/TrainCC/','trainData/TrainCP/','trainData/TrainLP/','trainData/TrainCP/','trainData/TrainCPM/','trainData/TrainLPM/','trainData/TrainCCM/','trainData/TrainLCM/','trainData/TrainCPB/','trainData/TrainLPB/','trainData/TrainCCB/','trainData/TrainLCB/','trainData/TrainLC16/']
graficas = ['Graficas/Predicciones/GraficasCC/','Graficas/Predicciones/GraficasCP/','Graficas/Predicciones/GraficasLP/','Graficas/Predicciones/GraficasCP/','Graficas/Predicciones/GraficasCPR/','Graficas/Predicciones/GraficasLPR/','Graficas/Predicciones/GraficasCCR/','Graficas/Predicciones/GraficasLCR/','Graficas/Predicciones/GraficasCPB/','Graficas/Predicciones/GraficasLPB/','Graficas/Predicciones/GraficasCCB/','Graficas/Predicciones/GraficasLCB/','Graficas/Predicciones/GraficasLC16/']
est =['AJM','MGH','CCA','SFE','UAX','CUA','NEZ','CAM','LPR','SJA','IZT','SAG','TAH','ATI','FAC','UIZ','MER','PED','TLA','XAL'];

tp.init(datos[12],datosComp[12],graficas[12],train[12])

#for i in range(len(datos)):
#    print(datos[i])
est1 =['CHO']
est2 =['BJU']
#au.trainNeuralNetworks(est,datos[12],train[12]);
#au.trainNeuralNetworks(est1,datos[12],train[12]);
#au.trainNeuralNetworks(est2,datos[12],train[12]);
 #   tp.init(datos[i],datosComp[i],graficas[i],train[i]);
