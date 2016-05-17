#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
import time
import os
from bs4 import BeautifulSoup 
import random
import re
import glob

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
            url = 'http://slate-dev.accuweather.com/en/de/' + CITY + '/' + PC + '/' + 'hourly-weather-forecast/' + ID + '?hour=' + str(HOUR)
            filename = 'accuweather_' + timestr + '_' + CITY + '_' + 'hourly_h' + str(HOUR) + '_' + str(int(time.time())) + ".html"
            savepath = os.path.join(datafolder, filename)

            url_list.append((url, savepath))
            
        
        # Daylie forecast
        
        for DAY in days:
            url = 'http://slate-dev.accuweather.com/en/de/' + CITY + '/' + PC + '/' + 'daily-weather-forecast/' + ID + '?day=' + str(DAY)
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


def find_unique(soup, **kwargs):
    """ Use BeautifulSoup.find_all() but throw AssertionError if multiple instances are found. """
    result = soup.find_all(**kwargs)
    assert len(result) == 1, 'None or multiple instances of {} were found in {}, found instances: {}.'.format(kwargs, soup.attrs, result)
    return result[0]


def parse_unique(pattern, string, **kwargs):
    """ Use re.findall() but throw AssersionError if multiple instances are found. """
    result = re.findall(pattern, string, **kwargs)
    assert len(result) == 1, 'None or multiple sets of {} found in {}, found instances: {}.'.format(pattern, string, result)
    return result[0]


#def scrape_html(html_file):

def scrape(date, city):

    daily_dict = {}
    hourly_dict = {}

    for html_file in glob.glob('./data/accuweather_' + date + '*' + city + '*.html'):

        site, date_, time, city_, request_type, request_index, timestemp = os.path.splitext(os.path.basename(html_file))[0].split('_') 
        request_index = request_index[1:]

        assert city == city_, "City name from function argument ({}) and from html filename ({}) are different!".format(city, city_)
        assert date == date_, "Date from function argument ({}) and from html filename ({}) are different!".format(date, date_)

        if request_type == 'daily':

            day_dict = {}

#    site = os.path.splitext(os.path.basename(html_file))[0].split('_')[0]
#    date = os.path.splitext(os.path.basename(html_file))[0].split('_')[1]
#    time = os.path.splitext(os.path.basename(html_file))[0].split('_')[2]
#    city = os.path.splitext(os.path.basename(html_file))[0].split('_')[3]
#    site, date, time, city, request_type, request_index, timestemp = os.path.splitext(os.path.basename(html_file))[0].split('_') 
#    request_index = request_index[1:]
            print('EXTRACT FILENAME:')
            print(site, date, time, city, request_type, request_index, timestemp)
        
        
            ### dayly_save
            soup = BeautifulSoup(open(html_file))
        
            daily = find_unique(soup, name='div', id='detail-day-night')
        
            day = find_unique(daily, name='div', class_='day')
            night = find_unique(daily, name='div', class_='night')
        
            keys = ['day', 'night']
            for j, cl in enumerate([day, night]):
        
                temp_str = find_unique(cl, name='span', class_='large-temp').get_text()
                temp = parse_unique('\d+', temp_str)
                if j==0:
                    key = 'high'
                else j==1:
                    key = 'low'
                day_dict[key] = float(temp)
        
                realfeel_str = find_unique(cl, name='span', class_='realfeel').get_text()
                realfeel = parse_unique('\d+', realfeel_str)
                day_dict['felt_' + keys[j]] = float(realfeel)
                
                precip_str = find_unique(cl, name='span', class_='precip').get_text()
                precip_chance = parse_unique('\d+', precip_str)
                day_dict['precipitation_chance_' + keys[j]] = float(precip_chance)
        
                cond = find_unique(cl, name='div', class_='cond').get_text().strip()
                day_dict['condition_' + keys[j]] = cond
        
                wind_stats = find_unique(cl, name='ul', class_='wind-stats')
        
                for strong in wind_stats.find_all('strong'):
                    strong_list = strong.get_text().split()
                    if len(strong_list) == 2:
                        gusts, unit = strong_list
                        assert unit == 'km/h', 'Unit of gusts is not km/h.'
                        day_dict['gusts_' + keys[j] + ' [m/s]'] = float(gusts) * 1e3 / 3600 # m/s
                    elif len(strong_list) == 3:
                        wind_direction, wind_speed, unit = strong_list
                        assert unit == 'km/h', 'Unit of wind speed is not km/h.'
                        day_dict['wind_direction_' + keys[j]] = wind_direction
                        day_dict['wind_speed_' + keys[j]] = float(wind_speed) * 1e3 / 3600 # m/s
                    else:
                        assert False, 'There is "strong" section in "wind_stats" that cant be identified.'
        
                stats = find_unique(cl, name='ul', class_='stats')
        
                stats_dic = {}
                for stat in stats.find_all('li'):
                    stat_list = stat.get_text().split()
                    if stat_list[0] == 'Thunderstorms:':
                        thunderstorm_chance = stat_list[1].rstrip('%')
                        day_dict['thunderstorm_chance_' + keys[j]] = float(thunderstorm_chance)
                    elif stat_list[0] == 'Precipitation:':
                        precip_amount = stat_list[1]
                        assert stat_list[2] == 'mm', 'Unit of precipitation amount is not mm.'
                        day_dict['precipitation_amount_' + keys[j]] = float(precip_amount)
                    elif stat_list[0] == 'Rain:':
                        rain_amount = stat_list[1]
                        assert stat_list[2] == 'mm', 'Unit of rain amount is not mm.'
                        day_dict['rain_amount_' + keys[j]] = float(rain_amount)
                    elif stat_list[0] == 'Snow:':
                        snow_amount = stat_list[1]
                        assert stat_list[2] == 'CM', 'Unit of snow amount is not cm.'
                        day_dict['snow_amount_' + keys[j]] = float(snow_amount)
                    elif stat_list[0] == 'Ice:':
                        ice_amount = stat_list[1]
                        assert stat_list[2] == 'mm', 'Unit of ice amount is not mm.'
                        day_dict['ice_amount_' + keys[j]] = float(ice_amount)
                    elif stat_list[1] == 'UV': #dont save max UV index
                        pass
                    elif stat_list[2] == 'Precipitation:':
                        precipitation_hours = stat_list[3]
                        assert stat_list[4] == 'hrs', 'Unit of hours of precipitation is not hrs.'
                        day_dict['precipitation_hours_' + keys[j]] = float(precipitation_hours)
                    elif stat_list[2] == 'Rain:':
                        rain_hours = stat_list[3]
                        assert stat_list[4] == 'hrs', 'Unit of hours of snow is not hrs.'
                        day_dict['rain_hours_' + keys[j]] = float(rain_hours)
                    else:
                        assert False, 'Unkown variable found in stats of daily forecast.'
            
            # rain_amnt and rain_chance average btwn day and night
            day_dict['rain_amt'] = (day_dict['rain_amount_day'] + day_dict['rain_amount_night']) / 2.
            day_dict['rain_chance'] = (day_dict['precipitation_chance_day'] + day_dict['precipitation_chance_night']) / 2.

            # request_index is hours since 12 midnight of day of recording
            daily_dict[request_index] = day_dict

            #print('temp', temp)
            #print('realfeel', realfeel)
            #print('precip', precip_chance)
            #print('cond', cond)
            #print('wind_direction', wind_direction)
            #print('wind_speed', wind_speed)
            #print('gutst', gusts)
            #print('thunderstorm_chance', thunderstorm_chance)
            #print('precip_amount', precip_amount)
            #print('rain_amount', rain_amount)
            #print('snow_amount', snow_amount)
            #print('ice_amount', ice_amount)
            #print('precipitation_hours', precipitation_hours)
            #print('rain_hours', rain_hours)
        
            #TODO: turn into correct dictionary


        elif request_type == 'hourly':  
            #TODO

    data_dict = {'site'     :   'accuweather',
                 'city'     :   city,
                 'date'     :   date
                 'hourly'   :   {}
                 'daily'    :
        

if __name__=='__main__':
    #download_html('../data/')
    #scrape_html('/home/denis/Documents/Uni/project_software_carpentry/weather_2016/scraping/data/accuweather_10-05-2016_16:33_dortmund_daily_d15_1462890787.html', {})
    scrape_html('26-04-2016', 'Berlin')
