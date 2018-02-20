#!/bin/bash

export LD_LIBRARY_PATH=/usr/local/cuda/lib64/
source ~/anaconda3/envs/tensorflow/bin/activate tensorflow
python /ServerScript/AirQualityModel/ContaminationForecast/lib/total_bash.py O3 cont_otres
python /ServerScript/AirQualityModel/ContaminationForecast/lib/total_bash.py PMCO cont_pmco
python /ServerScript/AirQualityModel/ContaminationForecast/lib/total_bash.py PM2.5 cont_pmdoscinco
python /ServerScript/AirQualityModel/ContaminationForecast/lib/total_bash.py NOX cont_nox
python /ServerScript/AirQualityModel/ContaminationForecast/lib/total_bash.py CO cont_co
python /ServerScript/AirQualityModel/ContaminationForecast/lib/total_bash.py NO2 cont_nodos
python /ServerScript/AirQualityModel/ContaminationForecast/lib/total_bash.py NO cont_no
python /ServerScript/AirQualityModel/ContaminationForecast/lib/total_bash.py SO2 cont_sodos
python /ServerScript/AirQualityModel/ContaminationForecast/lib/total_bash.py PM10 cont_pmdiez
