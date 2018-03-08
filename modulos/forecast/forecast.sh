#!/bin/bash

source ~/anaconda3/envs/tensorflow/bin/activate tensorflow
export LD_LIBRARY_PATH=/usr/local/cuda/lib64/
python /ServerScript/AirQualityModel/ContaminationForecast/lib/automatic_System.py O3
#python /ServerScript/AirQualityModel/ContaminationForecast/lib/automatic_System.py PMCO
#python /ServerScript/AirQualityModel/ContaminationForecast/lib/automatic_System.py PM2.5
python /ServerScript/AirQualityModel/ContaminationForecast/lib/automatic_System.py NOX
python /ServerScript/AirQualityModel/ContaminationForecast/lib/automatic_System.py CO
#python /ServerScript/AirQualityModel/ContaminationForecast/lib/automatic_System.py NO2
#python /ServerScript/AirQualityModel/ContaminationForecast/lib/automatic_System.py NO
python /ServerScript/AirQualityModel/ContaminationForecast/lib/automatic_System.py SO2
python /ServerScript/AirQualityModel/ContaminationForecast/lib/automatic_System.py PM10
