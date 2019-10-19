# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 09:32:26 2017

@author: ASAD
"""

'''
Writing Raster
'''
def writeRaster(location,Value,cols,rows):
    """
    Writes the raster to specified location.
    Input arguments:
        location = complete path with name of output raster
        Value = raster array
        cols = number of raster columns
        rows = number of raster rows
    Usage: 
        writeRaster(location,Value,cols,rows)
        
    """
    driver = Value.GetDriver() # Getting same driver as DSM
    outDataset = driver.Create(location,cols,rows,1)#Creating Output Dataset
    outBand = outDataset.GetRasterBand(1) # Specifying band to which data is written
    geoTransform = Value.GetGeoTransform()#getting geometric transformation information from dsm
    outDataset.SetGeoTransform(geoTransform) 
    outBand.WriteArray(Value,0,0) # Writing binary raster to specified file.
    outBand =None # cleaning up the memory
    outDataset=None # cleaning up the memory