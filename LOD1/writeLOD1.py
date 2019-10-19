# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 09:34:06 2017

@author: ASAD
"""

from osgeo import ogr,gdal
def writeLOD1(location,dataBand,maskBand,fieldName):
    """
    Writes LOD1 to specified path
    
    Input arugments:
        location = complete output location of LOD1 shapefile with name
        dataBand = nDSM band (This should not be array)
        maskBand = BnDSM band (This should not be array)
        fieldName = fieldName to which elevation data is written.
    Usage:
        writeLOD1(location,dataBand,maskBand,fieldName)
    """
    dst_layername = location
    drv = ogr.GetDriverByName("ESRI Shapefile")
    dst_ds = drv.CreateDataSource( dst_layername + ".shp")
    dst_layer = dst_ds.CreateLayer(dst_layername,geom_type=ogr.wkbPolygon)
# Creating new field
    fd = ogr.FieldDefn(fieldName,ogr.OFTInteger)
    dst_layer.CreateField(fd)
# Polygonize
    gdal.Polygonize(dataBand,maskBand, dst_layer,0)
# writing feature to shapefile
    featureDefn = dst_layer.GetLayerDefn()
    feature = ogr.Feature(featureDefn)
    dst_layer.CreateFeature(feature)
    feature.Destroy()
    dst_ds.Destroy()