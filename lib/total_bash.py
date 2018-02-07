import auto as au
import testPrediction as tp
import configparser


def init():
    config = configparser.ConfigParser()
    # config.read('../modulos/training/confTraining.conf')
    config.read('confTraining.conf')
    # Datos postprocesados de la base de datos y de meteorologia
    datos = config.get('total_bash', 'datos')
    # Datos postprocesados de la base de datos y de meteorologia completos
    datosComp = config.get('total_bash', 'datosComp')
    # Las redes neuronales ya entrenadas
    train = config.get('total_bash', 'train')
    # Folders donde se van a almacenar las graficas
    graficas = config.get('total_bash', 'graficas')
    # Lista de estaciones que va a entrenar
    est = config.get('total_bash', 'est')
    # Fecha hasta donde se tomaran los datos para el entrenamiento
    fechaInicio = config.get('total_bash', 'fechaInicio')
    fechaFinal = config.get('total_bash', 'fechaFinal')
    contaminant = config.get('total_bash', 'contaminant')
    columnContaminant = config.get('total_bash', 'columnContaminant')
    option = config.get('total_bash', 'option')
    iteraciones = config.get('total_bash', 'iteraciones')
    num = len(contaminant)
    for xs in range(num):
        if option == 2:
            # tp.init(datos[0],datosComp[0],graficas[numEs],train[numEs])
            tp.init(datos[xs], datosComp[xs], graficas[xs], train[xs], contaminant[xs], columnContaminant[xs], fechaInicio, fechaFinal,est)
        elif option == 1:
            au.trainNeuralNetworks(est, datos[xs], train[xs], fechaFinal, contaminant[xs], iteraciones)


init()
