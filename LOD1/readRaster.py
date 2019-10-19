# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 09:28:14 2017

@author: ASAD
"""
from osgeo import gdal
'''
Reading Raster
'''
def readRaster(path):
    """
    Reads raster from specified path and returns raster information.
    
    Input arguments:
        path = complete path of raster to be read including its name
    Returns:
        col = Number of raster columns
        row = Number of raster rows
        bandNum = Number of raster bands
        band = Raster band
        dataRaster = Raster band as array
        geotansform = Raster geometric transformation information
    Usage:
        col,row,bandNum,band,dataRaster,geotransform = readRaster('drive:/directory/raster')
    """
    raster = gdal.Open(path) # opening Raster
    col = raster.RasterXSize # getting number of columns
    row = raster.RasterYSize # getting number of rows
    bandNum= raster.RasterCount # counting number of bands in a raster
    geotransform = raster.GetGeoTransform()
#    originX = geotransform[0]
#    originY = geotransform[3]
#    pixelWidth = geotransform[1]
#    pixelHeight = geotransform[5]
    band=raster.GetRasterBand(1) # getting 1st raster band
    dataRaster=band.ReadAsArray(0, 0, col, row) # reading raster as array
    print raster.GetMetadata() # printing meta data
    return (col,row,bandNum,band,dataRaster,geotransform)