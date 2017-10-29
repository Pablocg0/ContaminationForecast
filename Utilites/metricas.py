import numpy as np


def mape(real,obs):
    #real = np.array(real);
    #obs = np.array(obs);
    #err = np.mean(np.abs((obs -  real)/ obs)) * 100;
    err = np.sum(np.abs((obs -  real)/ np.abs(obs)));
    print(err)
    print(len(real))
    return  err*(100/len(real));

def uTheils(real, obs):
    n = len(real)
    sqError = np.square(obs -real).sum();
    error = np.sqrt((1/n) * sqError);
    obsError = np.sqrt((1/n) * np.square(obs).sum());
    realError = np.sqrt((1/n) * np.square(real).sum());
    return error / (obsError + realError);

def correla(real,obs):
    medReal = np.mean(real)
    medObs = np.mean(obs);
    cov = (np.sum(real*obs) / len(real)) - (medReal*medObs);
    desvReal =np.sqrt(np.mean(np.square(real))-(medReal*medReal));
    desvObs = np.sqrt(np.mean(np.square(obs))-(medObs*medObs));
    return cov / (desvReal*desvObs);

def agreement(real,obs):
    frac =  np.mean(np.square(obs - real))
    req = np.mean(np.abs(obs - np.mean(obs)) + np.abs(np.square(real - np.mean(real))));
    agrr = 1 - (frac / req)
    return agrr;

def metricas(real,obs,station):
    met = [];
    if len(real) == 0:
        met.append(station)
        met.append(0);
        met.append(0);
        met.append(0);
        met.append(0);
    else:
        met.append(station);
        met.append(mape(real,obs));
        met.append(uTheils(real,obs));
        met.append(correla(real,obs));
        met.append(agreement(real,obs));
    return met;
