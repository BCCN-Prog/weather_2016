import QueryEgine
import sys
import os

q = QueryEngine.QueryEngine("daily_database.hdf5", "houry_database.hdf5", make_new=True)
os.system('rm cached_data.h5py')
os.system('rm cachedict.p')

