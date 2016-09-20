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

tex_raster = r"C:\workspace\Merged_SS\window_analysis\10_percent_shift\raster\tex_50_rasterclipped.tif"
ds = gdal.Open(tex_raster)
tex_data_50 = ds.GetRasterBand(1).ReadAsArray()
tex_data_50[tex_data_50<=0] = np.nan
del ds

tex_raster = r"C:\workspace\Merged_SS\window_analysis\10_percent_shift\raster\tex_55_rasterclipped.tif"
ds = gdal.Open(tex_raster)
tex_data_55 = ds.GetRasterBand(1).ReadAsArray()
tex_data_55[tex_data_55<=0] = np.nan
del ds


tex_raster = r"C:\workspace\Merged_SS\window_analysis\10_percent_shift\raster\tex_60_rasterclipped.tif"
ds = gdal.Open(tex_raster)
tex_data_60 = ds.GetRasterBand(1).ReadAsArray()
tex_data_60[tex_data_60<=0] = np.nan
del ds

tex_raster = r"C:\workspace\Merged_SS\window_analysis\10_percent_shift\raster\tex_65_rasterclipped.tif"
ds = gdal.Open(tex_raster)
tex_data_65 = ds.GetRasterBand(1).ReadAsArray()
tex_data_65[tex_data_65<=0] = np.nan
del ds

tex_raster = r"C:\workspace\Merged_SS\window_analysis\10_percent_shift\raster\tex_70_rasterclipped.tif"
ds = gdal.Open(tex_raster)
tex_data_70 = ds.GetRasterBand(1).ReadAsArray()
tex_data_70[tex_data_70<=0] = np.nan
del ds

tex_raster = r"C:\workspace\Merged_SS\window_analysis\10_percent_shift\raster\tex_80_rasterclipped.tif"
ds = gdal.Open(tex_raster)
tex_data_80 = ds.GetRasterBand(1).ReadAsArray()
tex_data_80[tex_data_80<=0] = np.nan
del ds

tex_raster = r"C:\workspace\Merged_SS\window_analysis\10_percent_shift\raster\tex_120_rasterclipped.tif"
ds = gdal.Open(tex_raster)
tex_data_120 = ds.GetRasterBand(1).ReadAsArray()
tex_data_120[tex_data_120<=0] = np.nan
del ds

tex_raster = r"C:\workspace\Merged_SS\window_analysis\10_percent_shift\raster\tex_160_rasterclipped.tif"
ds = gdal.Open(tex_raster)
tex_data_160 = ds.GetRasterBand(1).ReadAsArray()
tex_data_160[tex_data_160<=0] = np.nan
del ds

df_50 = convert_to_dataframe(tex_data_50)
df_55 = convert_to_dataframe(tex_data_55)
df_60 = convert_to_dataframe(tex_data_60)
df_65 = convert_to_dataframe(tex_data_65)
df_70 = convert_to_dataframe(tex_data_70)
df_80 = convert_to_dataframe(tex_data_80)
df_120 = convert_to_dataframe(tex_data_120)
df_160 = convert_to_dataframe(tex_data_160)

bin_s = list(np.arange(0,3.25,0.05))

fig = plt.figure(figsize=(22,3))
ax1 = fig.add_subplot(1,8,1)
df_50.plot(ax = ax1, kind='hist',bins=bin_s, legend=False)
table2 = table(ax1, np.round(df_50.describe(),3), loc='upper right', colWidths=[0.2])
table2.auto_set_font_size(False)
table2.set_fontsize(4)
ax1.set_ylabel('frequency')
ax1.set_xlabel('Texture Lengthscale (m)')
ax1.set_title('50 Pixel Window')

ax1 = fig.add_subplot(1,8,2)
df_55.plot(ax = ax1, kind='hist',bins=bin_s, legend=False)
table2 = table(ax1, np.round(df_55.describe(),3), loc='upper right', colWidths=[0.2])
table2.auto_set_font_size(False)
table2.set_fontsize(4)
ax1.set_ylabel('frequency')
ax1.set_xlabel('Texture Lengthscale (m)')
ax1.set_title('55 Pixel Window')

ax1 = fig.add_subplot(1,8,3)
df_60.plot(ax = ax1, kind='hist',bins=bin_s, legend=False)
table2 = table(ax1, np.round(df_60.describe(),3), loc='upper right', colWidths=[0.2])
table2.auto_set_font_size(False)
table2.set_fontsize(4)
ax1.set_ylabel('frequency')
ax1.set_xlabel('Texture Lengthscale (m)')
ax1.set_title('60 Pixel Window')

ax1 = fig.add_subplot(1,8,4)
df_65.plot(ax = ax1, kind='hist',bins=bin_s, legend=False)
table2 = table(ax1, np.round(df_65.describe(),3), loc='upper right', colWidths=[0.2])
table2.auto_set_font_size(False)
table2.set_fontsize(4)
ax1.set_ylabel('frequency')
ax1.set_xlabel('Texture Lengthscale (m)')
ax1.set_title('65 Pixel Window')

ax2 = fig.add_subplot(1,8,5)
df_70.plot(ax=ax2,kind='hist',bins=bin_s, legend=False)
table2=table(ax2, np.round(df_70.describe(),3), loc='upper right', colWidths=[0.2])
table2.set_fontsize(12)
ax2.set_ylabel('frequency')
ax2.set_xlabel('Texture Lengthscale (m)')
ax2.set_title('70 Pixel Window')

ax3 = fig.add_subplot(1,8,6)
df_80.plot(ax=ax3,kind='hist',bins=bin_s, legend=False)
table1 = table(ax3, np.round(df_80.describe(),3), loc='upper right', colWidths=[0.2])
ax3.set_ylabel('frequency')
ax3.set_xlabel('Texture Lengthscale (m)')
ax3.set_title('80 Pixel Window')

ax4 = fig.add_subplot(1,8,7)
df_120.plot(ax=ax4, kind='hist',bins=bin_s, legend=False)
table(ax4, np.round(df_120.describe(),3), loc='upper right', colWidths=[0.2])
ax4.set_ylabel('frequency')
ax4.set_xlabel('Texture Lengthscale (m)')
ax4.set_title('120 Pixel Window')

ax5 = fig.add_subplot(1,8,8)
df_160.plot(ax=ax5, kind='hist',bins=bin_s, legend=False)
table(ax5, np.round(df_160.describe(),3), loc='upper right', colWidths=[0.2])
ax5.set_ylabel('frequency')
ax5.set_xlabel('Texture Lengthscale (m)')
ax5.set_title('160 Pixel Window')
fig.tight_layout()
plt.savefig(r"C:\workspace\Merged_SS\window_analysis\10_percent_shift\output\Texture_lenghtscale_distributions_normalized_maxscale.png", dpi=600)
plt.show()

