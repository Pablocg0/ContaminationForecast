#!/bin/bash
export LD_LIBRARY_PATH=/usr/local/cuda/lib64/
source /home/pablo/anaconda3/envs/py35/bin/activate py35
python /home/pablo/PollutionForecast/ContaminationForecast/automatic_System.py
