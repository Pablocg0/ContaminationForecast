# ContaminationForecast

This system is a Neural Network for pollution prediction of Mexico City

## Installation
### Pip dependency installation

Tensorflow

`pip installl tensorflow`

or

`pip installl tensorflow-gpu`

```
pip install pandas
pip install -U scikit-learn
pip install seaborn
```

### Anaconda dependency installation


```
conda install -c jjhelmus tensorflow=0.12.0rc0
conda install -c anaconda tensorflow-gpu
conda install -c anaconda pandas=0.20.1
conda install -c anaconda scikit-learn=0.18.1
conda install seaborn
```
## Quickstart
### Create data from Netcdf files
This code will generate CSV files from NetCDFs of a metheorological forecast form the IOA group at the UNAM. It should
also work for other WRF model outputs. 
`python NetCDF/makeCsv.py`

File involved:
   * `NetCDF/NewBBOX.py`
   * `NetCDF/Dominio.py`

### Create holiday data
This code will generate a CSV file containing the Mexican holidays with these numbers: 0 = laboral, 1 = oficial, 2 = sep
`python Utilites/makeDayCsv.py`

Input file:
   * `Data/Festivos.csv`
   
Output file:
   * `Data/Festivos2019Merged.csv`

### Creation of table with pollutant data and data created previously

`python saveData.py`

File involved:

   * `Utilites/FormatData.py`
   * `Utilites/Utilites.py`

 4. Neural network training

`auto.py`

File involved:

   * `NNSystem/neuralNetworkGpu.py`
   * `NNSystem/neuralNetwork.py`
   * `NNSystem/neuralNetworkGpuMax.py`

 5. Neural network prediction

`testPediction.py`

File involved:

   * `prediction.py`
