from query_engine import QueryEngine
import sys
sys.path.append('../')
from visualization import station_map
import numpy as np

#mock_latlon = 

latlong_dict = {'berlin': np.array([[52.31, 13.23], [45.9664, 8.3268]])}
city_dict = {'berlin': 91}
param_dict = {'high': 3, 'low': 4}

print('Welcome to the command line interface of the weather project')
loc = input('Location: ')
date_time = input('Date (+Time): ')
hourly_daily = input('Hourly or Daily Data?: ')
historical_scraping = input('Historical or Scraping Data?: ')
parameters = input('Which parameters?: ')

#loc = 'berlin'
#date_time = 20160412
#hourly_daily = 'd'
#historical_scraping = 'h'
#parameters = 'high'

qe = QueryEngine()

#loc = city_dict[loc]
#parameters = param_dict[parameters]

data = qe.get_data_point(loc, date_time, hourly_daily, historical_scraping, parameters)

print('...')
print('...')
print('...')
print('result:', data)

#geo_locations = get_geo_locations()[:2,:]
#print (geo_locations)
#print(geo_locations.shape)

#geo_locations = latlong_dict[loc]
#print(geo_locations)

geo_locations = latlong_dict[loc]

station_map(geo_locations, np.ones(geo_locations.shape[0]) * data, hex_grid_size=(2,2))

