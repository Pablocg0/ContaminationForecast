#!/bin/bash

source ~/anaconda3/envs/tensorflow/bin/activate tensorflow
export LD_LIBRARY_PATH=/usr/local/cuda/lib64/
python /ServerScript/AirQualityModel/ContaminationForecast/lib/automatic_System.py

