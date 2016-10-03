# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 11:35:30 2016

@author: dan
"""

from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D
import gdal
import matplotlib.pyplot as plt
import numpy as np
import pyproj
import pandas as pd
from pandas.tools.plotting import table
from rasterstats import zonal_stats
from osgeo import ogr

def make_df(x):
    df = pd.DataFrame(x.flatten())
    return df
def mean(obs):
    return (1. / len(obs)) * np.sum(obs)

def variance(obs):
    return (1. / len(obs)) * np.sum((obs - mean(obs)) ** 2)
    
def mykurt(x):
    num = np.sum((x - mean(x)) ** 4)/ len(x)
    denom = variance(x) ** 2
    return num / denom
    
def myskew(x):
    df = make_df(x)
    skew = df.skew().values
    return float(skew[0])
    

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


##################################################################################################################
#Summary Statistics Table 
in_shp = r"C:\workspace\Merged_SS\window_analysis\shapefiles\tex_seg_2014_09_67.shp"
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
df['std_error']=df['std']/np.sqrt(df['count'])

sub = df[['substrate','mean','std','std_error','25%','50%','75%','kurt','skew']]
pivot_table = pd.pivot_table(sub, values=['std_error','mean','std','std_error','25%','50%','75%','kurt','skew'], 
                             index='substrate',aggfunc=np.average).sort_values(['std'])


nrows, ncols = 8, 2
hcell, wcell = 0.3, 1.
hpad,wpad = 0,0
##################################################################################################################

xx, yy = np.mgrid[xmin:xmax+xres:xres, ymax+yres:ymin:yres]

trans =  pyproj.Proj(init="epsg:26949") 
glon, glat = trans(xx, yy, inverse=True)
#ortho_lon, ortho_lat = trans(ortho_x, ortho_y, inverse=True)
cs2cs_args = "epsg:26949"
ss_level=[0,2.5,5,7.5,10,12.5,15,17.5,20,22.5,25,27.5,30,32.5,35]

fig = plt.figure(figsize=(12,10))
#ax = fig.add_subplot(2,2,1)
ax = plt.subplot2grid((3,2),(0,0),rowspan=3)
ax.set_title('September 2014 \n R01767')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon) - 0.0009, 
            llcrnrlat=np.min(glat) - 0.0006,
            urcrnrlon=np.max(glon) + 0.0009, 
            urcrnrlat=np.max(glat) + 0.0006)
m.wmsimage(server='http://grandcanyon.usgs.gov/arcgis/services/Imagery/ColoradoRiverImageryExplorer/MapServer/WmsServer?', layers=['0'], xpixels=1000)
x,y = m.projtran(glon, glat)
im = m.contourf(x,y,data.T, cmap='Greys_r',levels=ss_level)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
cbr = plt.colorbar(im, cax=cax)
cbr.set_label('Sidescan Intensity [dBw]', size=10)

#read shapefile and create polygon collections
##NOTE: Shapefile has to be in WGS84
m.readshapefile( r"C:\workspace\Merged_SS\window_analysis\shapefiles\tex_seg_2014_09_67_geo","layer",drawbounds = False)

#sand, sand/gravel, gravel/sand, ledge, gravel, gravel/boulders, boulders, boulder
s_patch, sg_patch, gs_patch, g_patch, gb_patch, b_patch  =[],[],[],[],[],[]

for info, shape in zip(m.layer_info, m.layer):
    if info['substrate'] == 'sand':
        s_patch.append(Polygon(np.asarray(shape),True))
    if info['substrate'] == 'sand/gravel':
        sg_patch.append(Polygon(np.asarray(shape),True))        
    if info['substrate'] == 'gravel/sand':
        gs_patch.append(Polygon(np.asarray(shape),True))      
    if info['substrate'] == 'gravel':
        g_patch.append(Polygon(np.asarray(shape),True))         
    if info['substrate'] == 'gravel/boulders':
        gb_patch.append(Polygon(np.asarray(shape),True))          
    if info['substrate'] == 'boulders':
        b_patch.append(Polygon(np.asarray(shape),True))

        
a_val = 0.6
colors = ['#8c510a','#d8b365','#f6e8c3','#c7eae5','#5ab4ac','#01665e']
ax.add_collection(PatchCollection(s_patch, facecolor = colors[0],alpha=a_val, edgecolor='none',zorder=10))#,alpha=0.4
ax.add_collection(PatchCollection(sg_patch, facecolor = colors[1],alpha=a_val, edgecolor='none',zorder=10))#,alpha=0.4
ax.add_collection(PatchCollection(gs_patch, facecolor = colors[2],alpha=a_val, edgecolor='none',zorder=10))    # ,alpha=0.4
ax.add_collection(PatchCollection(g_patch, facecolor = colors[3],alpha=a_val, edgecolor='none',zorder=10)) #,alpha=0.4
ax.add_collection(PatchCollection(gb_patch, facecolor = colors[4],alpha=a_val, edgecolor='none',zorder=10)) #,alpha=0.4
ax.add_collection(PatchCollection(b_patch, facecolor = colors[5],alpha=a_val, edgecolor='none',zorder=10)) #,alpha=0.4

#create legend
circ1 = Line2D([0], [0], linestyle="none", marker="o", markersize=10, markerfacecolor=colors[0],alpha=a_val)
circ2 = Line2D([0], [0], linestyle="none", marker="o", markersize=10, markerfacecolor=colors[1],alpha=a_val)
circ3 = Line2D([0], [0], linestyle="none", marker="o", markersize=10, markerfacecolor=colors[2],alpha=a_val)
circ4 = Line2D([0], [0], linestyle="none", marker="o", markersize=10, markerfacecolor=colors[3],alpha=a_val)
circ5 = Line2D([0], [0], linestyle="none", marker="o", markersize=10, markerfacecolor=colors[4],alpha=a_val)
circ6 = Line2D([0], [0], linestyle="none", marker="o", markersize=10, markerfacecolor=colors[5],alpha=a_val)

#ax1 = fig.add_subplot(2,2,2)
ax1 = plt.subplot2grid((3,2),(0,1))
ax1.xaxis.set_visible(False)
ax1.yaxis.set_visible(False)
#hide the spines
for sp in ax1.spines.itervalues():
    sp.set_color('w')
    sp.set_zorder(0)

  
ax1.legend((circ1, circ2, circ3,circ4, circ5,circ6), ("sand", "sand/gravel", "gravel/sand","gravel","gravel/boulders","boulders"), 
           numpoints=1, loc='center left', borderaxespad=0.)   #bbox_to_anchor=(0.3, 0.9),

#ax2 = fig.add_subplot(2,2,3)
ax2 = plt.subplot2grid((3,2),(1,1),colspan=2)
ax2.xaxis.set_visible(False)
ax2.yaxis.set_visible(False)
for sp in ax2.spines.itervalues():
    sp.set_color('w')
    sp.set_zorder(0)
the_table = table(ax2, pivot_table.round(3),loc='center left',colWidths=[0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1])
the_table.set_fontsize(10)
plt.tight_layout(w_pad=10)#w_pad = 
plt.savefig(r"C:\workspace\Merged_SS\window_analysis\10_percent_shift\output\ss_visual_seg_2014_09_R01767.png", dpi=1000)
#plt.show()