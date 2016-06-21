# -*- coding: utf-8 -*-
#works only for Python 3
from bs4 import BeautifulSoup
import re
import test_scraper_output as tester
from itertools import product
import os.path
import wrapper.DataWrapH5py as wrapper

def get_month(string):
    """ function extracting month from the string from the table, for date sanity check """
    if 'Apr' in string:
        month = '04'
    elif 'Mai' in string:
        month = '05'
    elif 'Jun' in string:
        month = '06'
    elif 'Jul' in string:
        month = '07'
    else:
        raise Exception('wrong month (not in April - July interval)')
    return month

def prepend_0_if_single_digit(x):
    return '0' + x if len(x) == 1 else x


def scrape(file_date,city, data_path = ''):
    """scraping data from timeanddate.com/weather, returning 2 dictionaries for both hourly forecast dates
    only for dates in April - July period
    date format example: 30-05-2016
    first index in extended in date = 10.05 if downloaded 10.05
    first index in hourly when downloading at 17:24 is 18:00
    checks: if date in filename is date of hourly forecast,
    if the forecast is for the city that is in the filename (except from saarbrucken)
    if day is between 1-31
    if rain encoding hasn't change
    """

    hours = [prepend_0_if_single_digit(str(i)) for i in range(24)]
    minutes = [prepend_0_if_single_digit(str(i)) for i in range(60)]

    file_exists = False

    for hour, minute in product(hours,minutes):
        name = data_path + "/timeanddate_com_{}_{}_{}_{}_hourly.html".format(file_date,hour,minute,city)
        if os.path.exists(name):
            file_hourly = data_path + "/timeanddate_com_{}_{}_{}_{}_hourly.html".format(file_date,hour,minute,city)
            file_daily = data_path + "/timeanddate_com_{}_{}_{}_{}_daily.html".format(file_date,hour,minute,city)
            ho = hour
            mi = minute
            file_exists = True
            break

    if not file_exists:
        return
    out_dict = {}
    site = 0 #'timeanddate.com/weather'
    out_dict['site'] = site
    soup = [0,0]
    soup[0] = BeautifulSoup(open(file_daily))
    soup[1] = BeautifulSoup(open(file_hourly))

    # log the location
    title1 = soup[0].title.string.split(',')[0]
    html_city1 = title1.split(' ')[-1]
    title2 = soup[1].title.string.split(',')[0]
    html_city2 = title2.split(' ')[-1]

    if city is not 'saarbrucken':
        if html_city1.lower()==city and html_city2.lower()==city:
            out_dict['city'] = city
        else:
            raise Exception('forecast for city different than in the file name for', city)
    else:
        out_dict['city'] = city
    out_dict['daily'] = {}
    out_dict['hourly'] = {}

    date1 = soup[1].find_all('tr')[2:3]
    dates = date1[0].find_all('th')
    date_check = '{}_{}_2016'
    date_temp = '2016{}{}'
    a = dates[0].text[2:]  # gets dates in format i.e. 10. Mai
    month = get_month(a)

    #finding the day of forecast
    b = re.findall(r'\d+', str(dates))
    if 0 < int(b[-1]) < 32:
        day = prepend_0_if_single_digit(b[-1])
    else:
        raise Exception('wrong day')

    date_check = date_check.format(day, month)
    date = date_temp.format(month,day)
    out_dict['prediction_time'] = int('{}{}{}'.format(date, ho,mi ))

    if date_check==file_date:
        out_dict['date'] = int(date)
    else:
        raise Exception('wrong date in html for file from {}'.format(file_date))
    #scraping table: soup.find_all('tr')

    ## get the daily data
    if 'extended' in soup[0].title.string:
        for i, tr in enumerate(soup[0].find_all('tr')[2:-1]):
            dict ={}
            # scraping columns in the table
            tds = tr.find_all('td')
            c=list(map(int,re.findall(r'\d+', str(tds)))) #list of all numbers in each row of the table

            #interesting values:
            dict['low'] = float(c[4]) #c[4] - temp min
            dict['high'] = float(c[5]) #c[5] - temp max
            wind = round(c[7] * 1000 / 3600., 1) #c[7] - wind [km/h]
            dict['wind_speed'] = wind
            dict['humidity'] = float(c[10]) #c[10] - humidity
            dict['rain_chance'] = float(c[11]) #c[11] - rain chance
            # rain_amt:
            if len(c) ==19:
                rain= int(c[-7]) + int(c[-6])/10
            elif len(c) == 17:
                rain = 0.0
            else:
                raise Exception('scraping failed - change in a site structure')
            dict['rain_amt'] = rain
            out_dict['daily']["{}".format(str(i))] = dict

    else:
        raise Exception('wrong input file')

    ## get the hourly data
    if 'Hourly' in soup[1].title.string:
        out_dict2 = {}
        out_dict2['daily']={}
        out_dict2['hourly'] = {}
        out_dict2['site'] = site
        out_dict2['prediction_time'] = int('{}{}{}'.format(date, ho, mi))
        out_dict2['city'] = city
        date2 = date_temp.format(month, prepend_0_if_single_digit(str(int(b[-1])+1)))
        out_dict2['date'] = int(date2) #forecast for the next day
        for j, tr in enumerate(soup[1].find_all('tr')[2:-1]): #for every row in a table
            dict = {}
            #scraping from columns of the table except the first
            tds = tr.find_all('td')
            c = list(map(int, re.findall(r'[\d]+', str(tds))))  # list of all numbers in each row of the table
            if len(c) > 11:
                rain = int(c[-2]) + int(c[-1])/10
            else:
                rain = 0.0
            dict['rain_amt'] = rain
            # interesting values:
            dict['temp'] = float(c[4]) # c[4] - temp
            wind = round(c[6] * 1000 / 3600., 1) # c[6] - wind [km/h]
            dict['wind_speed'] = wind
            dict['humidity'] = float(c[9])# c[9] - humidity
            dict['rain_chance'] = float(c[10]) # c[10] - rain chance
            offset = int(ho)+1 #index of first hourly entry: 19 if forecast for 19:00
            idx = prepend_0_if_single_digit(str(j+offset))
            if j+offset<=23:
                out_dict['hourly']["{}".format(idx)] = dict #index: 00, 01, ..., 23
            else:
                idx2 = prepend_0_if_single_digit(str((j + offset)%24))
                out_dict2['hourly']["{}".format(idx2)] = dict
    else:
        raise Exception('wrong input file')

    #print(len(out_dict['hourly'])) #24
    assert (tester.run_tests(out_dict))
    assert (tester.run_tests(out_dict2))
    #print(out_dict, out_dict2)
    daily_db = wrapper.Daily_DataBase()
    hourly_db = wrapper.Hourly_DataBase()
    daily_db.save_dict(out_dict)
    hourly_db.save_dict(out_dict)
    hourly_db.save_dict(out_dict2)
    #return out_dict, out_dict2

if __name__ == '__main__':
    date = '07_06_2016'
    city = 'nuremberg'
    d = scrape(date,city)
    print(d)

