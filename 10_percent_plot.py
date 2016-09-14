# -*- coding: utf-8 -*-
"""
Created on Fri Sep 02 12:42:23 2016

@author: dan
"""
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import gdal
import matplotlib.pyplot as plt
import numpy as np
import pyproj

tex_raster = r"C:\workspace\Merged_SS\window_analysis\10_percent_shift\raster\tex_50_rasterclipped.tif"
ds = gdal.Open(tex_raster)
tex_data_50 = ds.GetRasterBand(1).ReadAsArray()
tex_data_50[tex_data_50<=0] = np.nan
tex_data_50[tex_data_50<=0] = np.nan
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

ss_raster = r"C:\workspace\Merged_SS\window_analysis\10_percent_shift\raster\ss_50_rasterclipped.tif"
ds = gdal.Open(ss_raster)
ss_data_50 = ds.GetRasterBand(1).ReadAsArray()
ss_data_50[ss_data_50<=0] = np.nan
del ds

tex_raster = r"C:\workspace\Merged_SS\window_analysis\10_percent_shift\raster\tex_70_rasterclipped.tif"
ds = gdal.Open(tex_raster)
tex_data_70 = ds.GetRasterBand(1).ReadAsArray()
tex_data_70[tex_data_70<=0] = np.nan
del ds

ss_raster = r"C:\workspace\Merged_SS\window_analysis\10_percent_shift\raster\ss_70_rasterclipped.tif"
ds = gdal.Open(ss_raster)
ss_data_70 = ds.GetRasterBand(1).ReadAsArray()
ss_data_70[ss_data_70<=0] = np.nan
del ds

tex_raster = r"C:\workspace\Merged_SS\window_analysis\10_percent_shift\raster\tex_80_rasterclipped.tif"
ds = gdal.Open(tex_raster)
tex_data_80 = ds.GetRasterBand(1).ReadAsArray()
tex_data_80[tex_data_80<=0] = np.nan
del ds

ss_raster = r"C:\workspace\Merged_SS\window_analysis\10_percent_shift\raster\ss_80_rasterclipped.tif"
ds = gdal.Open(tex_raster)
ss_data_80 = ds.GetRasterBand(1).ReadAsArray()
ss_data_80[ss_data_80<=0] = np.nan
del ds

tex_raster = r"C:\workspace\Merged_SS\window_analysis\10_percent_shift\raster\tex_120_rasterclipped.tif"
ds = gdal.Open(tex_raster)
tex_data_120 = ds.GetRasterBand(1).ReadAsArray()
tex_data_120[tex_data_120<=0] = np.nan
del ds

ss_raster = r"C:\workspace\Merged_SS\window_analysis\10_percent_shift\raster\ss_120_rasterclipped.tif"
ds = gdal.Open(tex_raster)
ss_data_120 = ds.GetRasterBand(1).ReadAsArray()
ss_data_120[ss_data_120<=0] = np.nan
del ds

tex_raster = r"C:\workspace\Merged_SS\window_analysis\10_percent_shift\raster\tex_160_rasterclipped.tif"
ds = gdal.Open(tex_raster)
tex_data_160 = ds.GetRasterBand(1).ReadAsArray()
tex_data_160[tex_data_160<=0] = np.nan
del ds

ss_raster = r"C:\workspace\Merged_SS\window_analysis\10_percent_shift\raster\ss_160_rasterclipped.tif"
ds = gdal.Open(tex_raster)
ss_data_160 = ds.GetRasterBand(1).ReadAsArray()
ss_data_160[ss_data_160<=0] = np.nan
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

tex_levels=[0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.60,0.65,0.70,0.75,0.80,0.85,
       0.90,0.95,1.0,1.05,1.1,1.15,1.2,1.25,1.3,1.35,1.4,1.45,1.5,1.55,1.6,1.65,1.7,1.75,
       1.8,1.85,1.9,1.95,2.0,2.05,2.1,2.15,2.2,2.25,2.3,2.35,2.4]
ss_level=[0,2.5,5,7.5,10,12.5,15,17.5,20,22.5,25,27.5,30,32.5,35]
       
fig = plt.figure(figsize=(12,24))
ax = fig.add_subplot(3,5,11)
ax.set_title('50 square pixel')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
x,y = m.projtran(glon, glat)
im = m.contourf(x,y,ss_data_50.T, cmap='Greys_r',levels=ss_level)
im2 = m.contourf(x, y, tex_data_50.T, alpha=0.4, cmap='YlOrRd')#levels=tex_levels
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
cax2 = divider.append_axes("right", size="5%", pad=0.3)
cbr = plt.colorbar(im, cax=cax)
cbr2 = plt.colorbar(im2,cax=cax2)

ax_1 = fig.add_subplot(3,5,6)
ax_1.set_title('50 square pixel')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
im = m.contourf(x, y, tex_data_50.T, alpha=0.4, cmap='YlOrRd')
divider = make_axes_locatable(ax_1)
cax = divider.append_axes("right", size="5%", pad=0.1)
cbr = plt.colorbar(im,cax=cax)

ax_2 = fig.add_subplot(3,5,1)
ax_2.set_title('50 square pixel')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
im = m.contourf(x, y, ss_data_50.T, cmap='Greys_r',levels=ss_level)
divider = make_axes_locatable(ax_2)
cax = divider.append_axes("right", size="5%", pad=0.1)
cbr = plt.colorbar(im,cax=cax)

ax1 = fig.add_subplot(3,5,12)
ax1.set_title('70 square pixel')
m1 = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))

x,y = m1.projtran(glon, glat)

im = m1.contourf(x,y,ss_data_70.T, cmap='Greys_r',levels=ss_level)
im2 = m1.contourf(x, y, tex_data_70.T, alpha=0.4, cmap='YlOrRd')#levels=tex_levels
divider = make_axes_locatable(ax1)
cax = divider.append_axes("right", size="5%", pad=0.1)
cax2 = divider.append_axes("right", size="5%", pad=0.3)
cbr = plt.colorbar(im, cax=cax)
cbr2 = plt.colorbar(im2,cax=cax2)

ax1_1 = fig.add_subplot(3,5,7)
ax1_1.set_title('70 square pixel')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
im = m.contourf(x, y, tex_data_70.T, alpha=0.4, cmap='YlOrRd')
divider = make_axes_locatable(ax1_1)
cax = divider.append_axes("right", size="5%", pad=0.1)
cbr = plt.colorbar(im,cax=cax)

ax1_2 = fig.add_subplot(3,5,2)
ax1_2.set_title('70 square pixel')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
im = m.contourf(x, y, ss_data_70.T, cmap='Greys_r',levels=ss_level)
divider = make_axes_locatable(ax1_2)
cax = divider.append_axes("right", size="5%", pad=0.1)
cbr = plt.colorbar(im,cax=cax)

ax2 = fig.add_subplot(3,5,13)
ax2.set_title('80 square pixel')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
x,y = m.projtran(glon, glat)
im = m.contourf(x, y, ss_data_50.T, cmap='Greys_r',levels=ss_level)
im2 = m.contourf(x, y, tex_data_80.T, alpha=0.4, cmap='YlOrRd')#levels=tex_levels
divider = make_axes_locatable(ax2)
cax = divider.append_axes("right", size="5%", pad=0.1)
cax2 = divider.append_axes("right", size="5%", pad=0.3)
cbr = plt.colorbar(im, cax=cax)
cbr2 = plt.colorbar(im2,cax=cax2)

ax2_1 = fig.add_subplot(3,5,8)
ax2_1.set_title('80 square pixel')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
im = m.contourf(x, y, tex_data_80.T, alpha=0.4, cmap='YlOrRd')
divider = make_axes_locatable(ax2_1)
cax = divider.append_axes("right", size="5%", pad=0.1)
cbr = plt.colorbar(im,cax=cax)

ax2_2 = fig.add_subplot(3,5,3)
ax2_2.set_title('80 square pixel')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
im = m.contourf(x, y, ss_data_50.T, cmap='Greys_r',levels=ss_level)
divider = make_axes_locatable(ax2_2)
cax = divider.append_axes("right", size="5%", pad=0.1)
cbr = plt.colorbar(im,cax=cax)

ax3 = fig.add_subplot(3,5,14)
ax3.set_title('120 square pixel')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
im = m.contourf(x,y,ss_data_50.T, cmap='Greys_r',levels=ss_level)
im2 = m.contourf(x, y, tex_data_120.T, alpha=0.4, cmap='YlOrRd')#levels=tex_levels
divider = make_axes_locatable(ax3)
cax = divider.append_axes("right", size="5%", pad=0.1)
cax2 = divider.append_axes("right", size="5%", pad=0.3)
cbr = plt.colorbar(im, cax=cax)
cbr2 = plt.colorbar(im2,cax=cax2)


ax3_1 = fig.add_subplot(3,5,9)
ax3_1.set_title('120 square pixel')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
im = m.contourf(x, y, tex_data_120.T, alpha=0.4, cmap='YlOrRd')
divider = make_axes_locatable(ax3_1)
cax = divider.append_axes("right", size="5%", pad=0.1)
cbr = plt.colorbar(im,cax=cax)

ax3_2 = fig.add_subplot(3,5,4)
ax3_2.set_title('120 square pixel')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
im = m.contourf(x, y, ss_data_50.T, cmap='Greys_r',levels=ss_level)
divider = make_axes_locatable(ax3_2)
cax = divider.append_axes("right", size="5%", pad=0.1)
cbr = plt.colorbar(im,cax=cax)

ax4 = fig.add_subplot(3,5,15)
ax4.set_title('160 square pixel')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
im = m.contourf(x,y,ss_data_50.T, cmap='Greys_r',levels=ss_level)
im2 = m.contourf(x, y, tex_data_160.T, alpha=0.4, cmap='YlOrRd')#levels=tex_levels
divider = make_axes_locatable(ax4)
cax = divider.append_axes("right", size="5%", pad=0.1)
cax2 = divider.append_axes("right", size="5%", pad=0.3)
cbr = plt.colorbar(im, cax=cax)
cbr2 = plt.colorbar(im2,cax=cax2)



ax4_1 = fig.add_subplot(3,5,10)
ax4_1.set_title('160 square pixel')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
im = m.contourf(x, y, tex_data_160.T, alpha=0.4, cmap='YlOrRd')
divider = make_axes_locatable(ax4_1)
cax = divider.append_axes("right", size="5%", pad=0.1)
cbr = plt.colorbar(im,cax=cax)

ax4_2 = fig.add_subplot(3,5,5)
ax4_2.set_title('160 square pixel')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
im = m.contourf(x, y, ss_data_50.T, cmap='Greys_r',levels=ss_level)
divider = make_axes_locatable(ax4_2)
cax = divider.append_axes("right", size="5%", pad=0.1)
cbr = plt.colorbar(im,cax=cax)
fig.tight_layout()
plt.savefig(r"C:\workspace\Merged_SS\window_analysis\10_percent_shift\output\ss_tex_overlay.png",dpi=1000)



