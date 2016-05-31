# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import test_scraper_output as tester

# my city names are different (in English):
# cities_table = {"berlin": 1, "hamburg": 2, "muenchen": 3,
# "koeln": 4, "frankfurt": 5, "stuttgart": 6,
# "bremen" :7, "leipzig": 8, "hannover": 9,
# "nuernberg": 10, "dortmund": 11, "dresden": 12,
# "kassel": 13, "kiel": 14, "bielefeld": 15,
# "saarbruecken": 16, "rostock": 17, "freiburg": 18,
# "magdeburg": 19, "erfurt": 20}
#
# provider_list = {'timeanddate_com': 0,
# 'wetter_com': 1,
# 'owm': 2,
# 'wetter_de':3,
# 'accuweather':4}

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

def scrape(file_date,city, data_path = ''):
    """scraping data from timeanddate.com/weather, returning one dictionary for both files
    only for dates in April - July period
    date format example: 30-05-2016
    first index in extended in date = 11.05 if downloaded 10.05
    first index in hourly when downloading at 17:24 is 18:00
    checks: if date in filename is date of hourly forecast,
    if the forecast is for the city that is in the filename (except from saarbrucken)
    if day is between 1-31
    if rain encoding hasn't change
    """
    file_hourly = "timeanddate_com_{}_{}_hourly.html".format(file_date,city)
    file_daily = "timeanddate_com_{}_{}_daily.html".format(file_date,city)
    out_dict = {}
    site = 0 #'timeanddate.com/weather'
    out_dict['site'] = site
    soup = [0,0]
    soup[0] = BeautifulSoup(open(file_daily), "lxml")
    soup[1] = BeautifulSoup(open(file_hourly), "lxml")

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
    date_check = '{}-{}-2016'
    date_temp = '{}{}2016'
    a = dates[0].text[2:]  # gets dates in format i.e. 10. Mai
    month = get_month(a)
    b = re.findall(r'\d+', str(dates))

    if 0 < int(b[-1]) < 32:
        day = b[-1]
    else:
        raise Exception('wrong day')
    date_check = date_check.format(day, month)
    date = date_temp.format(day,month)

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
            out_dict['daily']["{}".format(str(i+1))] = dict

    else:
        raise Exception('wrong input file')

    ## get the hourly data
    if 'Hourly' in soup[1].title.string:
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
            if j<10:
                j= str(j).zfill(2)
            else:
                j = str(j)
            out_dict['hourly']["{}".format(j)] = dict #index: 00, 01, ..., 23
    else:
        raise Exception('wrong input file')

    #print(len(out_dict['hourly'])) #24
    assert (tester.run_tests(out_dict))
    return out_dict

if __name__ == '__main__':
    date = '10-05-2016'
    city = 'saarbrucken'
    d = scrape(date,city)
    #print(d['city'])

    #tester.run_tests(d)

