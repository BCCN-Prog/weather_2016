#def get_data(*args):
#    print(args)

import sys
sys.path.append('/home/pythonproject/Weather_project/weather_2016/query_engine_v2')

import QueryEngine
print("1")
q = QueryEngine.QueryEngine()#(make_new=True, loading_path="/home/pythonproject/Schreibtisch/weatherdata/")

print("2")
s = q.smart_slice('daily', ['station_id', 'temperature'], 'date', 20160101, 20160101)

print(q.get_data('daily', s, ['station_id', 'temperature']))
