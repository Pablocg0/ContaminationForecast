#!/bin/bash

source ~/anaconda3/envs/tensorflow/bin/activate tensorflow
export LD_LIBRARY_PATH=/usr/local/cuda/lib64/
python /media/storageBK/AirQualityForecast/Scripts/ContaminationForecast/lib/forecastDate.py O3 cont_otres KERAS
python /media/storageBK/AirQualityForecast/Scripts/ContaminationForecast/lib/forecastDate.py O3 cont_otres TENSOR
#python /ServerScript/AirQualityModel/ContaminationForecast/lib/forecastDate.py PMCO cont_pmco
#python /ServerScript/AirQualityModel/ContaminationForecast/lib/forecastDate.py PM2.5 cont_pmdoscinco
#python /ServerScript/AirQualityModel/ContaminationForecast/lib/forecastDate.py NOX cont_nox
#python /ServerScript/AirQualityModel/ContaminationForecast/lib/forecastDate.py CO cont_co
#python /ServerScript/AirQualityModel/ContaminationForecast/lib/forecastDate.py NO2 cont_nodos
#python /ServerScript/AirQualityModel/ContaminationForecast/lib/forecastDate.py NO cont_no
#python /ServerScript/AirQualityModel/ContaminationForecast/lib/forecastDate.py SO2 cont_sodos
#python /ServerScript/AirQualityModel/ContaminationForecast/lib/forecastDate.py PM10 cont_pmdiez
