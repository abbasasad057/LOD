"""
Created on Fri Feb 03 12:04:07 2017
@author: ASAD
--------------------------------------------------------------------------------------
This code uses GDAL and OGR to generate LOD1 from DSM and DTM data.
--------------------------------------------------------------------------------------
"""
from osgeo import gdal,ogr
import numpy as np
import os
#%%
'''
Getting data filenames from specified path 
'''
def filenames(path):
    """
    Returns all filenames in specified directory.
    Input arguments:
        path = Name of the folder or directory from which filenames are to be read
    Usage:
        names = filenames('drive:/directory')
    """
    return os.listdir(path) # To get name of all the files stored in given directory
#%%
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
#%%
'''
Removing no data values and creating BnDSM
'''
def bAndnDSM(DSM,noDataValDSM,DTM,noDataValDTM,binThreshold):
    """
    Creates BnDSM and nDSM from DSM and DTM.
    Input arguments:
        DSM = DSM raster array
        noDataValDSM = No data value of DSM
        DTM = DTM raster array.
        noDataValDTM = No data value of DTM
        binThreshold = Height threshold to get BnDSM.
    Returns:
        nDSM = Normalized DSM
        BnDSM = Binary nDSM
    Usage:
        nDSM,BnDSM = bAndnDSM(DSM,noDataValDSM,DTM,noDataValDTM,binThreshold)
    """
    DSM=np.where(DSM>=noDataValDSM,np.nan,DSM) # replacing nodata with NAN
    DTM=np.where(DTM>=noDataValDTM,np.nan,DTM) # replacing nodata with NAN
    nDSM=DSM-DTM# Calculating nDSM
    BnDSM=np.greater(nDSM,binThreshold) 
    return (nDSM,BnDSM)# Creating a binary raster by using height threshold on nDSM. 
#%%
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
#%%

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
#%%
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
#%%
"""
Zonal Statistics
Vector-Raster Analysis
Copyright 2013 Matthew Perry
Usage:
  zonal_stats.py VECTOR RASTER
  zonal_stats.py -h | --help
  zonal_stats.py --version
Options:
  -h --help     Show this screen.
  --version     Show version.
"""
gdal.PushErrorHandler('CPLQuietErrorHandler')


def bbox_to_pixel_offsets(gt, bbox):
    originX = gt[0]
    originY = gt[3]
    pixel_width = gt[1]
    pixel_height = gt[5]
    x1 = int((bbox[0] - originX) / pixel_width)
    x2 = int((bbox[1] - originX) / pixel_width) + 1

    y1 = int((bbox[3] - originY) / pixel_height)
    y2 = int((bbox[2] - originY) / pixel_height) + 1

    xsize = x2 - x1
    ysize = y2 - y1
    return (x1, y1, xsize, ysize)


def zonal_stats(vector_path, raster_path, nodata_value=None, global_src_extent=False):
    rds = gdal.Open(raster_path)
    assert(rds)
    rb = rds.GetRasterBand(1)
    rgt = rds.GetGeoTransform()

    if nodata_value:
        nodata_value = float(nodata_value)
        rb.SetNoDataValue(nodata_value)

    vds = ogr.Open(vector_path)  # TODO maybe open update if we want to write stats
    assert(vds)
    vlyr = vds.GetLayer(0)

    # create an in-memory numpy array of the source raster data
    # covering the whole extent of the vector layer
    if global_src_extent:
        # use global source extent
        # useful only when disk IO or raster scanning inefficiencies are your limiting factor
        # advantage: reads raster data in one pass
        # disadvantage: large vector extents may have big memory requirements
        src_offset = bbox_to_pixel_offsets(rgt, vlyr.GetExtent())
        src_array = rb.ReadAsArray(*src_offset)

        # calculate new geotransform of the layer subset
        new_gt = (
            (rgt[0] + (src_offset[0] * rgt[1])),
            rgt[1],
            0.0,
            (rgt[3] + (src_offset[1] * rgt[5])),
            0.0,
            rgt[5]
        )

    mem_drv = ogr.GetDriverByName('Memory')
    driver = gdal.GetDriverByName('MEM')

    # Loop through vectors
    stats = []
    feat = vlyr.GetNextFeature()
    while feat is not None:

        if not global_src_extent:
            # use local source extent
            # fastest option when you have fast disks and well indexed raster (ie tiled Geotiff)
            # advantage: each feature uses the smallest raster chunk
            # disadvantage: lots of reads on the source raster
            src_offset = bbox_to_pixel_offsets(rgt, feat.geometry().GetEnvelope())
            src_array = rb.ReadAsArray(*src_offset)

            # calculate new geotransform of the feature subset
            new_gt = (
                (rgt[0] + (src_offset[0] * rgt[1])),
                rgt[1],
                0.0,
                (rgt[3] + (src_offset[1] * rgt[5])),
                0.0,
                rgt[5]
            )

        # Create a temporary vector layer in memory
        mem_ds = mem_drv.CreateDataSource('out')
        mem_layer = mem_ds.CreateLayer('poly', None, ogr.wkbPolygon)
        mem_layer.CreateFeature(feat.Clone())

        # Rasterize it
        rvds = driver.Create('', src_offset[2], src_offset[3], 1, gdal.GDT_Byte)
        rvds.SetGeoTransform(new_gt)
        gdal.RasterizeLayer(rvds, [1], mem_layer, burn_values=[1])
        rv_array = rvds.ReadAsArray()

        # Mask the source data array with our current feature
        # we take the logical_not to flip 0<->1 to get the correct mask effect
        # we also mask out nodata values explictly
        masked = np.ma.MaskedArray(
            src_array,
            mask=np.logical_or(
                src_array == nodata_value,
                np.logical_not(rv_array)
            )
        )

        feature_stats = {
            'mean': float(masked.mean()),
            'count': int(masked.count()),
            'fid': int(feat.GetFID())}

        stats.append(feature_stats)

        rvds = None
        mem_ds = None
        feat = vlyr.GetNextFeature()

    vds = None
    rds = None
    return stats