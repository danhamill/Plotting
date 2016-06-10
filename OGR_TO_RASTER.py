# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 19:33:49 2016

@author: dan
"""

from osgeo import ogr
from osgeo import gdal
import osgeo.osr as osr
from math import sqrt
import numpy as np

def readPoints(db_connect):  
    data1 = {}  
    xv=[]  
    yv=[]  
    values=[] 
    ds = ogr.Open(db_connect)  
    if ds is None:  
       raise Exception('Could not open ' + db_connect) 
    data = ds.ExecuteSQL("select the_geom from mosaic_2014_09 where sidescan_intensity <> 0 ORDER BY gid;")
    data2 = ds.ExecuteSQL("select sidescan_intensity from mosaic_2014_09 where sidescan_intensity <> 0 ORDER BY gid;")
    feature =data.GetNextFeature()
    feature2 = data2.GetNextFeature()
    
    while feature:
        geometry = feature.GetGeometryRef()  
        xv.append(geometry.GetX())  
        yv.append(geometry.GetY())  
        values.append(feature2.GetField("sidescan_intensity"))
        feature =data.GetNextFeature()
        feature2 = data2.GetNextFeature()
    
    extent = []
    extent.append(np.min(xv))
    extent.append(np.max(xv))
    extent.append(np.min(yv))
    extent.append(np.max(yv))
    extent = tuple(extent)
    
    proj = osr.SpatialReference()
    proj.ImportFromEPSG(26949)
     
  
    data1['extent'] = extent   
    data1['xv']=xv  
    data1['yv']=yv  
    data1['values']=values  
    data1['proj'] = proj  
    ds = None  
    return data1  
    
def CreateRaster(xv,yv,values,geotransform,xSize,ySize,power,smoothing,driverName,outFile):  
    #Transform geographic coordinates to pixels  
    for i in range(0,len(xv)):  
         xv[i] = (xv[i]-geotransform[0])/geotransform[1]  
    for i in range(0,len(yv)):  
         yv[i] = (yv[i]-geotransform[3])/geotransform[5]  
    #Creating the file  
    driver = gdal.GetDriverByName(driverName)
    ds = driver.Create( outFile, xSize, ySize, 1, gdal.GDT_Float32)  
#    srs = osr.SpatialReference()
#    srs.ImportFromEPSG(26949)
#    ds.SetProjection(srs.ExportToWkt()) 
    if proj is not None:  
        ds.SetProjection(proj.ExportToWkt()) 
    ds.SetGeoTransform(geotransform)  
    valuesGrid = np.zeros((ySize,xSize))  
    #Getting the interpolated values  
    for x in range(0,xSize):  
        for y in range(0,ySize):  
            valuesGrid[y][x] = pointValue(x,y,power,smoothing,xv,yv,values)  
    ds.GetRasterBand(1).WriteArray(valuesGrid)  
    del ds  
    return valuesGrid 
    
def pointValue(x,y,power,smoothing,xv,yv,values):  
    nominator=0  
    denominator=0  
    for i in range(0,len(values)):  
        dist = sqrt((x-xv[i])*(x-xv[i])+(y-yv[i])*(y-yv[i])+smoothing*smoothing);  
        #If the point is really close to one of the data points, return the data point value to avoid singularities  
        if(dist<0.0000000001):  
            return values[i]  
        nominator=nominator+(values[i]/pow(dist,power))  
        denominator=denominator+(1/pow(dist,power))  
    #Return NODATA if the denominator is zero  
    if denominator > 0:  
        value = nominator/denominator  
    else:  
        value = -9999  
    return value 

    
if  __name__ == '__main__':
    
    proj = None
    db_connect="PG:host=localhost dbname=reach_4a user=root port=9000 password=myPassword"
    data = readPoints(db_connect)
    
    xMin=data['extent'][0]
    xMax=data['extent'][1]
    yMin=data['extent'][2]
    yMax=data['extent'][3] 
    
    #Pixel size
    xSize=100  
    ySize=100
    
    #Build Geotransform
    geotransform=[]  
    geotransform.append(xMin)  
    geotransform.append((xMax-xMin)/xSize)  
    geotransform.append(0)  
    geotransform.append(yMax)  
    geotransform.append(0)  
    geotransform.append((yMin-yMax)/ySize) 
    
    driverName= 'GTiff'
    outFile = r'C:\workspace\Reach_4a\mosaic\test.tif'
    power =1
    smoothing=20    
    
    if proj is None:  
        proj = data['proj']
    ZI= CreateRaster(data['xv'],data['yv'],data['values'],geotransform,proj,xSize,ySize,power,smoothing,driverName,outFile) 
    
    
    #Debugging stuff
    proj = osr.SpatialReference()
    proj.ImportFromEPSG(26949)
    proj.ExportToWkt()
    xv=data['xv'] 
    yv=data['yv'] 
    values=data['values']
    ZI = CreateRaster(xv,yv,values,geotransform,proj,xSize,ySize,power,smoothing,driverName,outFile)
