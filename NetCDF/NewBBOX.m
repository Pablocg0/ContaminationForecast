function [newVar,newLAT,newLON]=NewBBOX(currVar,LON,LAT,LONsize,LATsize,minlat,maxlat,minlon,maxlon)

%Escanea los vectores LAT y LONG hasta encontrar minlon,maxlon,minlat,maxlat y guarda
%sus posiciones correspondientes.

for i=1:LONsize
    if LON(i) == minlon  
        lon1=i;
        break
    elseif LON(i) > minlon
        lon1=i-1;
        break
    end
end 
   

for i=1:LONsize
    if LON(i) == maxlon   
        lon2=i;
        break
    elseif LON(i)>maxlon
        lon2=i;
        break
    end
end  
  
    
for j=1:LATsize
     if LAT(j) == minlat
         lat1=j;
         break
     elseif LAT(j) > minlat
         lat1=j-1;
         break
     end 
end 
    
    
for j=1:LATsize
    if LAT(j) == maxlat  
        lat2=j;
        break
    elseif LAT(j) > maxlat
         lat2=j;
        break
    end
end 

%Corta los vectores LAT y LON 
    newLAT=LAT(lat1:lat2);
    newLON=LON(lon1:lon2);
    
%Saca las dimensiones de las variables
info = whos('currVar');
sizeX = info.size;
VarSize = length(sizeX);

%De acuerdo a la dimension corta las variaables.
  
 if VarSize==2
    newVar=currVar(lon1:lon2,lat1:lat2);  
 elseif VarSize==3
     newVar=currVar(lon1:lon2,lat1:lat2,:);
      elseif VarSize==4
     newVar=currVar(lon1:lon2,lat1:lat2,:,:); 
 end
 
end



     
        
