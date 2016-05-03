# -*- coding: utf-8 -*-

#import urllib.request
import time
from selenium import webdriver  
from bs4 import BeautifulSoup

base_url = 'http://openweathermap.org/city/{}'
base_path = '{}owm_{}_{}.html'

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


def download(data_path):
    for city in cities:
        print('downloading html for {}'.format(city))
        url = base_url.format(cities[city])
        path = base_path.format(data_path, time.strftime('%d_%m_%Y_%H_%M'), city)
        browser = webdriver.Firefox()  
        browser.get(url)
        time.sleep(1)  
        content = browser.page_source
        browser.quit()
        soup = BeautifulSoup(content, 'lxml')
        print(soup.find(id='date_m'))
        html = soup.prettify("utf-8")
        print(path)
        with open(path, "wb") as file:
            file.write(html)

#def download_old(data_path):
 ##   for city in cities:
   #     url = base_url.format(cities[city])
    #    path = base_path.format(data_path, time.strftime('%d_%m_%Y_%H_%M'), city)
     #   urllib.request.urlretrieve(url, filename=path)
    
    
    
