# -*- coding: utf-8 -*-

import urllib.request
import time
import os.path

# list fo all cities we are scraping from
CITIES = ['berlin', 'munich', 'hamburg', 'cologne', 'frankfurt', 'stuttgart', 'bremen',
          'leipzig', 'hannover', 'nuremberg', 'dortmund', 'dresden', 'kassel', 'kiel',
          'bielefeld', 'saarbrucken', 'rostock', 'magdeburg', 'freiburg', 'erfurt']

def download(datafolder):
    ''' Downloading html pages for 20 cities from timeanddate.com/weather into datafolder'''

    for city in CITIES:
        # construct url from city name and city ID, build filenname
        cityUrl1 = 'http://www.timeanddate.com/weather/germany/' + city + '/hourly'
        filename1 = os.path.join(datafolder,"timeanddate_com_" + time.strftime("%d_%m_%Y_%H_%M_") + city + "_hourly.html")
        cityUrl2 = 'http://www.timeanddate.com/weather/germany/' + city + '/ext'
        filename2 = os.path.join(datafolder,"timeanddate_com_" + time.strftime("%d_%m_%Y_%H_%M_") + city + "_daily.html")
        # download and save html file with given url and filename
        try:
            urllib.request.urlretrieve(cityUrl1, filename1)
            urllib.request.urlretrieve(cityUrl2, filename2)
        except:
            print(city)
