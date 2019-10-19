# -*- coding: utf-8 -*-
"""
Created on Sun May 21 17:57:56 2017
@author: ASAD
-----------------------------------------------------------------------------------
This code uses GDAL and OGR to generate LOD1 from DSM and DTM data.
-----------------------------------------------------------------------------------
"""
from osgeo import gdal,ogr,osr
import numpy as np
import os
import time
import ZonalStats as zs
#%%
'''
Getting data filenames from specified path 
'''
t0=time.time() #Note the initial time.
path="Path/to/DSM" # Path where DSM and DTM are stored
listing=os.listdir(path) # To get name of all the files stored in given directory
#%%
'''
Reading DSM
'''
dsm = gdal.Open(path+listing[0]) # opening DSM
cols1 = dsm.RasterXSize # getting number of columns
rows1 = dsm.RasterYSize # getting number of rows
bands1 = dsm.RasterCount # counting number of bands in a raster
band1=dsm.GetRasterBand(1) # getting 1st raster band
dataDSM=band1.ReadAsArray(0, 0, cols1, rows1) # reading raster as array
print dsm.GetMetadata() # printing meta data
#%%
'''
Reading DTM
'''
dtm = gdal.Open(path+listing[1])# opening DTM
cols2 = dtm.RasterXSize # getting number of columns
rows2 = dtm.RasterYSize # getting number of rows
bands2 = dtm.RasterCount # counting number of bands in a raster
band2=dtm.GetRasterBand(1) # getting 1st raster band
dataDTM=band2.ReadAsArray(0, 0, cols2,rows2) # reading raster as array
print dtm.GetMetadata() # printing meta data
#%%
'''
Removing no data values and creating BnDSM
'''
DSM=np.where(dataDSM>=9999.000,np.nan,dataDSM) # replacing 9999.000 with NAN
nDSM=DSM-dataDTM# Calculating nDSM
BnDSM=np.greater(nDSM,10) # Creating a binary raster by using height threshold on nDSM. 
#%%
'''
Writing DSM to file
'''
driver = dsm.GetDriver() # Getting same driver as DSM
outDataset = driver.Create("E:/Internship/gdalPractice/PracticeData/BnDSM.tif", cols1,rows1, 1)#Creating Output Dataset
outBand = outDataset.GetRasterBand(1) # Specifying band to which data is written
geoTransform = dsm.GetGeoTransform() # getting geometric transformation information from dsm
outDataset.SetGeoTransform(geoTransform) # setting geometric transformation of output data to be same as DSM
outBand.WriteArray(BnDSM,0,0) # Writing binary raster to specified file.
outBand =None # cleaning up the memory
outDataset=None # cleaning up the memory
#%%
'''
Writing DTM to file
'''
outDataset = driver.Create("path/to/nDSM.tif", cols1,rows1, 1)#Creating Output Dataset
outBand = outDataset.GetRasterBand(1)# Specifying band to which data is written
geoTransform = dsm.GetGeoTransform() # getting geometric transformation information from dsm
outDataset.SetGeoTransform(geoTransform ) # setting geometric transformation of output data to be same as DSM
outBand.WriteArray(nDSM,0,0) # Writing nDSM to specified file.
outBand =None # cleaning up the memory
outDataset=None # cleaning up the memory
#%%
'''
Reading nDSM and BnDSM
'''
mask=gdal.Open("oath/to/BnDSM.tif") # Reading mask data
maskBand=mask.GetRasterBand(1) # mask raster band
#%%
'''
Creating empty shapefile
'''
dst_layername = "path/to/POLYGONIZED_BnDSM"
drv = ogr.GetDriverByName("ESRI Shapefile")
dst_ds = drv.CreateDataSource( dst_layername + ".shp")
dst_layer = dst_ds.CreateLayer(dst_layername,geom_type=ogr.wkbPolygon)
#%%
'''
Creating empty fields
'''
#dst_fieldname = 'Elevation'
#fd = ogr.FieldDefn( dst_fieldname, ogr.OFTInteger )
#dst_layer.CreateField(fd)
#%%
'''
Polygonize the raster
'''
gdal.Polygonize(maskBand,maskBand, dst_layer,1)
#%%
'''
Writing polygonized data
'''
featureDefn = dst_layer.GetLayerDefn()
feature = ogr.Feature(featureDefn)
dst_layer.CreateFeature(feature)
feature.Destroy()
dst_ds.Destroy()
vpath="/to/path/POLYGONIZED_BnDSM.shp" # Reading mask data
rpath="path/to/nDSM.tif" # Reading nDSM
stats=zs.zonal_stats(vpath,rpath)
######Writing Stats##############
ds=ogr.Open("path/to/POLYGONIZED_BnDSM.shp",update=1)
out_layer=ds.GetLayer()
out_fld=ogr.FieldDefn("Mean",ogr.OFTReal)
out_layer.CreateField(out_fld)
out_layer.GetFeature
#out_feat=out_layer.GetFeature()
for i in range(len(stats)):
    out_feat=out_layer.GetFeature(i)
    out_feat.SetField("Mean",stats[i])
    out_layer.SetFeature(out_feat)
len(stats)
out_layer.CreateFeature(out_feat)
out_feat.Destroy()
ds.Destroy()
t1=time.time()
print(str(t1-t0)+"s")
