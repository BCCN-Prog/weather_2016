# -*- coding: utf-8 -*-
# Downloading timeanddate.com/weather
import urllib.request
import time

# list fo all cities we are scraping from
CITIES = ['berlin', 'munich', 'hamburg', 'cologne', 'frankfurt', 'stuttgart', 'bremen',
          'leipzig', 'hannover', 'nuremberg', 'dortmund', 'dresden', 'kassel', 'kiel',
          'bielefeld', 'saarbrucken', 'rostock', 'magdeburg', 'freiburg', 'erfurt']

# loop over all cities
for city in CITIES:
    # construct url from city name and city ID, build filenname
    cityUrl1 = 'http://www.timeanddate.com/weather/germany/' + city + '/hourly'
    filename1 = "timeanddate_com_" + time.strftime("%d-%m-%Y_") + city + "_hourly.html"
    cityUrl2 = 'http://www.timeanddate.com/weather/germany/' + city + '/ext'
    filename2 = "timeanddate_com_" + time.strftime("%d-%m-%Y_") + city + "_daily.html"
    # download and save html file with given url and filename
    try:
        urllib.request.urlretrieve(cityUrl1, filename1)
    except:
        print(city)
    try:
        urllib.request.urlretrieve(cityUrl2, filename2)
    except:
        print(city)
