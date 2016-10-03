# -*- coding: utf-8 -*-
"""
Created on Sat Oct 01 11:55:16 2016

@author: dan
"""

from rasterstats import zonal_stats
import ogr
import pandas as pd


def keywithmaxval(d):
     """
     a) create a list of the dict's keys and values 
     b) return the key with the max value
     """  
     v=list(d.values())
     k=list(d.keys())
     return k[v.index(max(v))]


def mode_calc(buff_shp, sed5_raster):
    '''
    calculate the mode for each polygon
    return data frame
    '''
    stats = zonal_stats(buff_shp, sed5_raster, all_touched=True,
                    categorical=True)#add_stats={'mode':mymode}
    tt = [keywithmaxval(a) for a in stats]
    df = pd.DataFrame(tt)
    df = df.rename(columns={0:'mode'})
    return df
    
def return_shp_df(in_shp):
    '''
    Returns reasmpled sed5class file attributes as dataframe
    '''
    ds = ogr.Open(in_shp)
    lyr = ds.GetLayer(0)
    X,Y,sed5class=[],[],[]
    for row in lyr:
        X.append(row.X)
        Y.append(row.Y)
        sed5class.append(row.sed5class)
    lyr.ResetReading()
    del ds
    df = pd.DataFrame(columns=['X','Y','sed5class'])
    df['X']= X
    df['Y']= Y
    df['sed5class']= sed5class
    return df


sed5_raster = r"C:\workspace\Reach_4a\Multibeam\mb_sed_class\may2014_mb6086r_sedclass\mb_sed5class_2014_05_raster.tif"
in_shp = r"C:\workspace\Reach_4a\Multibeam\mb_sed_class\output\shapefiles\may2014_3m.shp"
buff_shp = r"C:\workspace\Reach_4a\Multibeam\mb_sed_class\output\shapefiles\may2014_3m_buff.shp"

tmp_df = return_shp_df(in_shp)
tmp2_df = mode_calc(buff_shp,sed5_raster)
tmp_df['mode']=tmp2_df['mode']