import urllib.request
import time
import os
from bs4 import BeautifulSoup 
import random

#          CITY                         PC      ID
STATION = [('berlin',                   '10178',  '178087'),
           ('munich',                   '80331',  '178086'),
           ('hamburg',                  '20095',  '178556'),
           ('cologne',                  '50667',  '180169'),
           ('frankfurt',                '60311',  '168720'),
           ('stuttgart',                '70173',  '167220'),
           ('bremen',                   '28195',  '167950'),
           ('leipzig',                  '04109',  '171240'),
           ('hanover',                  '30159',  '169824'),
           ('nuremberg',                '90402',  '167559'),
           ('dortmund',                 '44137',  '170370'),
           ('dresden',                  '01067',  '171239'),
           ('kassel',                   '34118',  '168717'),
           ('kiel',                     '24103',  '171566'),
           ('bielefeld',                '33602',  '170367'),
           ('saarbrucken',              '66111',  '171212'),
           ('rostock',                  '18055',  '169581'),
           ('magdeburg',                '39104',  '171293'),
           ('freiburg-im-breisgau',     '79098',  '167209'),
           ('erfurt',                   '99084',  '171707')
          ]


def download_html(datafolder):


    timestr = time.strftime("%d-%m-%Y_%H:%M")
    hourstr = time.strftime("%H")

    days = [i for i in range(1,18)] + [20,30,40,50,60,70,80,90]
    downloads_per_city = len(days)+4
    total_downloads = downloads_per_city * len(STATION)

    url_list = []

    for CITY, PC, ID in STATION:

        # Hourly forecast
        for n in range(4):
            
            HOUR = int(hourstr) + n*8
            url = 'http://slate-dev.accuweather.com/en/de/' + CITY + '/' + PC + '/' + 'hourly-weather-forecast/' + ID + '_pc?hour=' + str(HOUR)
            filename = 'accuweather_' + timestr + '_' + CITY + '_' + 'hourly_h' + str(HOUR) + '_' + str(int(time.time())) + ".html"
            savepath = os.path.join(datafolder, filename)

            url_list.append((url, savepath))
            
        
        # Daylie forecast
        
        for DAY in days:
            url = 'http://slate-dev.accuweather.com/en/de/' + CITY + '/' + PC + '/' + 'daily-weather-forecast/' + ID + '_pc?day=' + str(DAY)
            filename = 'accuweather_' + timestr + '_' + CITY + '_' + 'daily_d' + str(DAY) + '_' + str(int(time.time())) + ".html"
            savepath = os.path.join(datafolder, filename)

            url_list.append((url, savepath))

    random.shuffle(url_list)
    counter = 1
    print('Starting html downloads for accuweather.com:\n\n')
    for (url, savepath) in url_list:
        print('{}/{}'.format(counter, total_downloads))
        print('Downloading {}, starting at: {}.'.format(url, time.strftime('%H:%M:%S')))
        t1 = time.time()
        urllib.request.urlretrieve(url, savepath)
        print('Finished download after {:.2f}s\n\n'.format((time.time() - t1)/10))
        counter += 1

if __name__=='__main__':
    download_html('./data/')
