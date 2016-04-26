import urllib.request
import time
import os
from bs4 import BeautifulSoup 

#URL = ''
#savefile = ''
#
#urllib.request.urlretrieve(URL, savefile)

#page = urllib.request.urlopen(url)
#soup = BeautifulSoup(page)

"""
berlin/10178/weather-forecast/178087
munich/80331/weather-forecast/178086
hamburg/20095/weather-forecast/178556
cologne/50667/weather-forecast/180169
frankfurt/60311/weather-forecast/168720
stuttgart/70173/weather-forecast/167220
bremen/28195/weather-forecast/167950
leipzig/04109/weather-forecast/171240
hanover/30159/weather-forecast/169824
nuremberg/90402/weather-forecast/167559
dortmund/44137/weather-forecast/170370
dresden/01067/weather-forecast/171239
kassel/34117/weather-forecast/168717
kiel/24103/weather-forecast/171566
bielefeld/33602/weather-forecast/170367
saarbrucken/66111/weather-forecast/171212
rostock/18055/weather-forecast/169581
magdeburg/39104/weather-forecast/171293
freiburg-im-breisgau/79098/weather-forecast/167209
erfurt/99084/weather-forecast/171707
"""

CITY = 'Berlin'
PC = '10178'
ID = '178087'
TIME_RANGE = 'hourly'
TIMEVAR = '18'
datafolder = 'data/'

timestr = time.strftime("%d-%m-%Y_%H:%M_")
hourstr = time.strftime("%H")
#Hourly forecast

for n in range(4):
    HOUR = int(hourstr) + n*8
    url = 'http://slate-dev.accuweather.com/en/de/' + CITY + '/' + PC + '/' + 'hourly-weather-forecast/' + ID + '_pc?hour=' + str(HOUR)
    filename = 'accuweather_' + timestr + CITY + '_' + 'hourly_h' + str(HOUR) + ".html"
    savepath = os.path.join(datafolder, filename)
    urllib.request.urlretrieve(url, savepath)

#Daylie forecast

days = [i for i in range(1,18)] + [20,30,40,50,60,70,80,90]
print(days)

for DAY in days:
    url = 'http://slate-dev.accuweather.com/en/de/' + CITY + '/' + PC + '/' + 'daily-weather-forecast/' + ID + '_pc?day=' + str(DAY)
    filename = 'accuweather_' + timestr + CITY + '_' + 'daily_d' + str(DAY) + ".html"
    savepath = os.path.join(datafolder, filename)
    urllib.request.urlretrieve(url, savepath)


