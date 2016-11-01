# -*- coding: utf-8 -*-
from osgeo import gdal
import osgeo.osr as osr
import numpy as np
from glob import glob
import pyproj
import os
import pandas as pd
from pyresample import geometry, kd_tree
from joblib import cpu_count


def readPoints(fIn, epsg_code):
    '''
    Reads analysis text file and returns a dictionary for use
    '''
    df = fIn
    df = df[df['texture'] > 9.9e-5]
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
    data1['ss']=df['texture']
    data1['proj'] = proj 
    del df
    return data1  
    
def CreateRaster(xv,yv,gridded_result,geotransform,proj,cols,rows,driverName,outFile):  
    '''
    Exports data to GTiff Raster
    '''
    gridded_result = np.squeeze(gridded_result)
    shp = np.shape(gridded_result)
    print 'Shape of squeezed array is %s' %(shp,)
    gridded_result[np.isinf(gridded_result)] = -99
    gridded_result[gridded_result>100] = -99
    driver = gdal.GetDriverByName(driverName)
    ds = driver.Create( outFile, cols, rows, 1, gdal.GDT_Float32)      
    if proj is not None:  
        ds.SetProjection(proj.ExportToWkt()) 
    ds.SetGeoTransform(geotransform)
    ss_band = ds.GetRasterBand(1)
    ss_band.WriteArray(gridded_result)
    ss_band.SetNoDataValue(-99)
    ss_band.FlushCache()
    ss_band.ComputeStatistics(False)
    del ds
        
def resample(orig_def, target_def, ss):
    '''
    Calculates Numpy Array for Raster Generation
    '''
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
    
    scan_list = glob(r"C:\workspace\Reach_4a\2014_09\R*")

    for scan in scan_list[6:7]:
        scan_name = scan.split('\\')[-1]
        date = scan.split('\\')[-2]
        glob_string = scan + os.sep + scan_name + 'x_y_c*'
        files = glob(glob_string)       
    
    
        #read all files into csv    
        for thing in files:
            df = pd.read_csv(thing, sep=' ', header = None, names = ['easting', 'northing','texture'])
            if thing == files[0]:
                out_df = df
            else:
                out_df = pd.concat([out_df,df]) 
                del df
                
        epsg_code=26949
        data = readPoints(out_df, epsg_code)
        del out_df
        print 'Done importing from the input file'
    
        #Extents for geotransform
        xMin, xMax, yMin, yMax = [i for i in data['extent']]
        
        res = 0.25
        
        #Resampling Section
        trans =  pyproj.Proj(init="epsg:26949")
        lon_in, lat_in = trans(data['e'].values,data['n'].values,inverse=True)
        orig_def = geometry.SwathDefinition(lons=lon_in.flatten(), lats=lat_in.flatten())
        
        grid_x, grid_y = np.meshgrid(np.arange(xMin, xMax, res), np.arange(yMin,yMax, res))
        lon_grid, lat_grid = trans(grid_x, grid_y, inverse=True)
        target_def = geometry.SwathDefinition(lons=lon_grid.flatten(), lats=lat_grid.flatten())
        
        #Build Numpy Array for imput to create Raster Function
        ss_grid_array = np.array(data['ss'])
    
        print 'Now Gridding...'
        ss_result = resample(orig_def,target_def,ss_grid_array)
        print 'Done Gridding!!!'
        
        ss_gridded_result = np.reshape(ss_result,np.shape(lon_grid))
        ss_gridded_result = np.flipud(ss_gridded_result)
        ss_gridded_result[ss_gridded_result<=0] = -99
    
        #Determine number of rows and columns in output raster
        cols, rows = get_raster_size(xMin,yMin,xMax,yMax,res,res)
        geotransform =[xMin,res,0,yMax,0,-res]
    
        #Input parameters for output raster    
        driverName= 'GTiff'    
        proj = data['proj']
        ss_outFile = r"C:\workspace\Merged_SS\raster"+ os.sep +'tex_' + date + '_' + scan_name + '_raster.tif'
        
        print 'Now Making Raster'
        CreateRaster(data['e'], data['n'], ss_gridded_result, geotransform, proj,cols,rows,driverName,ss_outFile) 
        print 'Sucssfully created %s' %(ss_outFile)
        del ss_gridded_result, ss_result, data, ss_grid_array
