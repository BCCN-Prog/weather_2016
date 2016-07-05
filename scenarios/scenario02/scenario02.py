# Scenario 02

import sys
sys.path.append('../')
sys.path.append('../wrapper/')
from query_engine_v2 import QueryEngine

qe_h = QueryEngine.QueryEngine('daily_database.hdf5',
                               'hourly_database.hdf5') # not using hourly DB for now



data_h = qe_h.smart_slice('daily', ['date', 'low', 'temperature','high'], 'site', 5, 5)


print(data_h[0].shape)
print()
print(data_h[1])
print()
print(data_h[0])