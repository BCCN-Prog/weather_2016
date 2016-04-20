from bs4 import BeautifulSoup
import requests
import pudb

CITIES = ['berlin-18228265', 'muenchen-18225562', 'hamburg', 'cologne', 'frankfurt', 'stuttgart', 'bremen', 'leipzig', 'hanover', 'nuremberg', 'dortmund', 'dresden', 'kassel', 'kiel', 'bielfeld', 'saarbrücken', 'rostock', 'magdeburg', 'freiburg', 'erfurt']


HOURLY_URL = 'http://www.wetter.de/deutschland/wetter-' + CITIES[0] + '/wetterbericht-aktuell.html'
FIFTEEN_URL = 'http://www.wetter.de/deutschland/wetter-' + CITIES[0] + '/wetterprognose.html'


pu.db

r = requests.get(HOURLY_URL)

soup = BeautifulSoup(r.content)
title = soup.title

day_forecast = soup.findAll("div", {"class":"forecast-day"})

hour_forecast = soup.findAll("div", {"class":"column column-4 forecast-detail-column-1h"})


r = requests.get(FIFTEEN_URL)

soup = BeautifulSoup(r.content)
title = soup.title

days_forecast = soup.findAll("div", {"class":"forecast-item-day"})


print('FIN')
