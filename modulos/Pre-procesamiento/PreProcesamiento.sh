#!/bin/bash

source ~/anaconda3/envs/tensorflow/bin/activate tensorflow
python ../../lib/NetCDF/makeCsv.py || python ../../lib/NetCDF/makeCsv.py
#python ../../lib/saveData.py

