#!/bin/bash

export LD_LIBRARY_PATH=/usr/local/cuda/lib64/
source ~/anaconda3/envs/tensorflow/bin/activate tensorflow
python /media/storageBK/AirQualityForecast/Scripts/ContaminationForecast/lib/total_bash.py O3 cont_otres TENSOR
python /media/storageBK/AirQualityForecast/Scripts/ContaminationForecast/lib/total_bash.py O3 cont_otres KERAS
#python /media/storageBK/AirQualityForecast/Scripts/ContaminationForecast/lib/total_bash.py PMCO cont_pmco
#python /media/storageBK/AirQualityForecast/Scripts/ContaminationForecast/lib/total_bash.py PM2.5 cont_pmdoscinco
python /media/storageBK/AirQualityForecast/Scripts/ContaminationForecast/lib/total_bash.py NOX cont_nox TENSOR
python /media/storageBK/AirQualityForecast/Scripts/ContaminationForecast/lib/total_bash.py CO cont_co TENSOR
#python /media/storageBK/AirQualityForecast/Scripts/ContaminationForecast/lib/total_bash.py NO2 cont_nodos
#python /media/storageBK/AirQualityForecast/Scripts/ContaminationForecast/lib/total_bash.py NO cont_no
python /media/storageBK/AirQualityForecast/Scripts/ContaminationForecast/lib/total_bash.py SO2 cont_sodos TENSOR
python /media/storageBK/AirQualityForecast/Scripts/ContaminationForecast/lib/total_bash.py PM10 cont_pmdiez TENSOR
