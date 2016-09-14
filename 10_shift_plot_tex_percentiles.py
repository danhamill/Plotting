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
import pandas as pd

def convert_to_dataframe(array):
    out_name = pd.DataFrame(array.flatten())
    out_name = out_name.dropna(axis=0)
    return out_name
    
def get_bounds(df,lower,upper):
    lbound = df.describe().iloc[lower][0]
    ubound = df.describe().iloc[upper][0]
    return lbound, ubound
    
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

df_50 = convert_to_dataframe(tex_data_50)
df_70 = convert_to_dataframe(tex_data_70)
df_80 = convert_to_dataframe(tex_data_80)
df_120 = convert_to_dataframe(tex_data_120)
df_160 = convert_to_dataframe(tex_data_160)


#######################################################################################################
                    
#######################################################################################################
# create a grid of xy coordinates in the original projection
xx, yy = np.mgrid[xmin:xmax+xres:xres, ymax+yres:ymin:yres]

trans =  pyproj.Proj(init="epsg:26949") 
glon, glat = trans(xx, yy, inverse=True)
#ortho_lon, ortho_lat = trans(ortho_x, ortho_y, inverse=True)
cs2cs_args = "epsg:26949"

tex_levels=[0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.60,0.65,0.70,0.75,0.80,0.85,
       0.90,0.95,1.0,1.05,1.1,1.15,1.2,1.25,1.3,1.35,1.4,1.45,1.5,1.55,1.6,1.65,1.7,1.75,
       1.8,1.85,1.9,1.95,2.0,2.05,2.1,2.15,2.2,2.25,2.3,2.35,2.4]
ss_level=[0,2.5,5,7.5,10,12.5,15,17.5,20,22.5,25,27.5,30,32.5,35]

fig = plt.figure(figsize=(24,36))

ax = fig.add_subplot(3,5,1)
ax.set_title('50 square pixel \n 25th - 50th Percentile')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
x,y = m.projtran(glon, glat)
im = m.contourf(x,y,ss_data_50.T, cmap='Greys_r',levels=ss_level)
lbound, ubound = get_bounds(df_50,4,5)
tex_data_50[tex_data_50<lbound]= np.nan
tex_data_50[tex_data_50>ubound]= np.nan
im2 = m.contourf(x, y, tex_data_50.T, alpha=0.4, cmap='YlOrRd', levels=tex_levels)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
cax2 = divider.append_axes("right", size="5%", pad=0.3)
cbr = plt.colorbar(im, cax=cax)
cbr2 = plt.colorbar(im2,cax=cax2)

ax1 = fig.add_subplot(3,5,2)
ax1.set_title('70 square pixel \n 25th - 50th Percentile')
m1 = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
x,y = m1.projtran(glon, glat)
#tex_levels = [0,0.5,0.75,1.25,1.5,1.75,2,3]
im = m1.contourf(x,y,ss_data_70.T, cmap='Greys_r',levels=ss_level)
lbound, ubound = get_bounds(df_70,4,5)
tex_data_70[tex_data_70<lbound]= np.nan
tex_data_70[tex_data_70>ubound]= np.nan
im2 = m1.contourf(x, y, tex_data_70.T, alpha=0.4, cmap='YlOrRd', levels=tex_levels)
divider = make_axes_locatable(ax1)
cax = divider.append_axes("right", size="5%", pad=0.1)
cax2 = divider.append_axes("right", size="5%", pad=0.3)
cbr = plt.colorbar(im, cax=cax)
cbr2 = plt.colorbar(im2,cax=cax2)

ax2 = fig.add_subplot(3,5,3)
ax2.set_title('80 square pixel \n 25th - 50th Percentile')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))

x,y = m.projtran(glon, glat)
im = m.contourf(x,y,ss_data_50.T, cmap='Greys_r',levels=ss_level)
lbound, ubound = get_bounds(df_80,4,5)
tex_data_80[tex_data_80<lbound]= np.nan
tex_data_80[tex_data_80>ubound]= np.nan
im2 = m.contourf(x, y, tex_data_80.T, alpha=0.4, cmap='YlOrRd',levels=tex_levels)
divider = make_axes_locatable(ax2)
cax = divider.append_axes("right", size="5%", pad=0.1)
cax2 = divider.append_axes("right", size="5%", pad=0.3)
cbr = plt.colorbar(im, cax=cax)
cbr2 = plt.colorbar(im2,cax=cax2)


ax3 = fig.add_subplot(3,5,4)
ax3.set_title('120 square pixel \n 25th - 50th Percentile')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
im = m.contourf(x,y,ss_data_50.T, cmap='Greys_r',levels=ss_level)
lbound, ubound = get_bounds(df_120,4,5)
tex_data_120[tex_data_120<lbound]= np.nan
tex_data_120[tex_data_120>ubound]= np.nan
im2 = m.contourf(x, y, tex_data_120.T, alpha=0.4, cmap='YlOrRd', levels=tex_levels)
divider = make_axes_locatable(ax3)
cax = divider.append_axes("right", size="5%", pad=0.1)
cax2 = divider.append_axes("right", size="5%", pad=0.3)
cbr = plt.colorbar(im, cax=cax)
cbr2 = plt.colorbar(im2,cax=cax2)
#
#
ax4 = fig.add_subplot(3,5,5)
ax4.set_title('160 square pixel:25th - 50th Percentile')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))

im = m.contourf(x,y,ss_data_50.T, cmap='Greys_r',levels=ss_level)
lbound, ubound = get_bounds(df_160, 4,5)
tex_data_160[tex_data_160<lbound]= np.nan
tex_data_160[tex_data_160>ubound]= np.nan
im2 = m.contourf(x, y, tex_data_160.T, alpha=0.4, cmap='YlOrRd', levels=tex_levels)
divider = make_axes_locatable(ax4)
cax = divider.append_axes("right", size="5%", pad=0.1)
cax2 = divider.append_axes("right", size="5%", pad=0.3)
cbr = plt.colorbar(im, cax=cax)
cbr2 = plt.colorbar(im2,cax=cax2)

##################Row 2
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

df_50 = convert_to_dataframe(tex_data_50)
df_70 = convert_to_dataframe(tex_data_70)
df_80 = convert_to_dataframe(tex_data_80)
df_120 = convert_to_dataframe(tex_data_120)
df_160 = convert_to_dataframe(tex_data_160)

ax = fig.add_subplot(3,5,6)
ax.set_title('50 square pixel \n 50th - 75th Percentile')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
x,y = m.projtran(glon, glat)
im = m.contourf(x,y,ss_data_50.T, cmap='Greys_r',levels=ss_level)
lbound, ubound = get_bounds(df_50,5,6)
tex_data_50[tex_data_50<lbound]= np.nan
tex_data_50[tex_data_50>ubound]= np.nan
im2 = m.contourf(x, y, tex_data_50.T, alpha=0.4, cmap='YlOrRd', levels=tex_levels)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
cax2 = divider.append_axes("right", size="5%", pad=0.3)
cbr = plt.colorbar(im, cax=cax)
cbr2 = plt.colorbar(im2,cax=cax2)

ax1 = fig.add_subplot(3,5,7)
ax1.set_title('70 square pixel \n 50th - 75th Percentile')
m1 = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
x,y = m1.projtran(glon, glat)
im = m1.contourf(x,y,ss_data_70.T, cmap='Greys_r',levels=ss_level)
lbound, ubound = get_bounds(df_70,5,6)
tex_data_70[tex_data_70<lbound]= np.nan
tex_data_70[tex_data_70>ubound]= np.nan
im2 = m1.contourf(x, y, tex_data_70.T, alpha=0.4, cmap='YlOrRd', levels=tex_levels)
divider = make_axes_locatable(ax1)
cax = divider.append_axes("right", size="5%", pad=0.1)
cax2 = divider.append_axes("right", size="5%", pad=0.3)
cbr = plt.colorbar(im, cax=cax)
cbr2 = plt.colorbar(im2,cax=cax2)

ax2 = fig.add_subplot(3,5,8)
ax2.set_title('80 square pixel:50th - 75th Percentile')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))

x,y = m.projtran(glon, glat)
im = m.contourf(x,y,ss_data_50.T, cmap='Greys_r',levels=ss_level)
lbound, ubound = get_bounds(df_80,5,6)
tex_data_80[tex_data_80<lbound]= np.nan
tex_data_80[tex_data_80>ubound]= np.nan
im2 = m.contourf(x, y, tex_data_80.T, alpha=0.4, cmap='YlOrRd',levels=tex_levels)
divider = make_axes_locatable(ax2)
cax = divider.append_axes("right", size="5%", pad=0.1)
cax2 = divider.append_axes("right", size="5%", pad=0.3)
cbr = plt.colorbar(im, cax=cax)
cbr2 = plt.colorbar(im2,cax=cax2)


ax3 = fig.add_subplot(3,5,9)
ax3.set_title('120 square pixel \n 50th - 75th Percentile')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
im = m.contourf(x,y,ss_data_50.T, cmap='Greys_r',levels=ss_level)
lbound, ubound = get_bounds(df_120,5,6)
tex_data_120[tex_data_120<lbound]= np.nan
tex_data_120[tex_data_120>ubound]= np.nan
im2 = m.contourf(x, y, tex_data_120.T, alpha=0.4, cmap='YlOrRd', levels=tex_levels)
divider = make_axes_locatable(ax3)
cax = divider.append_axes("right", size="5%", pad=0.1)
cax2 = divider.append_axes("right", size="5%", pad=0.3)
cbr = plt.colorbar(im, cax=cax)
cbr2 = plt.colorbar(im2,cax=cax2)
#
#
ax4 = fig.add_subplot(3,5,10)
ax4.set_title('160 square pixel \n 50th - 75th Percentile')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
im = m.contourf(x,y,ss_data_50.T, cmap='Greys_r',levels=ss_level)
lbound, ubound = get_bounds(df_160, 6, 7)
tex_data_160[tex_data_160<lbound]= np.nan
tex_data_160[tex_data_160>ubound]= np.nan
im2 = m.contourf(x, y, tex_data_160.T, alpha=0.4, cmap='YlOrRd', levels=tex_levels)
divider = make_axes_locatable(ax4)
cax = divider.append_axes("right", size="5%", pad=0.1)
cax2 = divider.append_axes("right", size="5%", pad=0.3)
cbr = plt.colorbar(im, cax=cax)
cbr2 = plt.colorbar(im2,cax=cax2)

##################Row 3
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

df_50 = convert_to_dataframe(tex_data_50)
df_70 = convert_to_dataframe(tex_data_70)
df_80 = convert_to_dataframe(tex_data_80)
df_120 = convert_to_dataframe(tex_data_120)
df_160 = convert_to_dataframe(tex_data_160)

ax = fig.add_subplot(3,5,11)
ax.set_title('50 square pixel \n 75th - 100th Percentile')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
x,y = m.projtran(glon, glat)
im = m.contourf(x,y,ss_data_50.T, cmap='Greys_r',levels=ss_level)
lbound, ubound = get_bounds(df_50,6,7)
tex_data_50[tex_data_50<lbound]= np.nan
tex_data_50[tex_data_50>ubound]= np.nan
im2 = m.contourf(x, y, tex_data_50.T, alpha=0.4, cmap='YlOrRd', levels=tex_levels)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
cax2 = divider.append_axes("right", size="5%", pad=0.3)
cbr = plt.colorbar(im, cax=cax)
cbr2 = plt.colorbar(im2,cax=cax2)

ax1 = fig.add_subplot(3,5,12)
ax1.set_title('70 square pixel \n 75th - 100th Percentile')
m1 = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
x,y = m1.projtran(glon, glat)
im = m1.contourf(x,y,ss_data_70.T, cmap='Greys_r',levels=ss_level)
lbound, ubound = get_bounds(df_70,6,7)
tex_data_70[tex_data_70<lbound]= np.nan
tex_data_70[tex_data_70>ubound]= np.nan
im2 = m1.contourf(x, y, tex_data_70.T, alpha=0.4, cmap='YlOrRd', levels=tex_levels)
divider = make_axes_locatable(ax1)
cax = divider.append_axes("right", size="5%", pad=0.1)
cax2 = divider.append_axes("right", size="5%", pad=0.3)
cbr = plt.colorbar(im, cax=cax)
cbr2 = plt.colorbar(im2,cax=cax2)

ax2 = fig.add_subplot(3,5,13)
ax2.set_title('80 square pixel:75th - 100th Percentile')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))

x,y = m.projtran(glon, glat)
im = m.contourf(x,y,ss_data_50.T, cmap='Greys_r',levels=ss_level)
lbound, ubound = get_bounds(df_80,6,7)
tex_data_80[tex_data_80<lbound]= np.nan
tex_data_80[tex_data_80>ubound]= np.nan
im2 = m.contourf(x, y, tex_data_80.T, alpha=0.4, cmap='YlOrRd',levels=tex_levels)
divider = make_axes_locatable(ax2)
cax = divider.append_axes("right", size="5%", pad=0.1)
cax2 = divider.append_axes("right", size="5%", pad=0.3)
cbr = plt.colorbar(im, cax=cax)
cbr2 = plt.colorbar(im2,cax=cax2)


ax3 = fig.add_subplot(3,5,14)
ax3.set_title('120 square pixel \n 75th - 100th Percentile')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
im = m.contourf(x,y,ss_data_50.T, cmap='Greys_r',levels=ss_level)
lbound, ubound = get_bounds(df_120,6,7)
tex_data_120[tex_data_120<lbound]= np.nan
tex_data_120[tex_data_120>ubound]= np.nan
im2 = m.contourf(x, y, tex_data_120.T, alpha=0.4, cmap='YlOrRd', levels=tex_levels)
divider = make_axes_locatable(ax3)
cax = divider.append_axes("right", size="5%", pad=0.1)
cax2 = divider.append_axes("right", size="5%", pad=0.3)
cbr = plt.colorbar(im, cax=cax)
cbr2 = plt.colorbar(im2,cax=cax2)
#
#
ax4 = fig.add_subplot(3,5,15)
ax4.set_title('160 square pixel \n 75th - 100th Percentile')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
im = m.contourf(x,y,ss_data_50.T, cmap='Greys_r',levels=ss_level)
lbound, ubound = get_bounds(df_160,6,7)
tex_data_160[tex_data_160<lbound]= np.nan
tex_data_160[tex_data_160>ubound]= np.nan
im2 = m.contourf(x, y, tex_data_160.T, alpha=0.4, cmap='YlOrRd', levels=tex_levels)
divider = make_axes_locatable(ax4)
cax = divider.append_axes("right", size="5%", pad=0.1)
cax2 = divider.append_axes("right", size="5%", pad=0.3)
cbr = plt.colorbar(im, cax=cax)
cbr2 = plt.colorbar(im2,cax=cax2)
#plt.show()

plt.suptitle('Spatial Variations of texture lenthscales', fontsize=12)
plt.savefig(r"C:\workspace\Merged_SS\window_analysis\10_percent_shift\output\tex_mutiple_percentiles.png",dpi=1000)
#plt.show()

plt.close()


