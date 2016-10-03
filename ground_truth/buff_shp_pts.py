# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 14:14:57 2016

@author: dan
"""

import ogr, os, csv, osr, shapely

def createBuffer(inputfn, outputBufferfn, bufferDist):
    inputds = ogr.Open(inputfn)
    inputlyr = inputds.GetLayer()

    shpdriver = ogr.GetDriverByName('ESRI Shapefile')
    if os.path.exists(outputBufferfn):
        shpdriver.DeleteDataSource(outputBufferfn)
    outputBufferds = shpdriver.CreateDataSource(outputBufferfn)
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(26949)
    
    #Create the Layer
    bufferlyr = outputBufferds.CreateLayer(outputBufferfn, srs, geom_type=ogr.wkbPolygon)
    field_name = ogr.FieldDefn('raw_sed5lass', ogr.OFTReal)
    bufferlyr.CreateField(field_name)
    
    featureDefn = bufferlyr.GetLayerDefn()

    for feature in inputlyr:
        #read input feature
        ingeom = feature.GetGeometryRef()
        a = feature.sed5class
        #buffer input feature
        geomBuffer = ingeom.Buffer(bufferDist)
        
        #Create feature in output shapefile
        outFeature = ogr.Feature(featureDefn)
        outFeature.SetField('raw_sed5lass',a)
        outFeature.SetGeometry(geomBuffer)
        bufferlyr.CreateFeature(outFeature)
        
def createShp(fIn,fOut):
    reader = csv.DictReader(open(fIn,"rb"), fieldnames=("X", "Y","sed5class"), delimiter=' ', quoting=csv.QUOTE_NONE)
    
    driver = ogr.GetDriverByName("ESRI Shapefile")    
    
    #create the data source
    ds = driver.CreateDataSource(fOut)
    # create the spatial reference, AZ Central SP
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(26949)
    
    # create the layer
    layer = ds.CreateLayer(fOut, srs, ogr.wkbPoint)
    
    # Add the fields we're interested in
    field_name = ogr.FieldDefn("X", ogr.OFTReal)
    layer.CreateField(field_name)
    layer.CreateField(ogr.FieldDefn("Y", ogr.OFTReal))
    layer.CreateField(ogr.FieldDefn("sed5class", ogr.OFTReal))
    print 'Now creating shapefile...'
    for row in reader:
        # create the feature
        feature = ogr.Feature(layer.GetLayerDefn())
        # Set the attributes using the values from the delimited text file
        feature.SetField("X", row['X'])
        feature.SetField("Y", row['Y'])
        feature.SetField("sed5class", row['sed5class'])
        
        # create the WKT for the feature using Python string formatting
        wkt = "POINT(%f %f)" %  (float(row['X']) , float(row['Y']))
    
        # Create the point from the Well Known Txt
        point = ogr.CreateGeometryFromWkt(wkt)
    
        # Set the feature geometry using the point
        feature.SetGeometry(point)
        # Create the feature in the layer (shapefile)
        layer.CreateFeature(feature)
    del ds, reader
def main(fIn, fOut, buff_fOut, bufferDist):
    createShp(fIn,fOut)
    print 'Sucessfully Created Shapefile'
    print 'Now Buffering Shapefile...'
    createBuffer(fOut, buff_fOut, bufferDist)

if __name__ == "__main__":
    
    fIn = r"C:\workspace\Reach_4a\Multibeam\mb_sed_class\output\may2014_3m.xyz"
    fOut = r"C:\workspace\Reach_4a\Multibeam\mb_sed_class\output\shapefiles\may2014_3m.shp"
    buff_fOut = r"C:\workspace\Reach_4a\Multibeam\mb_sed_class\output\shapefiles\may2014_3m_buff.shp"
    bufferDist = 1.5

    main(fIn, fOut, buff_fOut, bufferDist)
    
    

    
