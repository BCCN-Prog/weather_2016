#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
import time
import os
from bs4 import BeautifulSoup 
import random
import re
import glob
import pprint
import numpy as np

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
        print('Finished download after {:.2f}s'.format((time.time() - t1)))
        print('Saved html to {}\n\n'.format(savepath))
        counter += 1


def test_html_title(html_file, city, country, request_type):
    """ Check if the title of html_file has the expected city, country and request_type (hourly or daily) name. """

    soup = BeautifulSoup(open(html_file))
    title = find_unique(soup, name='title').get_text()
    words = title.split()

    request_type = request_type.lower()

    if request_type == 'hourly':
        title_type = words[1].lower() # hourly or daily
        assert title_type == request_type, 'Request type in html file title ({}) is not the one expected ({}).'.format(title_type, request_type)
        title_city = words[0].lower()
    elif request_type == 'daily':
        title_city = words[2].lower()
    else:
        assert False, "Request=type = {} not know. Only 'daily' or 'hourly' possible".format(request_type)

    city = city.lower()
    assert title_city == city, 'City in html file title ({}) is not the one expected ({}).'.format(title_city, city)

    title_country = words[-1].lower()
    country = country.lower()
    assert title_country == country, 'Country in html file title ({}) is not the one expected ({}).'.format(title_country, country)



def find_unique(soup, n=1, **kwargs):
    """ Use BeautifulSoup.find_all() but throw AssertionError if not exactly n instances are found. """
    result = soup.find_all(**kwargs)
    assert len(result) == n, 'Not exactly {} instances of {} were found in {}, found instances: {}.'.format(n, kwargs, soup.attrs, result)
    if n==1:
        return result[0]
    else:
        return result


def parse_unique(pattern, string, **kwargs):
    """ Use re.findall() but throw AssersionError if multiple instances are found. """
    result = re.findall(pattern, string, **kwargs)
    assert len(result) == 1, 'None or multiple sets of {} found in {}, found instances: {}.'.format(pattern, string, result)
    return result[0]


def split_string(string):
    match = re.match(r"([0-9]+)([a-z]+)", string, re.I)
    if match:
        items = match.groups()
        return items
    else:
        return None


def scrape_daily_html(html_file):

    #TODO: test city name!!

    day_dict = {}

    site, date, time, city, request_type, request_index, timestemp = os.path.splitext(os.path.basename(html_file))[0].split('_') 
    request_index = request_index[1:]
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
        elif j==1:
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

    pprint.pprint(day_dict)

    return day_dict

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
        

def scrape_hourly_html(html_file):

    hour_dicts = {}

    soup = BeautifulSoup(open(html_file))
    
    overview = find_unique(soup, name='div', class_="hourly-table overview-hourly")

    lines = find_unique(overview, n=5, name='tr')

    hour_entries = find_unique(lines[0], n=8, name='td')
    hour = np.empty(8, dtype=str)
    for j, hour_entry in enumerate(hour_entries):
        hour_str = hour_entry.find('div').get_text()
        h, unit = split_string(hour_str)
        assert (unit == 'am' or unit == 'pm'), 'Unit of hour variable is not am, but {}'.format(unit)
        hour[j] = h

    # create dict with given hourly values
    for h in hour:
        hour_dicts[h] = {}


    temp_entries = find_unique(lines[2], n=8, name='span')
    temp = np.empty(8, dtype=float)
    for j, temp_entry in enumerate(temp_entries):
        temp_str = temp_entry.get_text()
        t = parse_unique('\d+', temp_str)
        temp[j] = t
        hour_dicts[str(hour[j])]['temp'] = t


    felt_temp_entries = find_unique(lines[3], n=8, name='span')
    felt_temp = np.empty(8, dtype=float)
    for j, felt_temp_entry in enumerate(felt_temp_entries):
        felt_temp_str = felt_temp_entry.get_text()
        ft = parse_unique('\d+', felt_temp_str)
        felt_temp[j] = ft
        hour_dicts[str(hour[j])]['felt_temp'] = ft


    wind_entries = find_unique(lines[4], n=8, name='span')
    wind_speed = np.empty(8, dtype=float)
    wind_dir = []
    for j, wind_entry in enumerate(wind_entries):
        wind_str = wind_entry.get_text()
        speed, direction = wind_str.split()
        wind_speed[j] = float(speed) * 1e3 / 3600 # m/s 
        wind_dir.append(direction)
        hour_dicts[str(hour[j])]['wind_speed'] = speed
        hour_dicts[str(hour[j])]['wind_direction'] = direction


    precip_hourly = find_unique(soup, name='div', class_="hourly-table precip-hourly")

    lines = find_unique(precip_hourly, n=4, name='tr')


    hour2_entries = find_unique(lines[0], n=8, name='td')
    hour2 = np.empty(8, dtype=str)
    for j, hour2_entry in enumerate(hour2_entries):
        hour2_str = hour2_entry.find('div').get_text()
        h, unit = split_string(hour2_str)
        assert (unit == 'am' or unit == 'pm'), 'Unit of hour2 variable is not am, but {}'.format(unit)
        hour2[j] = h
    assert np.all(hour==hour2), 'Something wrong with the hour variable.'


    rain_chance_entries = find_unique(lines[1], n=8, name='span')
    rain_chance = np.empty(8, dtype=float)
    for j, rain_chance_entry in enumerate(rain_chance_entries):
        rain_chance_str = rain_chance_entry.get_text()
        rc = parse_unique('\d+', rain_chance_str)
        rain_chance[j] = rc
        hour_dicts[str(hour[j])]['rain_chance'] = rc


    snow_chance_entries = find_unique(lines[2], n=8, name='span')
    snow_chance = np.empty(8, dtype=float)
    for j, snow_chance_entry in enumerate(snow_chance_entries):
        snow_chance_str = snow_chance_entry.get_text()
        sc = parse_unique('\d+', snow_chance_str)
        snow_chance[j] = sc
        hour_dicts[str(hour[j])]['snow_chance'] = sc


    ice_chance_entries = find_unique(lines[3], n=8, name='span')
    ice_chance = np.empty(8, dtype=float)
    for j, ice_chance_entry in enumerate(ice_chance_entries):
        ice_chance_str = ice_chance_entry.get_text()
        ic = parse_unique('\d+', ice_chance_str)
        ice_chance[j] = ic
        hour_dicts[str(hour[j])]['ice_chance'] = ic


    sky_hourly = find_unique(soup, name='div', class_="hourly-table sky-hourly")

    lines = find_unique(sky_hourly, n=5, name='tr')

    hour3_entries = find_unique(lines[0], n=8, name='td')
    hour3 = np.empty(8, dtype=str)
    for j, hour3_entry in enumerate(hour3_entries):
        hour3_str = hour3_entry.find('div').get_text()
        h, unit = split_string(hour3_str)
        assert (unit == 'am' or unit == 'pm'), 'Unit of hour3 variable is not am, but {}'.format(unit)
        hour3[j] = h
    assert np.all(hour==hour3), 'Something wrong with the hour variable.'

    # skip UV factor

    cloud_cover_entries = find_unique(lines[2], n=8, name='span')
    cloud_cover = np.empty(8, dtype=float)
    for j, cloud_cover_entry in enumerate(cloud_cover_entries):
        cloud_cover_str = cloud_cover_entry.get_text()
        cc = parse_unique('\d+', cloud_cover_str)
        cloud_cover[j] = cc
        hour_dicts[str(hour[j])]['cloud_cover'] = cc


    humidity_entries = find_unique(lines[3], n=8, name='span')
    humidity = np.empty(8, dtype=float)
    for j, humidity_entry in enumerate(humidity_entries):
        humidity_str = humidity_entry.get_text()
        hu = parse_unique('\d+', humidity_str)
        humidity[j] = hu
        hour_dicts[str(hour[j])]['humidity'] = hu


    dew_point_entries = find_unique(lines[4], n=8, name='span')
    dew_point = np.empty(8, dtype=float)
    for j, dew_point_entry in enumerate(dew_point_entries):
        dew_point_str = dew_point_entry.get_text()
        dp = parse_unique('\d+', dew_point_str)
        dew_point[j] = dp
        hour_dicts[str(hour[j])]['dew_point'] = dp

    return hour_dicts


def scrape(date, city, data_folder):

    data_dict = {'site'     :   'accuweather',
                 'city'     :   city,
                 'date'     :   date
                }
    daily_dict = {}
    hourly_dict = {}

    for html_file in glob.glob(data_folder + '/accuweather_' + date + '*' + city + '*.html'):


        print('Scraping html file:\n', html_file, '\n\n')
        site, date_, time, city_, request_type, request_index, timestemp = os.path.splitext(os.path.basename(html_file))[0].split('_') 
        request_index = request_index[1:]

        assert city == city_, "City name from function argument ({}) and from html filename ({}) are different!".format(city, city_)
        assert date == date_, "Date from function argument ({}) and from html filename ({}) are different!".format(date, date_)

        if request_type == 'daily':

            test_html_title(html_file, city=city, country='Germany', request_type='Daily')

            day_dict = scrape_daily_html(html_file)

            # request_index is days since day of recording (today = 1)
            daily_dict[request_index] = day_dict

        elif request_type == 'hourly':  

            test_html_title(html_file, city=city, country='Germany', request_type='Hourly')

            hour_dict = scrape_hourly_html(html_file)

            # request_index is hours since 12 midnight of day of recording
            hourly_dict.update(hour_dict)

    data_dict['hourly'] = hourly_dict
    data_dict['daily'] = daily_dict

    pprint.pprint(data_dict)

    return data_dict


def scrape_all(data_folder):
    """ Scrape all html file from accuweather in data_folder """

    cities = []
    dates = []

    data_dicitonaries = []

    for html_file in glob.glob(data_folder + '/accuweather*.html'):

        site, date_, time, city_, request_type, request_index, timestemp = os.path.splitext(os.path.basename(html_file))[0].split('_') 

        dates.append(date_)
        cities.append(city_)

    for city in cities:
        for date in dates:
            scraped_dict = scrape(city, date)
            data_dictionaries.append(scraped_dict)

        
if __name__=='__main__':
    #download_html('./data/')
    scrape('17-05-2016', 'berlin', './data/')
    #scrape_all('./data')
    #scrape_daily_html('/home/denis/Documents/Uni/project_software_carpentry/weather_2016/scraping/data/accuweather_10-05-2016_16:33_dortmund_daily_d15_1462890787.html')
    #scrape_hourly_html('./data/accuweather_17-05-2016_17:37_cologne_hourly_h25_1463499470.html')
    #test_html_title('./data/accuweather_17-05-2016_17:37_cologne_hourly_h25_1463499470.html', city='cologne', country='germany', request_type='hourly')
