#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
import time
import os
from bs4 import BeautifulSoup 
import random
import re

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

    days = [i for i in range(1,18)] + [30,50,70,90]
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
        print('Finished download after {:.2f}s\n\n'.format((time.time() - t1)))
        counter += 1

def convert_fahrenheit_to_celcius(fahrenheit):
    # TODO: something wrong here?
    fahrenheit = float(fahrenheit)
    celcius = (fahrenheit - 32.)/1.8
    return celcius


def scrape_html(html_file, data_dict):

#    site = os.path.splitext(os.path.basename(html_file))[0].split('_')[0]
#    date = os.path.splitext(os.path.basename(html_file))[0].split('_')[1]
#    time = os.path.splitext(os.path.basename(html_file))[0].split('_')[2]
#    city = os.path.splitext(os.path.basename(html_file))[0].split('_')[3]
    site, date, time, city, request_type, request_index, timestemp = os.path.splitext(os.path.basename(html_file))[0].split('_') 
    request_index = request_index[1:]
    print('EXTRACT FILENAME:')
    print(site, date, time, city, request_type, request_index, timestemp)


    ### dayly_save
    # TODO: check for list length before [0]
    soup = BeautifulSoup(open(html_file))

    daily = soup.find_all('div', id='detail-day-night')
    assert len(daily) == 1
    daily = daily[0]

    day = daily.find_all('div', class_='day')
    assert len(day) == 1
    day = day[0]




    night = daily.find_all('div', class_='night')
    assert len(night) == 1
    night = night[0]

    for cl in [day, night]:
        # TODO: check if there are multiple found

        high_temp_F_str = cl.find('span', class_='large-temp').get_text()
        high_temp_F = re.findall('\d+', high_temp_F_str)
        assert len(high_temp_F) == 1
        high_temp_C = convert_fahrenheit_to_celcius(high_temp_F[0])

        feel_temp_F_str = cl.find('span', class_='realfeel').get_text()
        feel_temp_F = re.findall('\d+', feel_temp_F_str)
        assert len(feel_temp_F) == 1
        feel_temp = convert_fahrenheit_to_celcius(feel_temp_F[0])

        precip_str = cl.find('span', class_='precip').get_text()
        precip = re.findall('\d+', precip_str)
        assert len(precip) == 1
        precip = precip[0]

        condition = cl.find('div', class_='cond').get_text().strip()

        print('high_temp', high_temp_C)
        print('feel_temp', feel_temp)
        print('precip', precip)
        print('condition', condition)


if __name__=='__main__':
    #download_html('./data/')
    scrape_html('../data/accuweather_03-05-2016_14:20_berlin_daily_d1_1462278002.html', {})
