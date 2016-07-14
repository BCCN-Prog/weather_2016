import QueryEngine
import sys
import os

os.system('rm daily_database.hdf5')
os.system('rm hourly_database.hdf5')
os.system('rm cached_data.h5py')
os.system('rm cachedict.p')

q = QueryEngine.QueryEngine("daily_database.hdf5", "hourly_database.hdf5", make_new=True)
