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


ss_raster = r"C:\workspace\Merged_SS\window_analysis\raster\ss_10_raster.tif"
ds = gdal.Open(ss_raster)
data = ds.GetRasterBand(1).ReadAsArray()
data[data<=0] = np.nan
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

tex_raster = r"C:\workspace\Merged_SS\window_analysis\raster\tex_10_raster.tif"
ds = gdal.Open(tex_raster)
tex_data = ds.GetRasterBand(1).ReadAsArray()
tex_data[tex_data<=0] = np.nan
del ds

#######################################################################################################
                    
#######################################################################################################

ss_raster_40 = r"C:\workspace\Merged_SS\window_analysis\raster\ss_40_rasterclipped.tif"
ds = gdal.Open(ss_raster_40)
data_40 = ds.GetRasterBand(1).ReadAsArray()
data_40[data_40<=0] = np.nan

del ds

tex_raster_40 = r"C:\workspace\Merged_SS\window_analysis\raster\tex_40_rasterclipped.tif"
ds = gdal.Open(tex_raster_40)
tex_data_40 = ds.GetRasterBand(1).ReadAsArray()
tex_data_40[tex_data_40<=0] = np.nan
del ds

#######################################################################################################
                    
#######################################################################################################

ss_raster_80 = r"C:\workspace\Merged_SS\window_analysis\raster\ss_80_rasterclipped.tif"
ds = gdal.Open(ss_raster_80)
data_80 = ds.GetRasterBand(1).ReadAsArray()
data_80[data_80<=0] = np.nan
del ds

tex_raster_80 = r"C:\workspace\Merged_SS\window_analysis\raster\tex_80_rasterclipped.tif"
ds = gdal.Open(tex_raster_80)
tex_data_80 = ds.GetRasterBand(1).ReadAsArray()
tex_data_80[tex_data_80<=0] = np.nan
del ds

#######################################################################################################
                    
#######################################################################################################

ss_raster_160 = r"C:\workspace\Merged_SS\window_analysis\raster\ss_160_rasterclipped.tif"
ds = gdal.Open(ss_raster_160)
data_160 = ds.GetRasterBand(1).ReadAsArray()
data_160[data_160<=0] = np.nan
del ds

tex_raster_160 = r"C:\workspace\Merged_SS\window_analysis\raster\tex_160_rasterclipped.tif"
ds = gdal.Open(tex_raster_160)
tex_data_160 = ds.GetRasterBand(1).ReadAsArray()
tex_data_160[tex_data_160<=0] = np.nan
del ds
#######################################################################################################
                    
#######################################################################################################
# create a grid of xy coordinates in the original projection
xx, yy = np.mgrid[xmin:xmax+xres:xres, ymax+yres:ymin:yres]

trans =  pyproj.Proj(init="epsg:26949") 
glon, glat = trans(xx, yy, inverse=True)
#ortho_lon, ortho_lat = trans(ortho_x, ortho_y, inverse=True)
cs2cs_args = "epsg:26949"

# [left, right, bottom, top]
#extent=[np.min(glon)-0.0009, np.max(glon)+0.0009, np.min(glat)-0.0009, np.max(glat)+0.0009]
#ortho_extent_2plot = [np.min(ortho_lon)-0.0009, np.max(ortho_lon)+0.0009, np.min(ortho_lat)-0.0009, np.max(ortho_lat)+0.0009]
# Create the figure and basemap object


fig = plt.figure(figsize=(24,12))
ax = fig.add_subplot(1,5,1)
ax.set_title('10 square pixel')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
#im2 = m.imshow(np.flipud(plt.imread(raster)), extent = ortho_extent_2plot)
x,y = m.projtran(glon, glat)
ss_level=[0,2.5,5,7.5,10,12.5,15,17.5,20,22.5,25,27.5,30,32.5,35]
#tex_levels = [0,0.5,0.75,1.25,1.5,1.75,2,3]
im = m.contourf(x,y,data.T, cmap='Greys_r',levels=ss_level)
im2 = m.contourf(x, y, tex_data.T, alpha=0.4, cmap='YlOrRd')#levels=tex_levels
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
cax2 = divider.append_axes("right", size="5%", pad=0.3)
cbr = plt.colorbar(im, cax=cax)
cbr2 = plt.colorbar(im2,cax=cax2)

del glon, glat
# create a grid of xy coordinates in the original projection
#######################################################################################################
                    
#######################################################################################################

ss_raster_20 = r"C:\workspace\Merged_SS\window_analysis\raster\ss_20_rasterclipped.tif"
ds = gdal.Open(ss_raster_20)
data_20 = ds.GetRasterBand(1).ReadAsArray()
data_20[data_20<=0] = np.nan
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

tex_raster_20 = r"C:\workspace\Merged_SS\window_analysis\raster\tex_20_rasterclipped.tif"
ds = gdal.Open(tex_raster_20)
tex_data_20 = ds.GetRasterBand(1).ReadAsArray()
tex_data_20[tex_data_20<=0] = np.nan
del ds

##########################################################################################################
#########################################################################################################
xx, yy = np.mgrid[xmin:xmax+xres:xres, ymax+yres:ymin:yres]

trans =  pyproj.Proj(init="epsg:26949") 
glon, glat = trans(xx, yy, inverse=True)


ax1 = fig.add_subplot(1,5,2)
ax1.set_title('20 square pixel')
m1 = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
#im2 = m.imshow(np.flipud(plt.imread(raster)), extent = ortho_extent_2plot)
x,y = m1.projtran(glon, glat)
ss_level=[0,2.5,5,7.5,10,12.5,15,17.5,20,22.5,25,27.5,30,32.5,35]
#tex_levels = [0,0.5,0.75,1.25,1.5,1.75,2,3]
im = m1.contourf(x,y,data_20.T, cmap='Greys_r',levels=ss_level)
im2 = m1.contourf(x, y, tex_data_20.T, alpha=0.4, cmap='YlOrRd')#levels=tex_levels
divider = make_axes_locatable(ax1)
cax = divider.append_axes("right", size="5%", pad=0.1)
cax2 = divider.append_axes("right", size="5%", pad=0.3)
cbr = plt.colorbar(im, cax=cax)
cbr2 = plt.colorbar(im2,cax=cax2)

ax2 = fig.add_subplot(1,5,3)
ax2.set_title('40 square pixel')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
#im2 = m.imshow(np.flipud(plt.imread(raster)), extent = ortho_extent_2plot)
x,y = m.projtran(glon, glat)
ss_level=[0,2.5,5,7.5,10,12.5,15,17.5,20,22.5,25,27.5,30,32.5,35]
#tex_levels = [0,0.5,0.75,1.25,1.5,1.75,2,3]
#im = m.pcolormesh(x,y,data_40.T, cmap='Greys_r')
im = m.contourf(x,y,data_40.T, cmap='Greys_r',levels=ss_level)
im2 = m.contourf(x, y, tex_data_40.T, alpha=0.4, cmap='YlOrRd')#levels=tex_levels
divider = make_axes_locatable(ax2)
cax = divider.append_axes("right", size="5%", pad=0.1)
cax2 = divider.append_axes("right", size="5%", pad=0.3)
cbr = plt.colorbar(im, cax=cax)
cbr2 = plt.colorbar(im2,cax=cax2)


ax3 = fig.add_subplot(1,5,4)
ax3.set_title('80 square pixel')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
#im2 = m.imshow(np.flipud(plt.imread(raster)), extent = ortho_extent_2plot)
#x,y = m.projtran(glon, glat)
ss_level=[0,2.5,5,7.5,10,12.5,15,17.5,20,22.5,25,27.5,30,32.5,35]
#tex_levels = [0,0.5,0.75,1.25,1.5,1.75,2,3]
im = m.contourf(x,y,data_80.T, cmap='Greys_r',levels=ss_level)
im2 = m.contourf(x, y, tex_data_80.T, alpha=0.4, cmap='YlOrRd')#levels=tex_levels
divider = make_axes_locatable(ax3)
cax = divider.append_axes("right", size="5%", pad=0.1)
cax2 = divider.append_axes("right", size="5%", pad=0.3)
cbr = plt.colorbar(im, cax=cax)
cbr2 = plt.colorbar(im2,cax=cax2)
#
#
ax4 = fig.add_subplot(1,5,5)
ax4.set_title('160 square pixel')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
#im2 = m.imshow(np.flipud(plt.imread(raster)), extent = ortho_extent_2plot)
#x,y = m.projtran(glon, glat)
ss_level=[0,2.5,5,7.5,10,12.5,15,17.5,20,22.5,25,27.5,30,32.5,35]
#tex_levels = [0,0.5,0.75,1.25,1.5,1.75,2,3]
im = m.contourf(x,y,data_160.T, cmap='Greys_r',levels=ss_level)
im2 = m.contourf(x, y, tex_data_160.T, alpha=0.4, cmap='YlOrRd')#levels=tex_levels
divider = make_axes_locatable(ax4)
cax = divider.append_axes("right", size="5%", pad=0.1)
cax2 = divider.append_axes("right", size="5%", pad=0.3)
cbr = plt.colorbar(im, cax=cax)
cbr2 = plt.colorbar(im2,cax=cax2)
#plt.savefig(r"C:\workspace\Merged_SS\window_analysis\output\test1.png",dpi=1000)
plt.show()

del data, gt, proj

#def get_extent(raster):
#    '''
#    Function to obtain the extents of an ortho photo
#    '''
#    ds_ortho = gdal.Open(raster)
#    gt = ds_ortho.GetGeoTransform()
#    xres = gt[1]
#    yres = gt[5]
#    xmin = gt[0] + xres * 0.5
#    xmax = gt[0] + (xres * ds_ortho.RasterXSize) - xres * 0.5
#    ymin = gt[3] + (yres * ds_ortho.RasterYSize) + yres * 0.5
#    ymax = gt[3] - yres * 0.5
#    extent = [xmin,xmax,ymin,ymax]
#    ortho_x, ortho_y = np.mgrid[xmin:xmax+xres:xres, ymax+yres:ymin:yres]
#    del ds_ortho
#    return extent, ortho_x, ortho_y
#
#raster = r"C:\workspace\Plotting\orthophotos\61rorthophoto.tif"
#ortho_extent, ortho_x, ortho_y = get_extent(raster)

##import ss_raster
#ds = gdal.Open(r"C:\workspace\Merged_SS\window_analysis\raster\ss_10_rasterclipped.tif")
#data = ds.ReadAsArray()
#gt = ds.GetGeoTransform()
#proj = ds.GetProjection()
#xres = gt[1]
#yres = gt[5]
#
## get the edge coordinates and add half the resolution 
## to go to center coordinates
#xmin = gt[0] + xres * 0.5
#xmax = gt[0] + (xres * ds.RasterXSize) - xres * 0.5
#ymin = gt[3] + (yres * ds.RasterYSize) + yres * 0.5
#ymax = gt[3] - yres * 0.5
#extent = [xmin,xmax,ymin,ymax]
#del ds
#im2=plt.imshow(plt.imread(r"C:\workspace\Merged_SS\window_analysis\raster\ss_10_rasterclipped.tif"), extent = extent)
## plot the data (first layer)
#im1 = m.pcolormesh(x, y, data[0,:,:].T, cmap=plt.cm.jet)
#
## annotate
#m.drawcountries()
#m.drawcoastlines(linewidth=.5)
#
#plt.show()
#
