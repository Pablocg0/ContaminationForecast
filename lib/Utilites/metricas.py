import numpy as np


def mape(real,obs):
    """
    Function to take the metric MAPE

    :param real: actual value of the pollutant
    :type real: matrix float32
    :param obs: value of the pollutant prediction
    :type obs: matrix float32
    :return: MAPE
    """
    err = np.sum(np.abs((obs -  real)/ np.abs(obs)));
    return  err*(100/len(real));


def rmse(real, obs):
    """
    Function to take the metric RMSE

    :param real: actual value of the pollutant
    :type real: matrix float32
    :param obs: value of the pollutant prediction
    :type obs: matrix float32
    :return: RMSE
    """
    error = np.sqrt(np.mean((obs-real)**2))
    return error;


def uTheils(real, obs):
    """
    Function to take the metric uTheils

    :param real: actual value of the pollutant
    :type real: matrix float32
    :param obs: value of the pollutant prediction
    :type obs: matrix float32
    :return: uTheils
    """
    n = len(real)
    sqError = np.square(obs -real).sum();
    error = np.sqrt((1/n) * sqError);
    obsError = np.sqrt((1/n) * np.square(obs).sum());
    realError = np.sqrt((1/n) * np.square(real).sum());
    return error / (obsError + realError);

def correla(real,obs):
    """
    Function to take the metric Correlation index

    :param real: actual value of the pollutant
    :type real: matrix float32
    :param obs: value of the pollutant prediction
    :type obs: matrix float32
    :return: Correlation index
    """
    medReal = np.mean(real)
    medObs = np.mean(obs);
    cov = (np.sum(real*obs) / len(real)) - (medReal*medObs);
    desvReal =np.sqrt(np.mean(np.square(real))-(medReal*medReal));
    desvObs = np.sqrt(np.mean(np.square(obs))-(medObs*medObs));
    return cov / (desvReal*desvObs);

def agreement(real,obs):
    """
    Function to take the metric Agreement index

    :param real: actual value of the pollutant
    :type real:  matrix float32
    :param obs: value of the pollutant prediction
    :type obs: matrix float32
    :return: Agreement index
    """
    frac =  np.mean(np.square(obs - real))
    req = np.mean(np.abs(obs - np.mean(obs)) + np.abs(np.square(real - np.mean(real))));
    agrr = 1 - (frac / req)
    return agrr;

def metricas(real,obs,station):
    """
    Function to get the metrics of the forecast made by the neural network

    :param real: actual value of the pollutant
    :type real:  matrix float32
    :param obs: value of the pollutant prediction
    :type obs: matrix float32
    :return: DataFrame
    """
    met = [];
    if len(real) == 0:
        met.append(station)
        met.append(0);
        met.append(0);
        met.append(0);
        met.append(0);
        met.append(0)
    else:
        met.append(station);
        met.append(mape(real,obs));
        met.append(uTheils(real,obs));
        met.append(correla(real,obs));
        met.append(agreement(real,obs));
        met.append(rmse(real, obs));
    return met;
