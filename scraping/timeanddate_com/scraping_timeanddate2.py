# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re

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

def scrape(file_hourly, file_daily):
    """scraping data from timeanddate.com/weather, returning one dictionary for both files
    first index in extended in date = 11.05 if downloaded 10.05
    first index in hourly when downloading at 17:24 is 18:00
    checks: if date in filename is date of hourly forecast,
    if day is between 1-31
    if rain encoding hasn't change
    if the first file is hourly """

    out_dict = {}
    site = 'timeanddate.com/weather'
    out_dict['site'] = site
    soup1 = BeautifulSoup(open(file_daily), "lxml")
    soup2 = BeautifulSoup(open(file_hourly), "lxml")

    # log the location
    city = soup1.title.string.split(',')[-2][1:]
    #print(city) #city name without space at the beginning
    out_dict['city'] = city
    out_dict['daily'] = {}
    out_dict['hourly'] = {}

    date1 = soup2.find_all('tr')[2:3]
    dates = date1[0].find_all('th')
    date = '{}-{}-2016'
    a = dates[0].text[2:]  # gets dates in format i.e. 10. Mai
    month = get_month(a)
    b = re.findall(r'\d+', str(dates))
    if 0 < int(b[-1]) < 32:
        day = b[-1]
    else:
        raise Exception('wrong day')
    date = date.format(day, month)

    if date in file1:
        out_dict['date'] = date
    else:
        raise Exception('wrong date')
    dicts1 = []
    dicts2 = []
    #scraping table: soup.find_all('tr')

    ## get the daily data
    if 'extended' in soup1.title.string:
        for i, tr in enumerate(soup1.find_all('tr')[2:-1]):
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
                rain = 0
            else:
                raise Exception('scraping failed - change in a site structure')
            dict['rain_amt'] = rain
            out_dict['daily']["{}".format(str(i+1))] = dict
            dicts1.append(dict)

    else:
        raise Exception('wrong input file')

    ## get the hourly data
    if 'Hourly' in soup2.title.string:
        for j, tr in enumerate(soup2.find_all('tr')[2:-1]): #for every row in a table
            dict = {}
            #scraping from columns of the table except the first
            tds = tr.find_all('td')
            c = list(map(int, re.findall(r'[\d]+', str(tds))))  # list of all numbers in each row of the table
            if len(c) > 11:
                rain = int(c[-2]) + int(c[-1])/10
            else:
                rain = 0
            dict['rain_amt'] = rain
            # interesting values:
            dict['temp'] = float(c[4]) # c[4] - temp
            wind = round(c[6] * 1000 / 3600., 1) # c[6] - wind [km/h]
            dict['wind_speed'] = wind
            dict['humidity'] = float(c[9])# c[9] - humidity
            dict['rain_chance'] = float(c[10]) # c[10] - rain chance
            dicts2.append(dict)
            if j+1<10:
                j= str(j+1).zfill(2)
            else:
                j = str(j+1)
            out_dict['hourly']["{}".format(j)] = dict
    else:
        raise Exception('wrong input file')

    #print(len(out_dict['hourly'])) #24
    return out_dict

if __name__ == '__main__':
    file1 = "timeanddate_com_10-05-2016_berlin_daily.html"
    file2 = "timeanddate_com_10-05-2016_bremen_hourly.html"
    d = scrape(file2,file1)
    print(d)


