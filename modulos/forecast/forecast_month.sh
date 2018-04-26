#!/bin/bash

source ~/anaconda3/envs/tensorflow/bin/activate tensorflow
export LD_LIBRARY_PATH=/usr/local/cuda/lib64/
python /ServerScript/AirQualityModel/ContaminationForecast/lib/NetCDF/makeCsv.py
python /ServerScript/AirQualityModel/ContaminationForecast/lib/forecast_month.py O3
