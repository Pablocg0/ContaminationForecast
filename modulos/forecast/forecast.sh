#!/bin/bash

source /home/olmozavala/anaconda3/bin/activate base
export LD_LIBRARY_PATH=/usr/local/cuda/lib64/
python /media/storageBK/AirQualityForecast/Scripts/ContaminationForecast/lib/automatic_System.py O3
python /media/storageBK/AirQualityForecast/Scripts/ContaminationForecast/lib/automatic_SystemKeras.py O3
#python /ServerScript/AirQualityModel/ContaminationForecast/lib/automatic_System.py PMCO
#python /ServerScript/AirQualityModel/ContaminationForecast/lib/automatic_System.py PM2.5
python /media/storageBK/AirQualityForecast/Scripts/ContaminationForecast/lib/automatic_System.py NOX
python /media/storageBK/AirQualityForecast/Scripts/ContaminationForecast/lib/automatic_System.py CO
#python /ServerScript/AirQualityModel/ContaminationForecast/lib/automatic_System.py NO2
#python /ServerScript/AirQualityModel/ContaminationForecast/lib/automatic_System.py NO
python /media/storageBK/AirQualityForecast/Scripts/ContaminationForecast/lib/automatic_System.py SO2
python /media/storageBK/AirQualityForecast/Scripts/ContaminationForecast/lib/automatic_System.py PM10
