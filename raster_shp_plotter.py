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


ss_raster = r"C:\workspace\Merged_SS\window_analysis\raster\ss_10_rasterclipped.tif"
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
in_shp = r"C:\workspace\Merged_SS\window_analysis\shapefiles\tex_seg_800.shp"
stats = zonal_stats(in_shp ,ss_raster,
                    stats=['min','max','median','std','count'])

df = pd.DataFrame(stats)

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

sub = df[['substrate','std_error']]
pivot_table = pd.pivot_table(sub,values='std_error',index='substrate',aggfunc=np.average).sort_values()


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

fig = plt.figure(figsize=(6,9))
ax = fig.add_subplot(1,2,1)
ax.set_title('April 2014')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.min(glon), 
            llcrnrlat=np.min(glat),
            urcrnrlon=np.max(glon), 
            urcrnrlat=np.max(glat))
x,y = m.projtran(glon, glat)
im = m.contourf(x,y,data.T, cmap='Greys_r',levels=ss_level)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
cbr = plt.colorbar(im, cax=cax)
#read shapefile and create polygon collections
m.readshapefile( r"C:\workspace\Merged_SS\window_analysis\shapefiles\tex_seg_800_geo","layer",drawbounds = False)

#sand, sand/gravel, gravel/sand, ledge, gravel, gravel/boulders, boulders, boulder
s_patch, sg_patch, gs_patch, l_patch, g_patch, gb_patch, b_patch ,b =[],[],[],[],[],[],[],[]

for info, shape in zip(m.layer_info, m.layer):
    if info['substrate'] == 'sand':
        s_patch.append(Polygon(np.asarray(shape),True))
    if info['substrate'] == 'sand/gravel':
        sg_patch.append(Polygon(np.asarray(shape),True))        
    if info['substrate'] == 'gravel/sand':
        gs_patch.append(Polygon(np.asarray(shape),True))
    if info['substrate'] == 'ledge':
        l_patch.append(Polygon(np.asarray(shape),True))        
    if info['substrate'] == 'gravel':
        g_patch.append(Polygon(np.asarray(shape),True))         
    if info['substrate'] == 'gravel/boulders':
        gb_patch.append(Polygon(np.asarray(shape),True))          
    if info['substrate'] == 'boulders':
        b_patch.append(Polygon(np.asarray(shape),True))
    if info['substrate'] == 'boulder':
        b.append(Polygon(np.asarray(shape),True))  
ax.add_collection(PatchCollection(s_patch, facecolor = '#f7fcfd',alpha=0.4, edgecolor='none',zorder=10))#,alpha=0.4
ax.add_collection(PatchCollection(sg_patch, facecolor = '#e5f5f9',alpha=0.4, edgecolor='none',zorder=10))#,alpha=0.4
ax.add_collection(PatchCollection(gs_patch, facecolor = '#ccece6',alpha=0.4, edgecolor='none',zorder=10))    # ,alpha=0.4
ax.add_collection(PatchCollection(l_patch, facecolor = '#99d8c9',alpha=0.4, edgecolor='none',zorder=10)) #,alpha=0.4
ax.add_collection(PatchCollection(g_patch, facecolor = '#66c2a4',alpha=0.4, edgecolor='none',zorder=10)) #,alpha=0.4
ax.add_collection(PatchCollection(gb_patch, facecolor = '#41ae76',alpha=0.4, edgecolor='none',zorder=10)) #,alpha=0.4
ax.add_collection(PatchCollection(b_patch, facecolor = '#238b45',alpha=0.4, edgecolor='none',zorder=10)) #,alpha=0.4
ax.add_collection(PatchCollection(b, facecolor = '#005824',alpha=0.4, edgecolor='none',zorder=10)) #alpha=0.4,
   
#create legend
circ1 = Line2D([0], [0], linestyle="none", marker="o", markersize=10, markerfacecolor="#f7fcfd",alpha=0.4)
circ2 = Line2D([0], [0], linestyle="none", marker="o", markersize=10, markerfacecolor="#e5f5f9",alpha=0.4)
circ3 = Line2D([0], [0], linestyle="none", marker="o", markersize=10, markerfacecolor="#ccece6",alpha=0.4)
circ4 = Line2D([0], [0], linestyle="none", marker="o", markersize=10, markerfacecolor="#99d8c9",alpha=0.4)
circ5 = Line2D([0], [0], linestyle="none", marker="o", markersize=10, markerfacecolor="#66c2a4",alpha=0.4)
circ6 = Line2D([0], [0], linestyle="none", marker="o", markersize=10, markerfacecolor="#41ae76",alpha=0.4)
circ7 = Line2D([0], [0], linestyle="none", marker="o", markersize=10, markerfacecolor="#238b45",alpha=0.4)
circ8 = Line2D([0], [0], linestyle="none", marker="o", markersize=10, markerfacecolor="#005824",alpha=0.4)


ax1 = fig.add_subplot(1,2,2)
ax1.xaxis.set_visible(False)
ax1.yaxis.set_visible(False)
#hide the spines
for sp in ax1.spines.itervalues():
    sp.set_color('w')
    sp.set_zorder(0)
the_table = table(ax1, pivot_table.round(3),loc='center',colWidths=[0.3])
the_table.set_fontsize(16)
  
ax1.legend((circ1, circ2, circ3,circ4,circ5, circ6,circ7, circ8), ("sand", "sand/gravel", "gravel/sand","ledge","gravel","gravel/boulders","boulders","boulder"), 
           numpoints=1,bbox_to_anchor=(0.3, 0.9), loc=0, borderaxespad=0.)   
plt.tight_layout(w_pad = 12)
plt.savefig(r"C:\workspace\Merged_SS\window_analysis\output\tex_seg_raster_table.png", dpi=1000)
#plt.show()