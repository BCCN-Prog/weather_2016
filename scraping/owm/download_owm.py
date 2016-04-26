# -*- coding: utf-8 -*-

import urllib.request
from time import strftime

base_url = 'http://openweathermap.org/city/{}'
base_path = 'output/owm_{}_{}.html'

cities = {'berlin': 2950159,
          'munich': 6940463,
          'hamburg': 2911298,
          'cologne': 6691073,
          'frankfurt': 2925533,
          'stuttgart': 2825297,
          'bremen': 2944388,
          'leipzig': 2879139,
          'hannover': 2910831,
          'nuremberg': 2861650,
          'dortmund': 2935517,
          'dresden': 2935022,
          'kassel': 2892518,
          'kiel': 2891122,
          'bielefeld': 2949186,
          'saarbrucken': 2842647,
          'rostock': 2844588,
          'magdeburg': 2874545,
          'freiburg': 2925177,
          'erfurt': 2929670}

def main():
    for city in cities:
        url = base_url.format(cities[city])
        path = base_path.format(strftime('%d_%m_%Y'), city)
        urllib.request.urlretrieve(url, filename=path)
    
    
    
