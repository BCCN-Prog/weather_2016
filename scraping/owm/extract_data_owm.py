# -*- coding: utf-8 -*-

import os
from bs4 import BeautifulSoup
from itertools import product
import test_scraper_output as tester

def scrape(date, city, data_path):
    """Scrape data for given date and city.
    :param data: should be in the format 30-05-2016
    :param city: should be the english city name, i.e., cologne, cassel, munich
    """
    # get date id
    dateInt = int(date.split('_')[2] + date.split('_')[1] + date.split('_')[0])
    # scrape full data dictionary
    data_dic = {'site': 2, # owm id: 1
                'city': city,
                'date': dateInt,
                'hourly': scrape_hourly(date, city, data_path),
                'daily': scrape_daily(date, city, data_path)}
    # run tests
    assert(tester.run_tests(data_dic))
    #TODO add data to data base
    # return nothing


def daily_high(tag):
    return float(tag.find('span').string.strip().replace('°C', ''))
    
def daily_low(tag):
    return float(tag.find_all('span')[1].string.strip().replace('°C', ''))
    
def daily_wind(tag):
    for child in tag.find('p').children:
        return float(child.string.strip().replace('m/s', ''))
        break

def daily_clouds(tag):
    for i, child in enumerate(tag.find('p').children):
        if i < 2:
            continue
        return float(child.string.strip().split('%')[0].split(' ')[1])
        
def daily_pressure(tag):
    for i, child in enumerate(tag.find('p').children):
        if i < 2:
            continue
        return float(child.string.strip().split(',')[1].replace('hpa', '').strip())

def hourly_first_index(date, time):
    print(date)
    scrape_time = date.split('_')[1]
    print(scrape_time)
    hours = int(scrape_time.split(':')[0]), int(time.split(':')[0])
    mins = int(scrape_time.split(':')[1])    
    diff = hours[1] - hours[0]        
    return diff if mins < 30 else diff - 1

def hourly_time(tag):
    return list(tag.find('td').children)[0].strip()

def hourly_temp(tag):
    return float(tag.find('span').string.strip().replace('°C', ''))

def hourly_wind(tag):
    return float(tag.find('p').string.strip().split(' ')[4].replace('m/s.', ''))
    
def hourly_clouds(tag):
    return float(tag.find('p').string.strip().split(' ')[6].replace('%,', ''))
    
def hourly_pressure(tag):
    return float(tag.find('p').string.strip().split(' ')[7])

def prepend_0_if_single_digit(x):
    return '0' + str(x) if len(x) == 1 else x

def get_filename(data_path, date, city):
    """Looks up filename of the html file in dirpath for given date and city
    :param mode: daily or hourly data
    """
    hours = [prepend_0_if_single_digit(str(i)) for i in range(24)]
    minutes = [prepend_0_if_single_digit(str(i)) for i in range(60)]    
    for hour, minute in product(hours,minutes):
        name = data_path + "owm_{}_{}_{}_{}.html".format(date, hour, minute, city)
        if os.path.exists(name):
            return data_path + "owm_{}_{}_{}_{}.html".format(date, hour, minute, city)

def scrape_daily(date, city, data_path):
    file_name = get_filename(data_path, date, city)
    dict = {}
    with open(file_name, encoding='utf-8') as html:
        soup = BeautifulSoup(html, 'lxml')
        
        date_tag = soup.find(id='date_m')
        date = date_tag.string.split()[2]
        date = '-'.join(date.split('.')[::-1])
        time = date_tag.string.split()[3]
        dict['last_updated'] = '{}_{}'.format(date, time)    
    
        # daily
        table = soup.find(id='daily_list')
        dict['daily'] = {}
        tds = table.find_all('td')
        for i, td in enumerate(tds):
            day = str(i // 2).zfill(2)
            if i % 2 == 0:
                dict['daily'][day] = {}
                # TODO: assert correct day
            else:
                dict['daily'][day]['high'] = daily_high(td)
                dict['daily'][day]['low'] = daily_low(td)
                dict['daily'][day]['pressure'] = daily_pressure(td)
                dict['daily'][day]['cloud_cover'] = daily_clouds(td)
                dict['daily'][day]['wind_speed'] = daily_wind(td)

def scrape_hourly(date, city, data_path):
    file_name = get_filename(data_path, date, city)
    dict = {}
    with open(file_name, encoding='utf-8') as html:
        soup = BeautifulSoup(html, 'lxml')
        
        date_tag = soup.find(id='date_m')
        date = date_tag.string.split()[2]
        date = '-'.join(date.split('.')[::-1])
        time = date_tag.string.split()[3]
        dict['last_updated'] = '{}_{}'.format(date, time)    
    
        # hourly
        table = soup.find(id='hourly_long_list').find('table')
        
        dict['hourly'] = {}
        trs = table.find_all('tr')
        
        day = None
        index = 0      
        
        for tr in trs:
            if ('class' in tr.attrs and tr.attrs['class'] == ['well']):
                # TODO: handle day switch, probably call database side more than once
                day = tr.find('b').string.strip()
                continue
            if index == 0:
                # TODO: how do I extract the time? It is somewhere in the tr.find('td') object
                print(tr.find('td'))
                index = tr.find('td').string
                
            dict['hourly'][index] = {}
            dict['hourly'][index]['temp'] = hourly_temp(tr)
            dict['hourly'][index]['pressure'] = hourly_pressure(tr)
            dict['hourly'][index]['cloud_cover'] = hourly_clouds(tr)
            dict['hourly'][index]['wind_speed'] = hourly_wind(tr)
            
            index += 3
            if index > 27:
                break

scrape('07_06_2016', 'berlin', 'output/')

#with open('output/{}'.format(file_name), encoding='utf-8') as html:
#    soup = BeautifulSoup(html, 'lxml')
#    
#    date_tag = soup.find(id='date_m')
#    date = date_tag.string.split()[2]
#    date = '-'.join(date.split('.')[::-1])
#    time = date_tag.string.split()[3]
#    dict['last_updated'] = '{}_{}'.format(date, time)    
#
#    split_file_name = file_name.split('_')    
#    dict['date'] = '{}_{}'.format(split_file_name[1], split_file_name[2])
#    dict['site'] = split_file_name[0]
#    dict['city'] = split_file_name[3].split('.')[0]
#    
#    # daily
#    table = soup.find(id='daily_list')
#    dict['daily'] = {}
#    tds = table.find_all('td')
#    for i, td in enumerate(tds):
#        day = str(i // 2).zfill(2)
#        if i % 2 == 0:
#            dict['daily'][day] = {}
#            # TODO: assert correct day
#        else:
#            dict['daily'][day]['high'] = daily_high(td)
#            dict['daily'][day]['low'] = daily_low(td)
#            dict['daily'][day]['pressure'] = daily_pressure(td)
#            dict['daily'][day]['cloud_cover'] = daily_clouds(td)
#            dict['daily'][day]['wind_speed'] = daily_wind(td)
#    
#    # hourly
#    table = soup.find(id='hourly_long_list').find('table')
#    
#    dict['hourly'] = {}
#    trs = table.find_all('tr')
#    
#    day = None
#    index = 0
#    
#    for tr in trs:
#        if ('class' in tr.attrs and tr.attrs['class'] == ['well']):
#            day = tr.find('b').string.strip()
#            continue
#        if index == 0:
#            time = hourly_time(tr)
#            index = hourly_first_index(dict['date'], time)
#            
#        dict['hourly'][index] = {}
#        dict['hourly'][index]['temp'] = hourly_temp(tr)
#        dict['hourly'][index]['pressure'] = hourly_pressure(tr)
#        dict['hourly'][index]['cloud_cover'] = hourly_clouds(tr)
#        dict['hourly'][index]['wind_speed'] = hourly_wind(tr)
#        
#        index += 3
#        if index > 27:
#            break
    
