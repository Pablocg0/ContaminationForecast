#!/bin/bash

source ~/anaconda3/envs/tensorflow/bin/activate tensorflow
#python /ServerScript/AirQualityModel/ContaminationForecast/lib/NetCDF/makeCsv.py || python /ServerScript/AirQualityModel/ContaminationForecast/lib/NetCDF/makeCsv.py
python /ServerScript/AirQualityModel/ContaminationForecast/lib/saveData.py

