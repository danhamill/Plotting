# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 17:06:34 2016

@author: dan
"""

import pandas as pd
from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
from pandas.tools.plotting import table

def convert_to_dataframe(array):
    out_name = pd.DataFrame(array.flatten())
    out_name = out_name.dropna(axis=0)
    return out_name

ss_raster = r"C:\workspace\Merged_SS\window_analysis\raster\ss_10_raster.tif"
ds = gdal.Open(ss_raster)
data_10 = ds.GetRasterBand(1).ReadAsArray()
data_10[data_10<=0] = np.nan
del ds

tex_raster = r"C:\workspace\Merged_SS\window_analysis\raster\tex_10_raster.tif"
ds = gdal.Open(tex_raster)
tex_data_10 = ds.GetRasterBand(1).ReadAsArray()
tex_data_10[tex_data_10<=0] = np.nan
del ds

                    
ss_raster = r"C:\workspace\Merged_SS\window_analysis\raster\ss_20_raster.tif"
ds = gdal.Open(ss_raster)
data_20 = ds.GetRasterBand(1).ReadAsArray()
data_20[data_20<=0] = np.nan
del ds

tex_raster = r"C:\workspace\Merged_SS\window_analysis\raster\tex_20_raster.tif"
ds = gdal.Open(tex_raster)
tex_data_20 = ds.GetRasterBand(1).ReadAsArray()
tex_data_20[tex_data_20<=0] = np.nan
del ds


tex_raster_40 = r"C:\workspace\Merged_SS\window_analysis\raster\tex_40_rasterclipped.tif"
ds = gdal.Open(tex_raster_40)
tex_data_40 = ds.GetRasterBand(1).ReadAsArray()
tex_data_40[tex_data_40<=0] = np.nan
del ds


tex_raster_80 = r"C:\workspace\Merged_SS\window_analysis\raster\tex_80_rasterclipped.tif"
ds = gdal.Open(tex_raster_80)
tex_data_80 = ds.GetRasterBand(1).ReadAsArray()
tex_data_80[tex_data_80<=0] = np.nan
del ds

tex_raster_160 = r"C:\workspace\Merged_SS\window_analysis\raster\tex_160_rasterclipped.tif"
ds = gdal.Open(tex_raster_160)
tex_data_160 = ds.GetRasterBand(1).ReadAsArray()
tex_data_160[tex_data_160<=0] = np.nan
del ds

df_10 = convert_to_dataframe(tex_data_10)
df_20 = convert_to_dataframe(tex_data_20)
df_40 = convert_to_dataframe(tex_data_40)
df_80 = convert_to_dataframe(tex_data_80)
df_160 = convert_to_dataframe(tex_data_160)


bin_s=[0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.0]

fig = plt.figure(figsize=(12,3))
ax1 = fig.add_subplot(1,5,1)
df_10.plot(ax = ax1, kind='hist',bins=bin_s, legend=False)
table(ax1, np.round(df_10.describe(),3), loc='upper right', colWidths=[0.2])
ax1.set_ylabel('frequency')
ax1.set_xlabel('Texture Lengthscale (m)')
ax1.set_title('10 Pixel Window')

ax2 = fig.add_subplot(1,5,2)
df_20.plot(ax=ax2,kind='hist',bins=bin_s, legend=False)
table(ax2, np.round(df_20.describe(),3), loc='upper right', colWidths=[0.2])
ax2.set_ylabel('frequency')
ax2.set_xlabel('Texture Lengthscale (m)')
ax2.set_title('20 Pixel Window')

ax3 = fig.add_subplot(1,5,3)
df_40.plot(ax=ax3,kind='hist',bins=bin_s, legend=False)
table(ax3, np.round(df_40.describe(),3), loc='upper right', colWidths=[0.2])
ax3.set_ylabel('frequency')
ax3.set_xlabel('Texture Lengthscale (m)')
ax3.set_title('40 Pixel Window')

ax4 = fig.add_subplot(1,5,4)
df_80.plot(ax=ax4, kind='hist',bins=bin_s, legend=False)
table(ax4, np.round(df_80.describe(),3), loc='upper right', colWidths=[0.2])
ax4.set_ylabel('frequency')
ax4.set_xlabel('Texture Lengthscale (m)')
ax4.set_title('80 Pixel Window')

ax5 = fig.add_subplot(1,5,5)
df_160.plot(ax=ax5, kind='hist',bins=bin_s, legend=False)
table(ax5, np.round(df_160.describe(),3), loc='upper right', colWidths=[0.2])
ax5.set_ylabel('frequency')
ax5.set_xlabel('Texture Lengthscale (m)')
ax5.set_title('160 Pixel Window')
fig.tight_layout()
plt.show()

