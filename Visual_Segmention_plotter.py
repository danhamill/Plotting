# -*- coding: utf-8 -*-
"""
Created on Tue Oct 04 15:22:57 2016

@author: dan
"""

from rasterstats import zonal_stats
import pandas as pd
import ogr
import gdal
import numpy as np
from pandas.tools.plotting import table
import pyproj

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D

def make_df(x):
    df = pd.DataFrame(x.compressed())
    return df
def make_df2(x):
    df = pd.DataFrame(x,columns=['dBW'])
    return df
def mykurt(x):
    df = make_df(x)
    return float(df.kurtosis().values)
    
def myskew(x):
    df = make_df(x)
    skew = df.skew().values
    return float(skew[0])
    
def sort_hack(row):
    if row['substrate']=='sand':
        return 1
    if row['substrate']=='sand/gravel':
        return 2
    if row['substrate']=='gravel':
        return 3
    if row['substrate']=='gravel/sand':
        return 4
    if row['substrate']=='gravel/boulders':
        return 5
    if row['substrate']=='boulders':
        return 6   

ss_raster = r"C:\workspace\Merged_SS\raster\2014_09\ss_2014_09_R01767_raster.tif"
in_shp = r"C:\workspace\Merged_SS\window_analysis\shapefiles\tex_seg_2014_09_67_3class.shp"
z_stats = zonal_stats(in_shp ,ss_raster,
                    stats=['min','mean','max','median','std','count','percentile_25','percentile_50','percentile_75'],
                    add_stats = {'kurt':mykurt,'skew':myskew})

df = pd.DataFrame(z_stats)
df.rename(columns={'percentile_25': '25%', 'percentile_50': '50%', 'percentile_75':'75%'}, inplace=True) 

#Lets get get the substrate+codes
ds = ogr.Open(in_shp)
lyr = ds.GetLayer(0)
a=[]
for row in lyr:
    a.append(row.substrate)
lyr.ResetReading()
del ds

df['substrate']=a
df['CV']=df['std']/df['mean']

sand = df[df['substrate']=='sand']
gravel = df[df['substrate']=='gravel']
boulders = df[df['substrate']=='boulders']

del a, df

in_shp = r"C:\workspace\Merged_SS\window_analysis\shapefiles\tex_seg_800_3class.shp"
ss_raster = r"C:\workspace\Merged_SS\window_analysis\10_percent_shift\raster\ss_50_rasterclipped.tif"
stats = zonal_stats(in_shp ,ss_raster,
                    stats=['min','mean','max','median','std','count','percentile_25','percentile_50','percentile_75'],
                    add_stats = {'kurt':mykurt,'skew':myskew})

df = pd.DataFrame(stats)
df.rename(columns={'percentile_25': '25%', 'percentile_50': '50%', 'percentile_75':'75%'}, inplace=True) 

#Lets get get the substrate+codes
ds = ogr.Open(in_shp)
lyr = ds.GetLayer(0)
a=[]
for row in lyr:
    a.append(row.substrate)
lyr.ResetReading()
del ds

df['substrate']=a
df['CV']=df['std']/df['mean']



sand1 = df[df['substrate']=='sand']
gravel1 = df[df['substrate']=='gravel']
boulders1 = df[df['substrate']=='boulders']

boulders = pd.concat([boulders,boulders1])
gravel = pd.concat([gravel,gravel1])
sand = pd.concat([sand,sand1])
del sand1, gravel1, boulders1, a

#Plots showing how statisics compare to eachother
#Kurtosis vs sample size
fig = plt.figure()
ax = fig.add_subplot(311)
sand.plot.scatter(ax = ax, x='count',y='kurt',label='sand', ylim=(-1,1))
ax = fig.add_subplot(312)
gravel.plot.scatter(ax = ax, x='count',y='kurt',label='gravel', ylim=(-1,1))
ax = fig.add_subplot(313)
boulders.plot.scatter(ax=ax, x='count',y='kurt', label='boulders', ylim=(-1,1))
plt.suptitle('Kurtosis vs. Count')
plt.tight_layout()
plt.savefig(r"c:\workspace\Texture_Classification\output\substrate_stat_plots\visual_kurt.png", dpi = 600)

#std vs sample size
fig = plt.figure()
ax = fig.add_subplot(311)
sand.plot.scatter(ax = ax, x='count',y='std',label='sand', ylim=(0,5))
ax = fig.add_subplot(312)
gravel.plot.scatter(ax = ax, x='count',y='std',label='gravel', ylim=(0,5))
ax = fig.add_subplot(313)
boulders.plot.scatter(ax=ax, x='count',y='std', label='boulders', ylim=(0,5))
plt.suptitle('std vs. Count')
plt.tight_layout()
plt.savefig(r"c:\workspace\Texture_Classification\output\substrate_stat_plots\visual_skew.png", dpi = 600)

#std vs sample size
fig = plt.figure()
ax = fig.add_subplot(311)
sand.plot.scatter(ax = ax, x='kurt',y='std',label='sand', ylim=(0,5))
ax = fig.add_subplot(312)
gravel.plot.scatter(ax = ax, x='kurt',y='std',label='gravel', ylim=(0,5))
ax = fig.add_subplot(313)
boulders.plot.scatter(ax=ax, x='kurt',y='std', label='boulders', ylim=(0,5))
plt.suptitle('std vs. kurt')
plt.tight_layout()
plt.savefig(r"c:\workspace\Texture_Classification\output\substrate_stat_plots\visual_std_vs_kurt.png", dpi = 600)
del sand, gravel, boulders, z_stats


#Aggregreated Distributions
ss_raster = r"C:\workspace\Merged_SS\raster\2014_09\ss_2014_09_R01767_raster.tif"
in_shp = r"C:\workspace\Merged_SS\window_analysis\shapefiles\tex_seg_2014_09_67_3class.shp"
z_stats_67 = zonal_stats(in_shp ,ss_raster,stats=['count'],raster_out=True)

#Lets get get the substrate codes
ds = ogr.Open(in_shp)
lyr = ds.GetLayer(0)
a=[]
for row in lyr:
    a.append(row.substrate)
lyr.ResetReading()
del ds

s, g, b = [],[],[]
n = 0
for item in z_stats_67:
    raster_array = item['mini_raster_array'].compressed()
    substrate = a[n]
    if substrate=='sand':
        s.extend(list(raster_array))
    if substrate=='gravel':
        g.extend(list(raster_array))
    if substrate=='boulders':
        b.extend(list(raster_array))
    n+=1
del raster_array, substrate, n, item, a

s_df = make_df2(s)
g_df = make_df2(g)
b_df = make_df2(b)


tbl = pd.DataFrame(columns=['substrate','mean','std','CV','25%','50%','75%','kurt','skew'])
tbl['substrate']=['sand','gravel','boulders']
tbl = tbl.set_index('substrate')
tbl.loc['sand'] = pd.Series({'mean':np.mean(s_df['dBW']),'std':np.std(s_df['dBW']) ,'CV':np.mean(s_df['dBW'])/np.std(s_df['dBW']),'25%':float(s_df.describe().iloc[4].values), '50%':float(s_df.describe().iloc[5].values),'75%':float(s_df.describe().iloc[6].values),'kurt':float(s_df.kurtosis().values),'skew':float(s_df.skew().values)})
tbl.loc['gravel'] = pd.Series({'mean':np.mean(g_df['dBW']),'std':np.std(g_df['dBW']) ,'CV':np.mean(g_df['dBW'])/np.std(g_df['dBW']),'25%':float(g_df.describe().iloc[4].values), '50%':float(g_df.describe().iloc[5].values),'75%':float(g_df.describe().iloc[6].values),'kurt':float(g_df.kurtosis().values),'skew':float(g_df.skew().values)})
tbl.loc['boulders'] = pd.Series({'mean':np.mean(b_df['dBW']),'std':np.std(b_df['dBW']) ,'CV':np.mean(b_df['dBW'])/np.std(b_df['dBW']),'25%':float(b_df.describe().iloc[4].values), '50%':float(b_df.describe().iloc[5].values),'75%':float(b_df.describe().iloc[6].values),'kurt':float(b_df.kurtosis().values),'skew':float(b_df.skew().values)})
tbl = tbl.applymap(lambda x: round(x,3))
del s_df, g_df, b_df

fig = plt.figure()
ax = fig.add_subplot(111)
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
for sp in ax.spines.itervalues():
    sp.set_color('w')
    sp.set_zorder(0)
the_table = table(ax, tbl.round(3),loc='best',colWidths=[0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1])
the_table.set_fontsize(12)
plt.tight_layout()
plt.savefig(r"c:\workspace\Texture_Classification\output\substrate_stat_plots\visual_agg_distribution_table_spet_14.png")
del tbl


in_shp = r"C:\workspace\Merged_SS\window_analysis\shapefiles\tex_seg_800_3class.shp"
ss_raster = r"C:\workspace\Merged_SS\window_analysis\raster\ss_10_rasterclipped.tif"
z_stats_46 = zonal_stats(in_shp ,ss_raster,stats=['count'],raster_out=True)


#Lets get get the substrate codes
ds = ogr.Open(in_shp)
lyr = ds.GetLayer(0)
a=[]
for row in lyr:
    a.append(row.substrate)
lyr.ResetReading()
del ds


n = 0
for item in z_stats_46:
    raster_array = item['mini_raster_array'].compressed()
    substrate = a[n]
    if substrate=='sand':
        s.extend(list(raster_array))
    if substrate=='gravel':
        g.extend(list(raster_array))
    if substrate=='boulders':
        b.extend(list(raster_array))
    n+=1
del raster_array, substrate, n, item, a

s_df = make_df2(s)
g_df = make_df2(g)
b_df = make_df2(b)
del s, g, b, z_stats_46, z_stats_67

tbl = pd.DataFrame(columns=['substrate','mean','std','CV','25%','50%','75%','kurt','skew'])
tbl['substrate']=['sand','gravel','boulders']
tbl = tbl.set_index('substrate')
tbl.loc['sand'] = pd.Series({'mean':np.mean(s_df['dBW']),'std':np.std(s_df['dBW']) ,'CV':np.mean(s_df['dBW'])/np.std(s_df['dBW']),'25%':float(s_df.describe().iloc[4].values), '50%':float(s_df.describe().iloc[5].values),'75%':float(s_df.describe().iloc[6].values),'kurt':float(s_df.kurtosis().values),'skew':float(s_df.skew().values)})
tbl.loc['gravel'] = pd.Series({'mean':np.mean(g_df['dBW']),'std':np.std(g_df['dBW']) ,'CV':np.mean(g_df['dBW'])/np.std(g_df['dBW']),'25%':float(g_df.describe().iloc[4].values), '50%':float(g_df.describe().iloc[5].values),'75%':float(g_df.describe().iloc[6].values),'kurt':float(g_df.kurtosis().values),'skew':float(g_df.skew().values)})
tbl.loc['boulders'] = pd.Series({'mean':np.mean(b_df['dBW']),'std':np.std(b_df['dBW']) ,'CV':np.mean(b_df['dBW'])/np.std(b_df['dBW']),'25%':float(b_df.describe().iloc[4].values), '50%':float(b_df.describe().iloc[5].values),'75%':float(b_df.describe().iloc[6].values),'kurt':float(b_df.kurtosis().values),'skew':float(b_df.skew().values)})
tbl = tbl.applymap(lambda x: round(x,3))
del s_df, g_df, b_df

fig = plt.figure()
ax = fig.add_subplot(111)
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
for sp in ax.spines.itervalues():
    sp.set_color('w')
    sp.set_zorder(0)
the_table = table(ax, tbl.round(3),loc='best',colWidths=[0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1])
the_table.set_fontsize(12)
plt.tight_layout()
plt.savefig(r"c:\workspace\Texture_Classification\output\substrate_stat_plots\visual_agg_distribution_combined.png")


#########################################################################################################################
########################################################################################################################
#                   Begin Plotting Routine
#########################################################################################################################
#########################################################################################################################


ss_raster = r"C:\workspace\Merged_SS\raster\2014_09\ss_2014_09_R01767_raster.tif"
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
xx, yy = np.mgrid[xmin:xmax+xres:xres, ymax+yres:ymin:yres]

trans =  pyproj.Proj(init="epsg:26949") 
glon, glat = trans(xx, yy, inverse=True)


#plotting variables
a_val = 0.6
colors = ['#ef8a62','#f7f7f7','#67a9cf']
circ1 = Line2D([0], [0], linestyle="none", marker="o", markersize=10, markerfacecolor=colors[0],alpha=a_val)
circ2 = Line2D([0], [0], linestyle="none", marker="o", markersize=10, markerfacecolor=colors[1],alpha=a_val)
circ3 = Line2D([0], [0], linestyle="none", marker="o", markersize=10, markerfacecolor=colors[2],alpha=a_val)
wms_url = r"http://grandcanyon.usgs.gov/arcgis/services/Imagery/ColoradoRiverImageryExplorer/MapServer/WmsServer?"
font_size=10


print 'Now plotting September 2014...'
#ortho_lon, ortho_lat = trans(ortho_x, ortho_y, inverse=True)
cs2cs_args = "epsg:26949"
ss_level=[0,2.5,5,7.5,10,12.5,15,17.5,20,22.5,25,27.5,30,32.5,35]

fig = plt.figure(figsize=(15,12))
ax = plt.subplot2grid((10,2),(0, 0),rowspan=9)
ax.set_title('September 2014 \n R01767')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon) - 0.0002, 
            llcrnrlat=np.min(glat) - 0.0006,
            urcrnrlon=np.max(glon) + 0.0002, 
            urcrnrlat=np.max(glat) + 0.0006)
m.wmsimage(server=wms_url, layers=['3'], xpixels=1000)
x,y = m.projtran(glon, glat)
im = m.contourf(x,y,data.T, cmap='Greys_r',levels=ss_level)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
cbr = plt.colorbar(im, cax=cax)
cbr.set_label('Sidescan Intensity [dBW]', size=10)

#read shapefile and create polygon collections
##NOTE: Shapefile has to be in WGS84
m.readshapefile( r"C:\workspace\Merged_SS\window_analysis\shapefiles\tex_seg_2014_09_67_geo","layer",drawbounds = False)

#sand, sand/gravel, gravel/sand, ledge, gravel, gravel/boulders, boulders, boulder
s_patch, g_patch, b_patch  =[],[],[]

for info, shape in zip(m.layer_info, m.layer):
    if info['substrate'] == 'sand':
        s_patch.append(Polygon(np.asarray(shape),True))          
    if info['substrate'] == 'gravel':
        g_patch.append(Polygon(np.asarray(shape),True))                
    if info['substrate'] == 'boulders':
        b_patch.append(Polygon(np.asarray(shape),True))
del info, shape

 
ax.add_collection(PatchCollection(s_patch, facecolor = colors[0],alpha=a_val, edgecolor='none',zorder=10))
ax.add_collection(PatchCollection(g_patch, facecolor = colors[1],alpha=a_val, edgecolor='none',zorder=10)) 
ax.add_collection(PatchCollection(b_patch, facecolor = colors[2],alpha=a_val, edgecolor='none',zorder=10))
del s_patch, g_patch, b_patch

ax.legend((circ1, circ2, circ3), ("sand", "gravel", "boulders"), numpoints=1, loc='best', borderaxespad=0., fontsize=font_size) 




    
ss_raster = r"C:\workspace\Merged_SS\window_analysis\10_percent_shift\raster\ss_50_rasterclipped.tif"
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
xx, yy = np.mgrid[xmin:xmax+xres:xres, ymax+yres:ymin:yres]

trans =  pyproj.Proj(init="epsg:26949") 
glon1, glat1 = trans(xx, yy, inverse=True)

#########################################################################################################################
########################################################################################################################
#                   Begin Subplot 2
#########################################################################################################################
#########################################################################################################################
print 'Now Plotting April 2014...'
ax = plt.subplot2grid((10,2),(0, 1),rowspan=9)
ax.set_title('April 2014 \n R01346 and R01347')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon1) - 0.0009, 
            llcrnrlat=np.min(glat1) - 0.0006,
            urcrnrlon=np.max(glon1) + 0.0009, 
            urcrnrlat=np.max(glat1) + 0.0013)
x,y = m.projtran(glon1, glat1)
m.wmsimage(server=wms_url, layers=['3'], xpixels=1000)
im = m.contourf(x,y,data.T, cmap='Greys_r',levels=ss_level)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
cbr = plt.colorbar(im, cax=cax)
cbr.set_label('Sidescan Intensity [dBW]', size=10)
m.readshapefile( r"C:\workspace\Merged_SS\window_analysis\shapefiles\tex_seg_800_geo","layer",drawbounds = False)

#sand, gravel, boulders
s_patch, g_patch, b_patch  =[],[],[]

for info, shape in zip(m.layer_info, m.layer):
    if info['substrate'] == 'sand':
        s_patch.append(Polygon(np.asarray(shape),True))   
    if info['substrate'] == 'gravel':
        g_patch.append(Polygon(np.asarray(shape),True))               
    if info['substrate'] == 'boulders':
        b_patch.append(Polygon(np.asarray(shape),True))
del info, shape

ax.add_collection(PatchCollection(s_patch, facecolor = colors[0],alpha=a_val, edgecolor='none',zorder=10))
ax.add_collection(PatchCollection(g_patch, facecolor = colors[1],alpha=a_val, edgecolor='none',zorder=10)) 
ax.add_collection(PatchCollection(b_patch, facecolor = colors[2],alpha=a_val, edgecolor='none',zorder=10))
del s_patch, g_patch, b_patch

ax.legend((circ1, circ2, circ3), ("sand", "gravel", "boulders"), numpoints=1, loc='best', borderaxespad=0., fontsize=font_size)

#########################################################################################################################
########################################################################################################################
#                   Begin Subplot 3: Table
#########################################################################################################################
#########################################################################################################################


ax2 = plt.subplot2grid((10,2),(9, 0), colspan=2)
ax2.xaxis.set_visible(False)
ax2.yaxis.set_visible(False)
for sp in ax2.spines.itervalues():
    sp.set_color('w')
    sp.set_zorder(0)

the_table = table(ax2, tbl,loc='upper right',colWidths=[0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1])
the_table.set_fontsize(font_size)



print 'Now Saving Figure...'

plt.savefig(r"c:\workspace\Texture_Classification\output\substrate_stat_plots\visual_agg_distribution_plots_table.png", dpi = 600)












