# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 09:30:19 2017

@author: ASAD
"""
import numpy as np
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