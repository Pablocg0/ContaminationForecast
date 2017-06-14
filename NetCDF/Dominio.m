clear;
clc;

ncdisp('NewFile.nc')

%Seleccionar las variables que se desean cortar creando una celda.
%variables=input('Introduce las variables que deseas cortar en un arreglo de celda.')
variables={'velocity'};

%Guarda las variables Longitude y Latitude del archivo NetCDF en LON y LAT
%respectivamente.
LON=ncread('NewFile.nc','Longitude');
LAT=ncread('NewFile.nc','Latitude');

%Saca el tamaño de los vectores LON y LAT
LONsize=length(LON);
LATsize=length(LAT);

%Calcula min y max de LON y LAT
minLON=min(LON);
maxLON=max(LON);
minLAT=min(LAT);
maxLAT=max(LAT);

fprintf('El siguiente es el intervalo de latitudes disponible \n');
            minLAT,maxLAT
            
fprintf('El siguiente es el intervalo de longitudes disponible \n');
            minLON,maxLON

%Pide ingresar las latitudes y longitudes de interés
%minlat=input('Introduce la latitud mínima deseada  :     ');
%maxlat=input('Introduce la latitud máxima deseada  :     ');
%minlon=input('Introduce la longitud mínima deseada  :     ');
%maxlon=input('Introduce la longitud máxima deseada  :     ');


%Mínimo y máximo de latitud y longitud que se van a tomar para cortar las
%variables.
minlat=19
maxlat=20
minlon=-96
maxlon=-95

l=length(variables);

%Crea una celda que servirá para guadar las variables recortadas.
celda=cell(1,l);
var_cut=cell(1,l);
new_vars=cell(1,l);
for i=1:l
    var=char(cellstr(variables{i}));
    celda{i}=ncread('NewFile.nc',var);
    [newVar,newLAT,newLON] = NewBBOX(celda{i},LON,LAT,LONsize,LATsize,minlat,maxlat,minlon,maxlon);
    var_cut{i}=newVar; 
end

%  ----------- Normal steps for creating a new NetCDF file
display('---------------------------------');
NewFileName = 'NewFileVars.nc'; % Name of the file


% 1.- Create the file OPTS: 'CLOBBER' -> overwrite existing files
newf = netcdf.create( NewFileName, 'CLOBBER');

% 2.- Define dimensions
dimlon = netcdf.defDim(newf, 'newLON', length(newLON));
dimlat = netcdf.defDim(newf, 'newLAT', length(newLAT));

% 3.- Create variables ----------------
% 3.1.- Create dimension variables
varlon = netcdf.defVar(newf, 'Longitude', 'float', dimlon);
varlat = netcdf.defVar(newf, 'Latitude', 'float', dimlat);

for i=1:l
 new_vars{i}= netcdf.defVar(newf, 'Variables', 'float', [dimlon dimlat]);

netcdf.endDef(newf);% Important! We are finishing the definition of the file

% 3.2.- Add data into the variables
netcdf.putVar(newf, varlon, newLON);
netcdf.putVar(newf, varlat, newLAT);
netcdf.putVar(newf, new_vars{i}, var_cut{i});
end
% 5.- Close file
netcdf.close(newf);


% Check header of new file
ncdisp('NewFileVars.nc');
%Regresa la variable (newfile), el vector LONGITUDE y LATITUDE  cortados para el dominio de interés 
%[NewFileName]=ByBBox(filename,LON,LAT,lonSize,latSize,minlat,maxlat,minlon,maxlon)
%[newfile1,LATITUDE,LONGITUDE]=ByBBox(filename1,LON,LAT,lonSize,latSize,minlat,maxlat,minlon,maxlon)
%[newfile2,LATITUDE,LONGITUDE]=ByBBox(filename2,LON,LAT,lonSize,latSize,minlat,maxlat,minlon,maxlon)
