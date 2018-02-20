import auto as au
import testPrediction as tp
import configparser


def init():
    config = configparser.ConfigParser()
    # config.read('confTraining.conf')
    config.read('/ServerScript/AirQualityModel/ContaminationForecast/modulos/training/confTraining.conf')
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
    option = int(config.get('total_bash', 'option'))
    iteraciones = int(config.get('total_bash', 'iteraciones'))
    est = est.split()
    contaminant = contaminant.split()
    columnContaminant = columnContaminant.split()
    #datos = datos.split()
    datosComp = datosComp.split()
    #train = train.split()
    graficas = graficas.split()
    num = len(contaminant)
    print(num)
    if option == 2:
        for xs in range(num):
            # tp.init(datos[0],datosComp[0],graficas[numEs],train[numEs])
            tp.init(datos[xs]+contaminant[xs]+'/', datosComp[xs]+contaminant[xs]+'/', graficas[xs], train[xs]+contaminant[xs]+'/', contaminant[xs], columnContaminant[xs], fechaInicio, fechaFinal,est)
    elif option == 1:
        for xs in range(num):
            au.trainNeuralNetworks(est, datos, train+contaminant[xs]+'/', fechaFinal, contaminant[xs], iteraciones)


init()
