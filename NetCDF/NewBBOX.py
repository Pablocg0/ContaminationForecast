def NewBBOX(currVar,LON,LAT,LONsize,LATsize,minlat,maxlat,minlon,maxlon):
    for i in range(LONsize):
        if LON[i] == minlon:
            lon1= i;
        elif LON[i] > minlon:
            lon1=i-1;

    for i in range(LONsize):
        if LON[i] == maxlon:
            lon2 = i;
        elif LON[i]>maxlon:
            lon2=i;

    for j in range(LATsize):
        if LAT[j] == minlat:
            lat1=j;
        elif LAT[j] > minlat:
            lat1= j-1;


    for j in range(LATsize):
        if LAT[j] == maxlat:
            lat2= j
        elif LAT[j] > maxlat:
            lat2= j;

    newLAT = LAT[lat1:lat2];
    newLON = LON[lon1:lon2];

    sizeX = currVar.ndim;
    VarSize = sizeX;
    newVar = 0;

    if VarSize == 2:
        newVar = currVar[lon1:lon2,lat1:lat2];
    elif VarSize == 3:
        newVar = currVar[lon1:lon2,lat1:lat2,:];
    elif VarSize == 4:
        newVar = currVar[lon1:lon2,lat1:lat2,:,:];

    return [newVar,newLAT,newLON];
