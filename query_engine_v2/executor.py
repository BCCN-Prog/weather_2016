def get_data(*args):
    print("hi")
#    print(args)


#Stuff below here will be put into get_data function once stuff is working.

import sys
sys.path.append('../visualization')#'/home/pythonproject/Weather_project/weather_2016/visualization')
sys.path.append('../query_engine_v2')
import map_functions as mf
import QueryEngine as qe


q = qe.QueryEngine()#(make_new=True, loading_path="/home/pythonproject/Schreibtisch/weatherdata/")

s = q.smart_slice('daily', ['station_id', 'temperature'], 'date', 20160101, 20160101)

print(q.get_data('daily', s, ['station_id', 'temperature']))
