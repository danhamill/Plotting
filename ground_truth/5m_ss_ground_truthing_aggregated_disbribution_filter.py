# -*- coding: utf-8 -*-
"""
Created on Mon Oct 03 10:08:09 2016

@author: dan
"""

from rasterstats import zonal_stats
import pandas as pd
import numpy as np
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
    
def make_df2(x):
    df = pd.DataFrame(x,columns=['dBW'])
    return df

#Sidescan sonar imagery
ss_r28 = r"C:\workspace\Reach_4a\Multibeam\mb_sed_class\output\ss_R02028.tif"
ss_r31 = r"C:\workspace\Reach_4a\Multibeam\mb_sed_class\output\ss_R02031.tif"

#Buffered points
buff_shp = r"C:\workspace\Reach_4a\Multibeam\mb_sed_class\output\shapefiles\may2014_5m_buff.shp"

#Resampled sed5Class
sed_pts = r"C:\workspace\Reach_4a\Multibeam\mb_sed_class\may2014_mb6086r_sedclass\xy_sed5class_5m.csv"

#Read points
pts_df = pd.read_csv(sed_pts,sep=',',names=['northing','easting','sed5class'])
pts_df['sed5class'] = pts_df.apply(lambda row: assign_class(row), axis = 1)

#Calculate Zonal statistics for aggregrated distributions
z_stats_28 = zonal_stats(buff_shp, ss_r28, stats=['count','mean'], raster_out=True)
bound = max(stat['count'] for stat in z_stats_28)
s, sg, g, sr, r = [],[],[],[],[]
n = 0
for item in z_stats_28:
    raster_array = item['mini_raster_array'].compressed()
    substrate = pts_df['sed5class'][n]
    if substrate=='sand' and item['count']==bound and item['mean']<15:
        s.extend(list(raster_array))
    if substrate=='sand/gravel' and item['count']==bound and item['mean']<15:
        sg.extend(list(raster_array))
    if substrate=='gravel' and item['count']==bound and item['mean']<20:
        g.extend(list(raster_array))
    if substrate=='sand/rock' and item['count']==bound and item['mean']<20:
        sr.extend(list(raster_array))
    if substrate=='rock' and item['count']==bound and item['mean']<20:
        r.extend(list(raster_array))
    n+=1
del raster_array, substrate, n, item, bound

s_df = make_df2(s)
sg_df = make_df2(sg)
g_df = make_df2(g)
sr_df = make_df2(sr)
r_df = make_df2(r)
del s, sg, g, sr, r
        
tbl_28 = pd.DataFrame(columns=['substrate','mean','std','CV','25%','50%','75%','kurt','skew'])
tbl_28['substrate']=['sand','sand/gravel','gravel','sand/rock','rock']
tbl_28 = tbl_28.set_index('substrate')
tbl_28.loc['sand'] = pd.Series({'mean':np.mean(s_df['dBW']),'std':np.std(s_df['dBW']) ,'CV':np.mean(s_df['dBW'])/np.std(s_df['dBW']),'25%':float(s_df.describe().iloc[4].values), '50%':float(s_df.describe().iloc[5].values),'75%':float(s_df.describe().iloc[6].values),'kurt':float(s_df.kurtosis().values),'skew':float(s_df.skew().values)})
tbl_28.loc['sand/gravel'] = pd.Series({'mean':np.mean(sg_df['dBW']),'std':np.std(sg_df['dBW']) ,'CV':np.mean(sg_df['dBW'])/np.std(sg_df['dBW']),'25%':float(sg_df.describe().iloc[4].values), '50%':float(sg_df.describe().iloc[5].values),'75%':float(sg_df.describe().iloc[6].values),'kurt':float(sg_df.kurtosis().values),'skew':float(sg_df.skew().values)})
tbl_28.loc['gravel'] = pd.Series({'mean':np.mean(g_df['dBW']),'std':np.std(g_df['dBW']) ,'CV':np.mean(g_df['dBW'])/np.std(g_df['dBW']),'25%':float(g_df.describe().iloc[4].values), '50%':float(g_df.describe().iloc[5].values),'75%':float(g_df.describe().iloc[6].values),'kurt':float(g_df.kurtosis().values),'skew':float(g_df.skew().values)})
#tbl_28.loc['sand/rock'] = pd.Series({'mean':np.mean(sr_df['dBW']),'std':np.std(sr_df['dBW']) ,'CV':np.mean(sr_df['dBW'])/np.std(sr_df['dBW']),'25%':float(sr_df.describe().iloc[4].values), '50%':float(sr_df.describe().iloc[5].values),'75%':float(sr_df.describe().iloc[6].values),'kurt':float(sr_df.kurtosis().values),'skew':float(sr_df.skew().values)})
tbl_28.loc['rock'] = pd.Series({'mean':np.mean(r_df['dBW']),'std':np.std(r_df['dBW']) ,'CV':np.mean(r_df['dBW'])/np.std(r_df['dBW']),'25%':float(r_df.describe().iloc[4].values), '50%':float(r_df.describe().iloc[5].values),'75%':float(r_df.describe().iloc[6].values),'kurt':float(r_df.kurtosis().values),'skew':float(r_df.skew().values)})
tbl_28 = tbl_28.applymap(lambda x: round(x,3))
del s_df, sg_df, g_df, sr_df, r_df

z_stats_31 = zonal_stats(buff_shp, ss_r31, stats=['count'], raster_out=True)
bound = max(stat['count'] for stat in z_stats_31)
s, sg, g, sr, r = [],[],[],[],[]
n = 0
for item in z_stats_31:
    raster_array = item['mini_raster_array'].compressed()
    substrate = pts_df['sed5class'][n]
    if substrate=='sand' and item['count']==bound:
        s.extend(list(raster_array))
    if substrate=='sand/gravel' and item['count']==bound:
        sg.extend(list(raster_array))
    if substrate=='gravel' and item['count']==bound:
        g.extend(list(raster_array))
    if substrate=='sand/rock' and item['count']==bound:
        sr.extend(list(raster_array))
    if substrate=='rock' and item['count']==bound:
        r.extend(list(raster_array))
    n+=1
del raster_array, substrate, n, item

s_df = make_df2(s)
sg_df = make_df2(sg)
g_df = make_df2(g)
sr_df = make_df2(sr)
r_df = make_df2(r)

del s, sg, g, sr, r
        
tbl_31 = pd.DataFrame(columns=['substrate','mean','std','CV','25%','50%','75%','kurt','skew'])
tbl_31['substrate']=['sand','sand/gravel','gravel','sand/rock','rock']
tbl_31 = tbl_31.set_index('substrate')
tbl_31.loc['sand'] = pd.Series({'mean':np.mean(s_df['dBW']),'std':np.std(s_df['dBW']) ,'CV':np.mean(s_df['dBW'])/np.std(s_df['dBW']),'25%':float(s_df.describe().iloc[4].values), '50%':float(s_df.describe().iloc[5].values),'75%':float(s_df.describe().iloc[6].values),'kurt':float(s_df.kurtosis().values),'skew':float(s_df.skew().values)})
tbl_31.loc['sand/gravel'] = pd.Series({'mean':np.mean(sg_df['dBW']),'std':np.std(sg_df['dBW']) ,'CV':np.mean(sg_df['dBW'])/np.std(sg_df['dBW']),'25%':float(sg_df.describe().iloc[4].values), '50%':float(sg_df.describe().iloc[5].values),'75%':float(sg_df.describe().iloc[6].values),'kurt':float(sg_df.kurtosis().values),'skew':float(sg_df.skew().values)})
tbl_31.loc['gravel'] = pd.Series({'mean':np.mean(g_df['dBW']),'std':np.std(g_df['dBW']) ,'CV':np.mean(g_df['dBW'])/np.std(g_df['dBW']),'25%':float(g_df.describe().iloc[4].values), '50%':float(g_df.describe().iloc[5].values),'75%':float(g_df.describe().iloc[6].values),'kurt':float(g_df.kurtosis().values),'skew':float(g_df.skew().values)})
#tbl_31.loc['sand/rock'] = pd.Series({'mean':np.mean(sr_df['dBW']),'std':np.std(sr_df['dBW']) ,'CV':np.mean(sr_df['dBW'])/np.std(sr_df['dBW']),'25%':float(sr_df.describe().iloc[4].values), '50%':float(sr_df.describe().iloc[5].values),'75%':float(sr_df.describe().iloc[6].values),'kurt':float(sr_df.kurtosis().values),'skew':float(sr_df.skew().values)})
tbl_31.loc['rock'] = pd.Series({'mean':np.mean(r_df['dBW']),'std':np.std(r_df['dBW']) ,'CV':np.mean(r_df['dBW'])/np.std(r_df['dBW']),'25%':float(r_df.describe().iloc[4].values), '50%':float(r_df.describe().iloc[5].values),'75%':float(r_df.describe().iloc[6].values),'kurt':float(r_df.kurtosis().values),'skew':float(r_df.skew().values)})
tbl_31 = tbl_31.applymap(lambda x: round(x,3))
del s_df, sg_df, g_df, sr_df, r_df

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
ax.set_title('R02028: 5 meter grid')
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
m.readshapefile(r"C:\workspace\Reach_4a\Multibeam\mb_sed_class\output\shapefiles\may2014_5m_buff_geo","layer",drawbounds = False)
#sand, sand/gravel, gravel, sand/rock, rock
s_patch, sg_patch, g_patch, sr_patch, r_patch, = [],[],[],[],[]
bound = max(stat['count'] for stat in z_stats_28)
n=0
for info, shape in zip(m.layer_info, m.layer):
    if info['substrate'] == 'sand' and info['count_28'] == bound and z_stats_28[n]['mean']<15:
        s_patch.append(Polygon(np.asarray(shape),True))
    if info['substrate'] == 'sand/gravel' and info['count_28'] == bound and z_stats_28[n]['mean']<15:
        sg_patch.append(Polygon(np.asarray(shape),True))        
    if info['substrate'] == 'gravel'and info['count_28'] == bound and z_stats_28[n]['mean']<20:
        g_patch.append(Polygon(np.asarray(shape),True))      
    if info['substrate'] == 'sand/rock'and info['count_28'] == bound and z_stats_28[n]['mean']<20:
        sr_patch.append(Polygon(np.asarray(shape),True))         
    if info['substrate'] == 'rock'and info['count_28'] == bound and z_stats_28[n]['mean']<20:
        r_patch.append(Polygon(np.asarray(shape),True))  
    n +=1
del info, shape, n, bound
        
ax.add_collection(PatchCollection(s_patch, facecolor = colors[4],alpha=a_val, edgecolor='none',zorder=10))
ax.add_collection(PatchCollection(sg_patch, facecolor = colors[3],alpha=a_val, edgecolor='none',zorder=10))
ax.add_collection(PatchCollection(g_patch, facecolor = colors[2],alpha=a_val, edgecolor='none',zorder=10))   
ax.add_collection(PatchCollection(sr_patch, facecolor = colors[1],alpha=a_val, edgecolor='none',zorder=10)) 
ax.add_collection(PatchCollection(r_patch, facecolor = colors[0],alpha=a_val, edgecolor='none',zorder=10)) 

ax.legend((circ1, circ2, circ3,circ4,circ5),('rock','sand/rock','gravel','sand/gravel','sand'),numpoints=1, loc='best')

print 'Now plotting R02031 Acoustic Sediment Classifications...'
ax = plt.subplot2grid((5,2),(0, 1),rowspan=4)
ax.set_title('R02031 5 meter grid')
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
m.readshapefile(r"C:\workspace\Reach_4a\Multibeam\mb_sed_class\output\shapefiles\may2014_5m_buff_geo","layer",drawbounds = False)

#sand, sand/gravel, gravel, sand/rock, rock
s_patch, sg_patch, g_patch, sr_patch, r_patch, = [],[],[],[],[]

bound = max(stat['count'] for stat in z_stats_31)
for info, shape in zip(m.layer_info, m.layer):
    if info['substrate'] == 'sand' and info['count_31'] == bound:
        s_patch.append(Polygon(np.asarray(shape),True))
    if info['substrate'] == 'sand/gravel' and info['count_31'] == bound:
        sg_patch.append(Polygon(np.asarray(shape),True))        
    if info['substrate'] == 'gravel'and info['count_31'] == bound:
        g_patch.append(Polygon(np.asarray(shape),True))      
    if info['substrate'] == 'sand/rock'and info['count_31'] == bound:
        sr_patch.append(Polygon(np.asarray(shape),True))         
    if info['substrate'] == 'rock'and info['count_31'] == bound:
        r_patch.append(Polygon(np.asarray(shape),True))  
del info, shape, bound      
ax.add_collection(PatchCollection(s_patch, facecolor = colors[4],alpha=a_val, edgecolor='none',zorder=10))
ax.add_collection(PatchCollection(sg_patch, facecolor = colors[3],alpha=a_val, edgecolor='none',zorder=10))
ax.add_collection(PatchCollection(g_patch, facecolor = colors[2],alpha=a_val, edgecolor='none',zorder=10))   
ax.add_collection(PatchCollection(sr_patch, facecolor = colors[1],alpha=a_val, edgecolor='none',zorder=10)) 
ax.add_collection(PatchCollection(r_patch, facecolor = colors[0],alpha=a_val, edgecolor='none',zorder=10)) 

ax.legend((circ1, circ2, circ3,circ4,circ5),('rock','sand/rock','gravel','sand/gravel','sand'),numpoints=1, loc='best')

print 'Now plotting focal statistics...'
ax = plt.subplot2grid((5,2),(4, 0))
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
for sp in ax.spines.itervalues():
    sp.set_color('w')
    sp.set_zorder(0)
the_table = table(ax, tbl_28.round(3),loc='best',colWidths=[0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1])
the_table.set_fontsize(12)
ax = plt.subplot2grid((5,2),(4, 1))
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
for sp in ax.spines.itervalues():
    sp.set_color('w')
    sp.set_zorder(0)
the_table = table(ax, tbl_31.round(3),loc='best',colWidths=[0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1])
the_table.set_fontsize(12)
plt.tight_layout()
#plt.show()
print 'Now Saving figure...'
plt.savefig(r"C:\workspace\Reach_4a\Multibeam\mb_sed_class\output\mb_sed_class_ground_truth_5m_agg_dist_filter.png",dpi=600)


