# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 09:27:14 2017

@author: ASAD
"""
import os
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