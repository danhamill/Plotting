from pyresample import geometry, kd_tree
from joblib import cpu_count
from glob import glob
import numpy as np
import pyproj
import os

trans =  pyproj.Proj(init="epsg:26949")


def right(s, amount):
    return s[-amount:]
    
def ascol( arr ):
   '''
   reshapes row matrix to be a column matrix (N,1).
   '''
   if len( arr.shape ) == 1: arr = arr.reshape( ( arr.shape[0], 1 ) )
   return arr 

def trythis(fOut,fIn,res):
    names = "Easting,Northing,sed5class"
    d = np.genfromtxt(fIn, dtype=float, delimiter =',', names=names)
    humlon, humlat = trans(d['Easting'],d['Northing'],inverse=True)
    orig_def = geometry.SwathDefinition(lons=humlon.flatten(), lats=humlat.flatten())
    res = res
    grid_x, grid_y = np.meshgrid( np.arange(np.floor(np.min(d['Easting'])), np.ceil(np.max(d['Easting'])), res), np.arange(np.floor(np.min(d['Northing'])), np.ceil(np.max(d['Northing'])), res) )
    longrid, latgrid = trans(grid_x, grid_y, inverse=True)
    target_def = geometry.SwathDefinition(lons=longrid.flatten(), lats=latgrid.flatten())
    result = kd_tree.resample_nearest(orig_def, d['sed5class'].flatten(), target_def, radius_of_influence=1, fill_value=None, nprocs = cpu_count()-2)
    
    del d
    
    gridded_result = np.reshape(result,np.shape(longrid))
    mask = gridded_result.mask==True
    with open(fOut, 'wb')as f:
        np.savetxt(f, np.hstack((ascol(grid_x[mask==False].flatten()),ascol(grid_y[mask==False].flatten()),ascol(gridded_result[mask==False].flatten()))),delimiter=' ', fmt="%8.6f %8.6f %1.6f")   
    f.close()
    del gridded_result, mask, result
    
if  __name__ == '__main__':
    fIn = r"C:\workspace\Reach_4a\Multibeam\mb_sed_class\may2014_mb6086r_sedclass\x_y_sedclass_dt_5class_25cm.xyz"
    fOut = r"C:\workspace\Reach_4a\Multibeam\mb_sed_class\output\may2014_10m.xyz"
    res = 10
    trythis(fOut,fIn,res)