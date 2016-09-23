# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 11:10:05 2016

@author: dan
"""

from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import gdal
import matplotlib.pyplot as plt
import numpy as np
import pyproj
import pandas as pd


def assign_class(row):
    if row.sed5class == 1:
        return 'sand'
    if row.sed5class == 2:
        return 'sand/gravel'
    if row.sed5class == 3:
        return 'gravel'
    if row.sed5class == 4:
        return 'sand/rock'
    if row.sed5class == 5:
        return 'rock'
               
#Load Aub 13 mb_sedclass data
aug_sed_class_raster = r"C:\workspace\Reach_4a\Multibeam\mb_sed_class\aug13_mb_sedclass_proc_sept16\mb_sed5class_2013_08_raster.tif"
ds = gdal.Open(aug_sed_class_raster)
aug_sed_class = ds.GetRasterBand(1).ReadAsArray()
aug_sed_class[aug_sed_class<0]=np.nan
gt = ds.GetGeoTransform()
proj = ds.GetProjection()
 
xres = gt[1]
yres = gt[5]

xmin = gt[0] + xres * 0.5
xmax = gt[0] + (xres * ds.RasterXSize) - xres * 0.5
ymin = gt[3] + (yres * ds.RasterYSize) + yres * 0.5
ymax = gt[3] - yres * 0.5
extent = [xmin,xmax,ymin,ymax]
del ds

# create a grid of xy coordinates in the original projection
xx, yy = np.mgrid[xmin:xmax+xres:xres, ymax+yres:ymin:yres]
trans =  pyproj.Proj(init="epsg:26949") 
aug_13_lon, aug_13_lat = trans(xx, yy, inverse=True)
del xx, yy, xmin, xmax, ymin, ymax

#load masked data
mask = r"C:\workspace\Reach_4a\Multibeam\mb_sed_class\may_2014_sub_aug_13.tif"
ds = gdal.Open(mask)
mask_array = ds.GetRasterBand(1).ReadAsArray()
mask_array[mask_array<-11]=np.nan
gt = ds.GetGeoTransform()
proj = ds.GetProjection()

xres = gt[1]
yres = gt[5]

# get the edge coordinates and add half the resolution 
# to go to center coordinates
xmin = gt[0] + xres * 0.5
xmax = gt[0] + (xres * ds.RasterXSize) - xres * 0.5
ymin = gt[3] + (yres * ds.RasterYSize) + yres * 0.5
ymax = gt[3] - yres * 0.5
extent = [xmin,xmax,ymin,ymax]
del ds

xx, yy = np.mgrid[xmin:xmax+xres:xres, ymax+yres:ymin:yres]
glon, glat = trans(xx, yy, inverse=True)
del xx, yy, xmin, xmax, ymin, ymax

#Load May 2014 Data
may_sed_class_raster = r"C:\workspace\Reach_4a\Multibeam\mb_sed_class\may2014_mb6086r_sedclass\mb_sed5class_2014_05_raster.tif"
ds = gdal.Open(may_sed_class_raster)
may_sed_class = ds.GetRasterBand(1).ReadAsArray()
may_sed_class[may_sed_class<0]=np.nan
gt = ds.GetGeoTransform()
proj = ds.GetProjection()

xres = gt[1]
yres = gt[5]

# get the edge coordinates and add half the resolution 
# to go to center coordinates
xmin = gt[0] + xres * 0.5
xmax = gt[0] + (xres * ds.RasterXSize) - xres * 0.5
ymin = gt[3] + (yres * ds.RasterYSize) + yres * 0.5
ymax = gt[3] - yres * 0.5
extent = [xmin,xmax,ymin,ymax]
del ds

xx, yy = np.mgrid[xmin:xmax+xres:xres, ymax+yres:ymin:yres]
may_lon, may_lat = trans(xx, yy, inverse=True)
del xx, yy, xmin, xmax, ymin, ymax



#mask arrays to ensure only plotting concurrent cells
aug_sed_class[np.isnan(mask_array)]=np.nan
glon[np.isnan(mask_array.T)]=np.nan
glat[np.isnan(mask_array.T)]=np.nan

may_lon[np.min(may_lon)<np.nanmin(glon)] = np.nan
may_lon[np.max(may_lon)>np.nanmax(glon)] = np.nan
may_lat[np.min(may_lat)<np.nanmin(glat)] = np.nan
may_lat[np.max(may_lat)>np.nanmax(glat)] = np.nan
may_sed_class[np.isnan(may_lat.T)]= np.nan

print 'Now plotting August 2013 Acoutic sediment classifications...'
#Begin the plot
cs2cs_args = "epsg:26949"
fig = plt.figure(figsize=(15,12))
ax = plt.subplot2grid((5,2),(0, 0),rowspan=4)
ax.set_title('August 2013 Acousic \n Sediment Classifications')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.nanmin(glon)-0.0009, 
            llcrnrlat=np.nanmin(glat)-0.0006,
            urcrnrlon=np.nanmax(glon)+0.0009, 
            urcrnrlat=np.nanmax(glat)+0.0006)
m.wmsimage(server='http://grandcanyon.usgs.gov/arcgis/services/Imagery/ColoradoRiverImageryExplorer/MapServer/WmsServer?', layers=['0'], xpixels=1000)
x,y = m.projtran(aug_13_lon, aug_13_lat)
im = m.contourf(x,y,aug_sed_class.T, cmap='YlOrRd', levels=[0,1,2,3,4,5])
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
cbr = plt.colorbar(im, cax=cax)

print 'Now plotting May 2014 Acoustic Sediment Classifications...'
ax = plt.subplot2grid((5,2),(0, 1),rowspan=4)
ax.set_title('May 2014 Acousic \n Sediment Classifications')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.nanmin(may_lon)-0.0009, 
            llcrnrlat=np.nanmin(may_lat)-0.0006,
            urcrnrlon=np.nanmax(may_lon)+0.0009, 
            urcrnrlat=np.nanmax(may_lat)+0.0006)
m.wmsimage(server='http://grandcanyon.usgs.gov/arcgis/services/Imagery/ColoradoRiverImageryExplorer/MapServer/WmsServer?', layers=['0'], xpixels=1000)
x,y = m.projtran(may_lon, may_lat)
im = m.contourf(x,y,may_sed_class.T, cmap='YlOrRd', levels=[0,1,2,3,4,5])
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
cbr = plt.colorbar(im, cax=cax)

#convert arrays to histograms
aug_df = pd.DataFrame(aug_sed_class.flatten())
aug_df.rename(columns={0:'sed5class'}, inplace=True)
aug_df = aug_df.dropna()
aug_df['sed5name'] = aug_df.apply(lambda row: assign_class(row), axis=1)


may_df = pd.DataFrame(may_sed_class.flatten())
may_df.rename(columns={0:'sed5class'}, inplace=True)
may_df = may_df.dropna()
may_df['sed5name'] = may_df.apply(lambda row: assign_class(row), axis=1)

print 'Now plotting distributions...'
ax1 = plt.subplot2grid((5,2),(4, 0))
aug_df.groupby('sed5name').size().plot(kind='bar', ax=ax1,rot=45)
ax1.set_ylabel('Frequency')
ax1.set_xlabel('Substrate Type')


ax = plt.subplot2grid((5,2),(4, 1),sharey=ax1)
may_df.groupby('sed5name').size().plot(kind='bar', ax=ax,rot=45)
ax.set_ylabel('Frequency')
ax.set_xlabel('Substrate Type')

plt.tight_layout()
print 'Now Saving figure...'
plt.savefig(r"C:\workspace\Reach_4a\Multibeam\mb_sed_class\output\mb_aug_may_comparison.png",dpi=1000)
#plt.show()