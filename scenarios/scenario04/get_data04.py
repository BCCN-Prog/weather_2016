import sys
sys.path.append('../../')
sys.path.append('../../wrapper/')
from query_engine_v2 import QueryEngine

qe = QueryEngine.QueryEngine('../../databases/test_data/daily_database.hdf5', 
                             '../../databases/test_data/hourly_database.hdf5')
                            

