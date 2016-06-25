# -*- coding: utf-8 -*-

from mpl_toolkits.basemap import Basemap
from joblib import cpu_count
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import psycopg2
import pyproj
from scipy.interpolate import griddata
from pyresample import geometry, kd_tree
from mpl_toolkits.axes_grid1 import make_axes_locatable


cs2cs_args = "epsg:26949"
trans =  pyproj.Proj(init=cs2cs_args)

def ss_plot():
    #Pandas method of importing data frame and getting extents
    db_connect="dbname='reach_4a' user='root'  host='localhost' port='9000'"
    conn = psycopg2.connect(db_connect)
    df = pd.read_sql_query('SELECT * from mb_may_2012_1m tt inner join (	SELECT s.easting, s.northing, s.texture, s.sidescan_intensity  FROM ss_2012_05 s) ss on tt.easting=ss.easting and tt.northing=ss.northing;', con=conn)
    minE = df['easting'].min()[0]
    maxE = df['easting'].max()[0]
    minN = df['northing'].min()[0]
    maxN = df['northing'].max()[0]
    conn.close()
    print 'Done Importing Data from Database'
    
    #Create grid for countourf plot
    res = 1
    grid_x, grid_y = np.meshgrid( np.arange(np.floor(minE), np.ceil(maxE), res), np.arange(np.floor(minN), np.ceil(maxN), res))
    grid_lon, grid_lat = trans(grid_x,grid_y,inverse=True)
    
    #Re-sampling procedure
    m_lon, m_lat = trans(df['easting'].values.flatten(), df['northing'].values.flatten(), inverse=True)
    orig_def = geometry.SwathDefinition(lons=m_lon, lats=m_lat)
    target_def = geometry.SwathDefinition(lons=grid_lon.flatten(), lats=grid_lat.flatten())
    print 'Now Resampling...'
    result = kd_tree.resample_nearest(orig_def, df['sidescan_intensity'].values.flatten(), target_def, radius_of_influence=1, fill_value=None, nprocs = cpu_count())
    print 'Done Resampling!!!' 
    
    #format side scan intensities grid for plotting
    gridded_result = np.reshape(result,np.shape(grid_lon))
    gridded_result = np.squeeze(gridded_result)
    gridded_result[np.isinf(gridded_result)] = np.nan
    gridded_result[gridded_result<=0] = np.nan
    grid2plot = np.ma.masked_invalid(gridded_result)
       
    
    print 'Now mapping...'
    #Create Figure
    fig = plt.figure(frameon=True)
    ax = plt.subplot(1,1,1)
    map = Basemap(projection='merc', epsg=cs2cs_args.split(':')[1], llcrnrlon=np.min(grid_lon)-0.0009, llcrnrlat=np.min(grid_lat)-0.0009,urcrnrlon=np.max(grid_lon)+0.0009, urcrnrlat=np.max(grid_lat)+0.0009)
    gx,gy = map.projtran(grid_lon,grid_lat)
    map.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='World_Imagery', xpixels=1000, ypixels=None, dpi=1200)
    im = map.pcolormesh(gx, gy, grid2plot, cmap='gray',vmin=0.1, vmax=30)
        
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    cbr = plt.colorbar(im, cax=cax)
    cbr.set_label('Sidescan Intensity [dBw]', size=8)
    for t in cbr.ax.get_yticklabels():
        t.set_fontsize(8)
    plt.savefig(r'C:\workspace\Texture_Classification\output\May2012_1m_sidescan_intensity.png')    
    
if __name__ == '__main__':
    ss_plot()