# -*- coding: utf-8 -*-
#%%
"""
Created on Tue May 31 16:06:39 2016

@author: pythonproject
"""
import numpy as np
import sys
sys.path.append('../../')
from wrapper.DataWrapH5py import Daily_DataBase

ids = np.load("Stationidlist.npy")

def extract_heatmap():
    extract_data_point(self,91, 20160102, 'high')
    