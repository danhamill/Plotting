# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 10:13:54 2016

@author: dan
"""

from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import gdal
import matplotlib.pyplot as plt
import numpy as np
import pyproj

#General Settings
cs2cs_args = "epsg:26949"
ss_level=[0,2.5,5,7.5,10,12.5,15,17.5,20,22.5,25,27.5,30,32.5,35]
trans =  pyproj.Proj(init="epsg:26949") 


ss_raster_59 = r"C:\workspace\Merged_SS\raster\ss_2014_05_R01359_raster.tif"
ds = gdal.Open(ss_raster_59)
data_59 = ds.GetRasterBand(1).ReadAsArray()
data_59[data_59<=0] = np.nan
gt = ds.GetGeoTransform()
proj = ds.GetProjection()
 
# get the edge coordinates and add half the resolution to go to center coordinates
xres = gt[1]
yres = gt[5]
xmin = gt[0] + xres * 0.5
xmax = gt[0] + (xres * ds.RasterXSize) - xres * 0.5
ymin = gt[3] + (yres * ds.RasterYSize) + yres * 0.5
ymax = gt[3] - yres * 0.5

del ds

xx, yy = np.mgrid[xmin:xmax+xres:xres, ymax+yres:ymin:yres]

glon, glat = trans(xx, yy, inverse=True)

ss_raster_60 = r"C:\workspace\Merged_SS\raster\ss_2014_05_R01360_raster.tif"
ds = gdal.Open(ss_raster_60)
data_60 = ds.GetRasterBand(1).ReadAsArray()
data_60[data_60<=0] = np.nan
gt = ds.GetGeoTransform()
proj = ds.GetProjection()
 
# get the edge coordinates and add half the resolution to go to center coordinates
xres = gt[1]
yres = gt[5]
xmin = gt[0] + xres * 0.5
xmax = gt[0] + (xres * ds.RasterXSize) - xres * 0.5
ymin = gt[3] + (yres * ds.RasterYSize) + yres * 0.5
ymax = gt[3] - yres * 0.5
del ds

#Get grid of coordinates from raster
xx_1, yy_1 = np.mgrid[xmin:xmax+xres:xres, ymax+yres:ymin:yres]
trans =  pyproj.Proj(init="epsg:26949") 
glon_1, glat_1 = trans(xx_1, yy_1, inverse=True)

fig = plt.figure(figsize=(12,24))
plt.suptitle('May 2014')
ax = fig.add_subplot(1,3,1)
ax.set_title('R01359')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon_1 - 0.0007), 
            llcrnrlat=np.min(glat_1 - 0.0006),
            urcrnrlon=np.max(glon_1 + 0.0005), 
            urcrnrlat=np.max(glat_1 + 0.0006))
x,y = m.projtran(glon, glat)
m.wmsimage(server='http://grandcanyon.usgs.gov/arcgis/services/Imagery/ColoradoRiverImageryExplorer/MapServer/WmsServer?', 
              layers=['0'], xpixels=1000)
im = m.contourf(x, y, data_59.T, cmap='Greys_r',levels=ss_level)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
cbr = plt.colorbar(im,cax=cax)

ax_2 = fig.add_subplot(1,3,2)
ax_2.set_title('R01360')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon_1 - 0.0007), 
            llcrnrlat=np.min(glat_1 - 0.0006),
            urcrnrlon=np.max(glon_1 + 0.0005), 
            urcrnrlat=np.max(glat_1 + 0.0006))
x,y = m.projtran(glon_1, glat_1)
m.wmsimage(server='http://grandcanyon.usgs.gov/arcgis/services/Imagery/ColoradoRiverImageryExplorer/MapServer/WmsServer?', 
              layers=['0'], xpixels=1000)
im = m.contourf(x, y, data_60.T, cmap='Greys_r',levels=ss_level)
divider = make_axes_locatable(ax_2)
cax = divider.append_axes("right", size="5%", pad=0.1)
cbr = plt.colorbar(im,cax=cax)
#plt.suptitle('May 2015')

ax_3 = fig.add_subplot(1,3,3)
ax_3.set_title('R01359 & R01360')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon_1 - 0.0007), 
            llcrnrlat=np.min(glat_1 - 0.0006),
            urcrnrlon=np.max(glon_1 + 0.0005), 
            urcrnrlat=np.max(glat_1 + 0.0006))
x,y = m.projtran(glon, glat)
m.wmsimage(server='http://grandcanyon.usgs.gov/arcgis/services/Imagery/ColoradoRiverImageryExplorer/MapServer/WmsServer?', 
              layers=['0'], xpixels=1000)
im = m.contourf(x, y, data_59.T, cmap='Greys_r',levels=ss_level)
x,y = m.projtran(glon_1, glat_1)
im = m.contourf(x, y, data_60.T, cmap='Greys_r',levels=ss_level)
divider = make_axes_locatable(ax_3)
cax = divider.append_axes("right", size="5%", pad=0.1)
cbr = plt.colorbar(im,cax=cax)
plt.tight_layout()
plt.savefig(r"C:\workspace\Merged_SS\output\2014_05\Complete_Channel.png", dpi = 1000)



