# -*- coding: utf-8 -*-
import psycopg2
from osgeo import gdal
import osgeo.osr as osr
import numpy as np
import pyproj
import pandas as pd
from pyresample import geometry, kd_tree
from joblib import cpu_count
import sys

def readPoints(db_connect,epsg_code):
    '''
    Performs query on the database and returns a dictionary
    '''
    data1 = {}  
    try:
        conn = psycopg2.connect(db_connect)
    except:
        print 'Could Not connect to database'
        
    df = pd.read_sql_query('select easting, northing, texture, sidescan_intensity from mosaic_2014_09', con=conn)
    conn.close()
    extent = []
    extent.append(np.min(df['easting']))
    extent.append(np.max(df['easting']))
    extent.append(np.min(df['northing']))
    extent.append(np.max(df['northing']))
    extent = tuple(extent)
    proj = osr.SpatialReference()
    proj.ImportFromEPSG(epsg_code) 
    data1 = {}  
    data1['extent'] = extent   
    data1['e']=df['easting']
    data1['n']=df['northing']
    data1['ss']=df['sidescan_intensity']  
    data1['proj'] = proj 
    del df
    return data1  
    
    
def get_point_bounds(lon_in,lat_in):      
    min_lon = np.min(lon_in)
    min_lat = np.min(lat_in)
    max_lon = np.max(lon_in)
    max_lat = np.max(lat_in)    
    return min_lon, min_lat, max_lon, max_lat
    
def CreateRaster(xv,yv,gridded_result,geotransform,proj,cols,rows,driverName,outFile):  
    
    gridded_result[np.isinf(gridded_result)] = -99
    grid2plot = np.ma.masked_invalid(gridded_result)
    #Creating the file  
    success, inverse_geotransform = gdal.InvGeoTransform(geotransform)    
    driver = gdal.GetDriverByName(driverName)
    ds = driver.Create( outFile, cols, rows, 1, gdal.GDT_Float32)      
    if proj is not None:  
        ds.SetProjection(proj.ExportToWkt()) 
    ds.SetGeoTransform(geotransform)
    ds.GetRasterBand(1).WriteArray(grid2plot)
    ds.GetRasterBand(1).FlushCache()
    ds.GetRasterBand(1).ComputeStastics(False)
    del ds
        

def resample(orig_def, target_def, ss):
    result = kd_tree.resample_nearest(orig_def, ss, target_def, radius_of_influence=1, fill_value=None, nprocs = cpu_count()-1)
    return result
    

    
def get_raster_size(minx, miny, maxx, maxy, cell_width, cell_height):
    """
    Determine the number of rows/columns given the bounds of the point data and the desired cell size
    """
    cols = int((maxx - minx) / cell_width)
    rows = int((maxy - miny) / abs(cell_height))
    return cols, rows
    
if  __name__ == '__main__':
    
    #Data Import Section
    db_connect="dbname='reach_4a' user='root'  host='localhost' port='9000'"
    epsg_code=26949
    data = readPoints(db_connect,epsg_code)
    print 'Done importing from the database'
    
    #Extents for geotransform
    xMin, xMax, yMin, yMax = [i for i in data['extent']]
    
    res = 0.25
    
    #Pyproj method to find lat/lon from Import
    trans =  pyproj.Proj(init="epsg:26949")
    lon_in, lat_in = trans(data['e'].values,data['n'].values,inverse=True)
    orig_def = geometry.SwathDefinition(lons=lon_in.flatten(), lats=lat_in.flatten())
    
    grid_x, grid_y = np.meshgrid(np.arange(xMin, xMax, res), np.arange(yMin,yMax, res))
    lon_grid, lat_grid = trans(grid_x, grid_y, inverse=True)
    target_def = geometry.SwathDefinition(lons=lon_grid.flatten(), lats=lat_grid.flatten())
    
    #Build Numpy Array for imput to create Raster Function
    grid_array = np.array(data['ss'])
    print 'Now Gridding...'
    result = resample(orig_def,target_def,grid_array)
    print 'Done Gridding!!!'
    gridded_result = np.reshape(result,np.shape(lon_grid))
    
    #Determine number of rows and columns in output raster
    cols, rows = get_raster_size(xMin,yMin,xMax,yMax,res,res)
    geotransform =[xMin,res,0,yMax,0,-res]

    #Input parameters for output raster    
    driverName= 'GTiff'
    outFile = r'C:\workspace\Reach_4a\mosaic\test_sr.tif'
    power =1
    smoothing=20         
    proj = data['proj']
    
    print 'Now Making Raster'
    ZI= CreateRaster(data['e'], data['n'], gridded_result, geotransform, proj,cols,rows,driverName,outFile) 
    
#    #Debugging stuff
#    proj = osr.SpatialReference()
#    proj.ImportFromEPSG(26949)
#    proj.ExportToWkt()
#    xv=data['e'] 
#    yv=data['n'] 
#    values=data['ss']
#    ZI = CreateRaster(xv,yv,values,geotransform,proj,xSize,ySize,power,smoothing,driverName,outFile)
