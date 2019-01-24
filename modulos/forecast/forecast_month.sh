#!/bin/bash

source /home/olmozavala/anaconda3/bin/activate base
export LD_LIBRARY_PATH=/usr/local/cuda/lib64/

python  /media/storageBK/AirQualityForecast/Scripts/ContaminationForecast/lib/NetCDF/makeCsv.py P
python  /media/storageBK/AirQualityForecast/Scripts/ContaminationForecast/lib/forecast_month.py O3
