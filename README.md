# ContaminationForecast

# Neural network design for pollution prediction

## Pip dependency installation

### tensorflow


`pip installl tensorflow`

or

`pip installl tensorflow-gpu`

### pandas

`pip install pandas`


### sklearn

`pip install -U scikit-learn`

## Anaconda dependency installation

### tensorflow

 For the installation of tensorflow gpu visit:

 https://www.tensorflow.org/install/install_linux#InstallingAnaconda

 For tensorflow

 `conda install -c jjhelmus tensorflow=0.12.0rc0`

### pandas

`conda install -c anaconda pandas=0.20.1`

### sklearn

`conda install -c anaconda scikit-learn=0.18.1`

## System operation

### Data
1. Create data from Netcdf files

`NetCDF/makeCsv.py`

File involved:

   * `NetCDF/NewBBOX.py`
   * `NetCDF/Dominio.py`
2. Create holiday data

`Utilites/makeDayCsv.py`

File involved:

   * `Utilites/data.csv`
3.
