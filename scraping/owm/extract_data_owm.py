# -*- coding: utf-8 -*-

import sys
sys.path.append('../')
sys.path.append('../../')
import os
from bs4 import BeautifulSoup
from itertools import product
import test_scraper_output as tester
import wrapper.DataWrapH5py as wrapper
import pprint

def scrape(date, city, data_path):
    """Scrape data for given date and city.
    :param data: should be in the format 30-05-2016
    :param city: should be the english city name, i.e., cologne, cassel, munich
    """
    # get date id
    dateInt = int(date.split('_')[2] + date.split('_')[1] + date.split('_')[0])
    # scrape full data dictionary
    data_dict = {'site': 2, # owm id: 1
                'city': city,
                'date': dateInt,
                'hourly': scrape_hourly(date, city, data_path),
                'daily': scrape_daily(date, city, data_path)}
                
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(data_dict)
    # run tests
    assert(tester.run_tests(data_dict))
    #TODO add data to data base
    daily_db = wrapper.Daily_DataBase()
    hourly_db = wrapper.Hourly_DataBase()
    daily_db.save_dict(data_dict)
    hourly_db.save_dict(data_dict)
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
    
def hourly_humidity(tag):
    return float(tag.find('p').string.strip().split(' ')[6].replace('%,', ''))

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
    dictionary = {}
    with open(file_name, encoding='utf-8') as html:
        soup = BeautifulSoup(html, 'lxml')
    
        # daily
        table = soup.find(id='daily_list')
        tds = table.find_all('td')
        for i, td in enumerate(tds):
            day = str(i // 2).zfill(2)
            if i % 2 == 0:
                dictionary[day] = {}
                # TODO: assert correct day
            else:
                dictionary[day]['high'] = daily_high(td)
                dictionary[day]['low'] = daily_low(td)
                dictionary[day]['pressure'] = daily_pressure(td)
                dictionary[day]['cloud_cover'] = daily_clouds(td)
                dictionary[day]['wind_speed'] = daily_wind(td)
                # TODO: remove mocked rain chance data
                dictionary[day]['rain_chance'] = None
                # TODO: maybe add rain amount data
                dictionary[day]['rain_amt'] = None
            
    return dictionary

def scrape_hourly(date, city, data_path):
    file_name = get_filename(data_path, date, city)
    dictionary = {}
    with open(file_name, encoding='utf-8') as html:
        soup = BeautifulSoup(html, 'lxml')
            
        # hourly
        table = soup.find(id='hourly_long_list').find('table')
        
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
                td = tr.find('td')
                for child in td.children:
                    index = int(child.string.strip().split(':')[0])
                    break
                
            dictionary[index] = {}
            dictionary[index]['temp'] = hourly_temp(tr)
            dictionary[index]['pressure'] = hourly_pressure(tr)
            dictionary[index]['cloud_cover'] = hourly_clouds(tr)
            dictionary[index]['wind_speed'] = hourly_wind(tr)
            # TODO: remove mocked rain chance data
            dictionary[index]['rain_chance'] = None
            # TODO: maybe add rain amount data
            dictionary[index]['rain_amt'] = None
            dictionary[index]['humidity'] = hourly_humidity(tr)
            
            index += 3
            if index > 27:
                break

        return dictionary        
        
scrape('07_06_2016', 'berlin', 'output/')
