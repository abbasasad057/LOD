# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 09:24:23 2017

@author: ASAD
"""
from osgeo import gdal,ogr
def PolygonizeBnDSM(BnDSM,OutputLocation):
    """
    To extract building foot prints using BnDSM.
    
    Input arguments:
        BnDSM = Binary nDSM can be obtained by bAndnDSM() function
        OutputLocation = Complete path of output file including filename
    """
    maskBand=BnDSM
    dst_layername = OutputLocation
    drv = ogr.GetDriverByName("ESRI Shapefile")
    dst_ds = drv.CreateDataSource( dst_layername + ".shp" ,)
    dst_layer = dst_ds.CreateLayer(dst_layername,geom_type=ogr.wkbPolygon)
    gdal.Polygonize(maskBand,maskBand, dst_layer,0)
    featureDefn = dst_layer.GetLayerDefn()
    feature = ogr.Feature(featureDefn)
    dst_layer.CreateFeature(feature)
    feature.Destroy()
    dst_ds.Destroy()