# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 10:13:54 2016

@author: dan
"""

from mpl_toolkits.basemap import Basemap
import gdal
import matplotlib.pyplot as plt
import numpy as np
import pyproj


ds = gdal.Open(r"C:\workspace\Plotting\orthophotos\61rorthophoto.tif")

data = ds.ReadAsArray()
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

# create a grid of xy coordinates in the original projection
xx, yy = np.mgrid[xmin:xmax+xres:xres, ymax+yres:ymin:yres]

trans =  pyproj.Proj(init="epsg:26949") 
glon, glat = trans(xx, yy, inverse=True)
cs2cs_args = "epsg:26949"

# [left, right, bottom, top]
extent=[np.min(glon)-0.0009, np.max(glon)+0.0009, np.min(glat)-0.0009, np.max(glat)+0.0009]
# Create the figure and basemap object
fig = plt.figure(figsize=(12, 6))
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
x,y = m.projtran(glon, glat)
im = plt.imshow(plt.imread(r"C:\workspace\Plotting\orthophotos\61rorthophoto.tif"),extent = extent)
plt.show()



# plot the data (first layer)
im1 = m.pcolormesh(x, y, data[0,:,:].T, cmap=plt.cm.jet)

# annotate
m.drawcountries()
m.drawcoastlines(linewidth=.5)

plt.show()

#plt.savefig('world.png',dpi=75)

## Create the projection objects for the convertion
## original (Albers)
#inproj = osr.SpatialReference()
#inproj.ImportFromWkt(proj)
#
## Get the target projection from the basemap object
##outproj = osr.SpatialReference()
##outproj.ImportFromProj4(m.proj4string)
#outproj = inproj
#
## Convert from source projection to basemap projection
#xx, yy = convertXY(xy_source, inproj, outproj)