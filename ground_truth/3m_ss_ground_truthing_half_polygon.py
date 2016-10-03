# -*- coding: utf-8 -*-
"""
Created on Mon Oct 03 10:08:09 2016

@author: dan
"""

from rasterstats import zonal_stats
import pandas as pd
import numpy as np
import ogr
import gdal
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
import pyproj
from pandas.tools.plotting import table

def assign_class(row):
    if row.sed5class == 1:
        return 'sand'
    if row.sed5class == 2:
        return 'sand/gravel'
    if row.sed5class == 3:
        return 'gravel'
    if row.sed5class == 4:
        return 'sand/rock'
    if row.sed5class == 5:
        return 'rock'
        
def make_df(x):
    df = pd.DataFrame(x.compressed())
    return df
    
def mykurt(x):
    df = make_df(x)
    return float(df.kurtosis().values)
    
def myskew(x):
    df = make_df(x)
    skew = df.skew().values
    return float(skew[0])

#Sidescan sonar imagery
ss_r28 = r"C:\workspace\Reach_4a\Multibeam\mb_sed_class\output\ss_R02028.tif"
ss_r31 = r"C:\workspace\Reach_4a\Multibeam\mb_sed_class\output\ss_R02031.tif"

#Buffered points
buff_shp = r"C:\workspace\Reach_4a\Multibeam\mb_sed_class\output\shapefiles\may2014_3m_buff.shp"

#Resampled sed5Class
sed_pts = r"C:\workspace\Reach_4a\Multibeam\mb_sed_class\may2014_mb6086r_sedclass\xy_sed5class_3m.csv"

#Read points
pts_df = pd.read_csv(sed_pts,sep=',',names=['northing','easting','sed5class'])
pts_df['sed5class'] = pts_df.apply(lambda row: assign_class(row), axis = 1)

#R02028 Zonal statistics
stats_28 = zonal_stats(buff_shp,ss_r28,stats=['min','mean','max','median','std','count','percentile_25','percentile_50','percentile_75'], add_stats = {'kurt':mykurt,'skew':myskew})
df = pd.DataFrame(stats_28)
df.rename(columns={'percentile_25': '25%', 'percentile_50': '50%', 'percentile_75':'75%'}, inplace=True)
df['substrate']=pts_df['sed5class']

#Determine threshold for stats
lbound = np.max(df['count'])/2
df = df[df['count']>lbound]
sub_28 = df[['substrate','mean','std','25%','50%','75%','kurt','skew']]
pivot_table_28 = pd.pivot_table(sub_28, values=['std_error','mean','std','25%','50%','75%','kurt','skew'], 
                             index='substrate',aggfunc=np.average).sort_values(['std'])
del df, lbound

#R02031 Zonal statistics
stats_31 = zonal_stats(buff_shp,ss_r31,stats=['min','mean','max','median','std','count','percentile_25','percentile_50','percentile_75'], add_stats = {'kurt':mykurt,'skew':myskew})
df = pd.DataFrame(stats_31)
df.rename(columns={'percentile_25': '25%', 'percentile_50': '50%', 'percentile_75':'75%'}, inplace=True)
df['substrate']=pts_df['sed5class']

#Determine threshold for stats
lbound = np.max(df['count'])/2
df = df[df['count']>lbound]
sub_31 = df[['substrate','mean','std','25%','50%','75%','kurt','skew']]
pivot_table_31 = pd.pivot_table(sub_31, values=['std_error','mean','std','25%','50%','75%','kurt','skew'], 
                             index='substrate',aggfunc=np.average).sort_values(['std'])
del df, lbound

#WGS shape files
buf_geo = r"C:\workspace\Reach_4a\Multibeam\mb_sed_class\output\shapefiles\may2014_3m_buff_geo.shp"

#count_28 = pd.DataFrame(stats_28)
#count_28 = count_28[['count']]
#count_31 = pd.DataFrame(stats_31)
#count_31 = count_31[['count']]
##Append sed5names to shapefile
#ds = ogr.Open(buf_geo,update=True)
#lyr = ds.GetLayer()
#lyr.CreateField(ogr.FieldDefn('substrate', ogr.OFTString))
#lyr.CreateField(ogr.FieldDefn('count_28', ogr.OFTReal))
#lyr.CreateField(ogr.FieldDefn('count_31', ogr.OFTReal))
#n=0
#for feature in lyr:
#    substrate = pts_df['sed5class'][n]
#    count28 = float(count_28['count'][n])
#    count31 = float(count_31['count'][n])
#    feature.SetField('substrate', substrate)
#    feature.SetField('count_28', count28)
#    feature.SetField('count_31', count31)
#    n += 1
#    lyr.SetFeature(feature)
#del ds, lyr, n, substrate, count28, count31


#Begin plotting routine

#Load R02028
R02028_raster = r"C:\workspace\Reach_4a\Multibeam\mb_sed_class\output\ss_R02028.tif"
ds = gdal.Open(R02028_raster)
R02028 = ds.GetRasterBand(1).ReadAsArray()
R02028[R02028<0]=np.nan
gt = ds.GetGeoTransform()
proj = ds.GetProjection()
 
xres = gt[1]
yres = gt[5]

xmin = gt[0] + xres * 0.5
xmax = gt[0] + (xres * ds.RasterXSize) - xres * 0.5
ymin = gt[3] + (yres * ds.RasterYSize) + yres * 0.5
ymax = gt[3] - yres * 0.5
extent = [xmin,xmax,ymin,ymax]
del ds

# create a grid of xy coordinates in the original projection
xx, yy = np.mgrid[xmin:xmax+xres:xres, ymax+yres:ymin:yres]
trans =  pyproj.Proj(init="epsg:26949") 
r28_lon, r28_lat = trans(xx, yy, inverse=True)
del xx, yy, xmin, xmax, ymin, ymax


#Load R02031
R02031_raster = r"C:\workspace\Reach_4a\Multibeam\mb_sed_class\output\ss_R02031.tif"
ds = gdal.Open(R02031_raster)
R02031 = ds.GetRasterBand(1).ReadAsArray()
R02031[R02031<0]=np.nan
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
r31_lon, r31_lat = trans(xx, yy, inverse=True)
del xx, yy, xmin, xmax, ymin, ymax


#legend Stuff
colors=['#ca0020','#f4a582','#f7f7f7','#92c5de','#0571b0']
a_val=0.6
circ1 = Line2D([0], [0], linestyle="none", marker="o", markersize=10, markerfacecolor=colors[0],alpha=a_val)
circ2 = Line2D([0], [0], linestyle="none", marker="o", markersize=10, markerfacecolor=colors[1],alpha=a_val)
circ3 = Line2D([0], [0], linestyle="none", marker="o", markersize=10, markerfacecolor=colors[2],alpha=a_val)
circ4 = Line2D([0], [0], linestyle="none", marker="o", markersize=10, markerfacecolor=colors[3],alpha=a_val)
circ5 = Line2D([0], [0], linestyle="none", marker="o", markersize=10, markerfacecolor=colors[4],alpha=a_val)
ss_level=[0,2.5,5,7.5,10,12.5,15,17.5,20,22.5,25,27.5,30,32.5,35]

print 'Now plotting R02028 Acoutic sediment classifications...'
#Begin the plot
cs2cs_args = "epsg:26949"
fig = plt.figure(figsize=(15,12))
ax = plt.subplot2grid((5,2),(0, 0),rowspan=4)
ax.set_title('R02028: 3 meter grid')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.nanmin(r28_lon)-0.0004, 
            llcrnrlat=np.nanmin(r28_lat)-0.0004,
            urcrnrlon=np.nanmax(r28_lon)+0.0004, 
            urcrnrlat=np.nanmax(r28_lat)+0.0004)
m.wmsimage(server='http://grandcanyon.usgs.gov/arcgis/services/Imagery/ColoradoRiverImageryExplorer/MapServer/WmsServer?', layers=['3'], xpixels=1000)
x,y = m.projtran(r28_lon, r28_lat)
im = m.contourf(x,y,R02028.T, cmap='Greys_r',levels=ss_level)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
cbr = plt.colorbar(im, cax=cax)
m.readshapefile(r"C:\workspace\Reach_4a\Multibeam\mb_sed_class\output\shapefiles\may2014_3m_buff_geo","layer",drawbounds = False)
#sand, sand/gravel, gravel, sand/rock, rock
s_patch, sg_patch, g_patch, sr_patch, r_patch, = [],[],[],[],[]
bound = max(stat['count'] for stat in stats_28)/2
for info, shape in zip(m.layer_info, m.layer):
    if info['substrate'] == 'sand' and info['count_28'] > bound:
        s_patch.append(Polygon(np.asarray(shape),True))
    if info['substrate'] == 'sand/gravel' and info['count_28'] > bound:
        sg_patch.append(Polygon(np.asarray(shape),True))        
    if info['substrate'] == 'gravel'and info['count_28'] > bound:
        g_patch.append(Polygon(np.asarray(shape),True))      
    if info['substrate'] == 'sand/rock'and info['count_28'] > bound:
        sr_patch.append(Polygon(np.asarray(shape),True))         
    if info['substrate'] == 'rock'and info['count_28'] > bound:
        r_patch.append(Polygon(np.asarray(shape),True))  
        
ax.add_collection(PatchCollection(s_patch, facecolor = colors[4],alpha=a_val, edgecolor='none',zorder=10))
ax.add_collection(PatchCollection(sg_patch, facecolor = colors[3],alpha=a_val, edgecolor='none',zorder=10))
ax.add_collection(PatchCollection(g_patch, facecolor = colors[2],alpha=a_val, edgecolor='none',zorder=10))   
ax.add_collection(PatchCollection(sr_patch, facecolor = colors[1],alpha=a_val, edgecolor='none',zorder=10)) 
ax.add_collection(PatchCollection(r_patch, facecolor = colors[0],alpha=a_val, edgecolor='none',zorder=10)) 

ax.legend((circ1, circ2, circ3,circ4,circ5),('rock','sand/rock','Gravel','Sand/Gravel','sand'),numpoints=1, loc='best')

print 'Now plotting R02031 Acoustic Sediment Classifications...'
ax = plt.subplot2grid((5,2),(0, 1),rowspan=4)
ax.set_title('R02031 3 meter grid')
m = Basemap(projection='merc', 
            epsg=cs2cs_args.split(':')[1], 
            llcrnrlon=np.nanmin(r28_lon)-0.0004, 
            llcrnrlat=np.nanmin(r28_lat)-0.0004,
            urcrnrlon=np.nanmax(r28_lon)+0.0004, 
            urcrnrlat=np.nanmax(r28_lat)+0.0004)
m.wmsimage(server='http://grandcanyon.usgs.gov/arcgis/services/Imagery/ColoradoRiverImageryExplorer/MapServer/WmsServer?', layers=['3'], xpixels=1000)
x,y = m.projtran(r31_lon, r31_lat)
im = m.contourf(x,y,R02031.T, cmap='Greys_r',levels=ss_level)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
cbr = plt.colorbar(im, cax=cax)
m.readshapefile(r"C:\workspace\Reach_4a\Multibeam\mb_sed_class\output\shapefiles\may2014_3m_buff_geo","layer",drawbounds = False)

#sand, sand/gravel, gravel, sand/rock, rock
s_patch, sg_patch, g_patch, sr_patch, r_patch, = [],[],[],[],[]

bound = max(stat['count'] for stat in stats_31)/2
for info, shape in zip(m.layer_info, m.layer):
    if info['substrate'] == 'sand' and info['count_31'] > bound:
        s_patch.append(Polygon(np.asarray(shape),True))
    if info['substrate'] == 'sand/gravel' and info['count_31'] > bound:
        sg_patch.append(Polygon(np.asarray(shape),True))        
    if info['substrate'] == 'gravel'and info['count_31'] > bound:
        g_patch.append(Polygon(np.asarray(shape),True))      
    if info['substrate'] == 'sand/rock'and info['count_31'] > bound:
        sr_patch.append(Polygon(np.asarray(shape),True))         
    if info['substrate'] == 'rock'and info['count_31'] > bound:
        r_patch.append(Polygon(np.asarray(shape),True))  
        
ax.add_collection(PatchCollection(s_patch, facecolor = colors[4],alpha=a_val, edgecolor='none',zorder=10))
ax.add_collection(PatchCollection(sg_patch, facecolor = colors[3],alpha=a_val, edgecolor='none',zorder=10))
ax.add_collection(PatchCollection(g_patch, facecolor = colors[2],alpha=a_val, edgecolor='none',zorder=10))   
ax.add_collection(PatchCollection(sr_patch, facecolor = colors[1],alpha=a_val, edgecolor='none',zorder=10)) 
ax.add_collection(PatchCollection(r_patch, facecolor = colors[0],alpha=a_val, edgecolor='none',zorder=10)) 

ax.legend((circ1, circ2, circ3,circ4,circ5),('rock','sand/rock','Gravel','Sand/Gravel','sand'),numpoints=1, loc='best')

print 'Now plotting focal statistics...'
ax = plt.subplot2grid((5,2),(4, 0))
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
for sp in ax.spines.itervalues():
    sp.set_color('w')
    sp.set_zorder(0)
the_table = table(ax, pivot_table_28.round(3),loc='best',colWidths=[0.1,0.1,0.1,0.1,0.1,0.1,0.1])

ax = plt.subplot2grid((5,2),(4, 1))
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
for sp in ax.spines.itervalues():
    sp.set_color('w')
    sp.set_zorder(0)
the_table = table(ax, pivot_table_31.round(3),loc='best',colWidths=[0.1,0.1,0.1,0.1,0.1,0.1,0.1])

plt.tight_layout()
#plt.show()
print 'Now Saving figure...'
plt.savefig(r"C:\workspace\Reach_4a\Multibeam\mb_sed_class\output\mb_sed_class_ground_truth_3m_full_polygon.png",dpi=1000)


