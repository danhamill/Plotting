# -*- coding: utf-8 -*-
"""
Created on Tue Oct 04 13:47:11 2016

@author: dan
"""

from rasterstats import zonal_stats
import matplotlib.pyplot as plt
import pandas as pd
import gdal
import ogr
import numpy as np

def make_df(x):
    df = pd.DataFrame(x,columns=['dBW'])
    return df

ss_raster = r"C:\workspace\Merged_SS\raster\2014_09\ss_2014_09_R01767_raster.tif"
ds = gdal.Open(ss_raster)
data = ds.GetRasterBand(1).ReadAsArray()
data[data<=0] = np.nan
del ds

in_shp = r"C:\workspace\Merged_SS\window_analysis\shapefiles\tex_seg_2014_09_67.shp"
z_stats = zonal_stats(in_shp ,ss_raster,
                    stats=['count'],
                    raster_out=True)

#Lets get get the substrate+codes
ds = ogr.Open(in_shp)
lyr = ds.GetLayer(0)
a=[]
for row in lyr:
    a.append(row.substrate)
lyr.ResetReading()
del ds

s, sg, g, gs, gb, b = [],[],[],[],[],[]
n = 0
for item in z_stats:
    raster_array = item['mini_raster_array'].compressed()
    substrate = a[n]
    if substrate=='sand':
        s.extend(list(raster_array))
    if substrate=='sand/gravel':
        sg.extend(list(raster_array))
    if substrate=='gravel':
        g.extend(list(raster_array))
    if substrate=='gravel/sand':
        gs.extend(list(raster_array))
    if substrate=='gravel/boulders':
        gb.extend(list(raster_array))
    if substrate=='boulders':
        b.extend(list(raster_array))
    n+=1
del raster_array, substrate    

s_df = make_df(s)
sg_df = make_df(sg)
g_df = make_df(g)
gs_df = make_df(gs)
gb_df = make_df(gb)
b_df = make_df(b)

fig = plt.figure(figsize=(5,10))
ax1 = fig.add_subplot(6,1,6)
b_df.plot.hist(ax=ax1)
ax1.set_title('Boulders')
ax1.set_xlabel('Sidescan Intensity [dBW]')
ax = fig.add_subplot(611, sharex=ax1)
s_df.plot.hist(ax=ax)
ax.set_title('Sand')
ax = fig.add_subplot(612)
sg_df.plot.hist(ax=ax)
ax.set_title('Sand/Gravel')
ax = fig.add_subplot(613, sharex=ax1)
g_df.plot.hist(ax=ax)
ax.set_title('Gravel')
ax = fig.add_subplot(614,sharex=ax1)
gs_df.plot.hist(ax=ax)
ax.set_title('Gravel/Sand')
ax = fig.add_subplot(615,sharex=ax1)
gb_df.plot.hist(ax=ax)
ax.set_title('Gravel/Boulders')
ax = fig.add_subplot(616,sharex=ax1)
b_df.plot.hist(ax=ax)
ax.set_title('Boulders')
plt.tight_layout()
plt.savefig(r"C:\workspace\Merged_SS\window_analysis\10_percent_shift\output\substrate_ss_intensity_distribution.png", dpi = 600)
plt.close()


