# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re

def get_month(string):
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

def scrape(file):
    site = 'timeanddate.com/weather'
    soup = BeautifulSoup(open(file), "lxml")

    # log the location
    city = soup.title.string.split(',')[-2][1:]
    print(city) #city name without space at the beginning
    dicts = []

    ## get the daily data
    if 'extended' in soup.title.string:
        for tr in soup.find_all('tr')[2:-1]:
            dict ={}
            dict['site'] = site
            dict['city'] = city

            #scraping date for the forecast
            dates = tr.find_all('th')
            date = '{}-{}-2016'
            a = dates[0].text[2:] #gets dates in format i.e. 10. Mai
            month = get_month(a)

            b = re.findall(r'\d+', str(dates))
            print(b[0])
            if 0 < int(b[0]) < 32:
                day = b[0]
            else:
                raise Exception('wrong day')

            date = date.format(day,month)
            dict['date'] = date
            # scraping the rest of columns in the table
            tds = tr.find_all('td')
            c=list(map(int,re.findall(r'\d+', str(tds)))) #list of all numbers in each row of the table

            #interesting values:
            #c[4] - temp min
            dict['Low'] = float(c[4])
            #c[5] - temp max
            dict['High'] = float(c[5])
            #c[7] - wind [km/h]
            wind = round(c[7] * 1000 / 3600., 1)
            dict['wind_speed'] = float(wind)
            #c[10] - humidity
            dict['humidity'] = int(c[10])
            #c[11] - rain chance
            dict['rain_chance'] = int(c[11])
            if len(c) ==19:
                rain= int(c[-7]) + int(c[-6])/10
            elif len(c) == 17:
                rain = 0
            else:
                raise Exception('scraping failed - change in a site structure')
            dict['rain_amt'] = rain
            dicts.append(dict)

    ## get the hourly data
    else:
        for tr in soup.find_all('tr')[2:-1]: #for every row in a table
            dict = {}
            dict['site'] = site
            dict['city'] = city
            dates = tr.find_all('th')
            a = dates[0].text[8:]
            #print(a, len(a))
            if 6 <= len(a) <= 8:
                date = '{}-{}-2016'
                month = get_month(a)

                b = re.findall(r'\d+', str(dates)) #finding all numbers
                #b[0] - hour, b[1] - minutes = 00, b[2] - day
                if 0 < int(b[2]) < 32:
                    day = b[2]
                else:
                    raise Exception('wrong day')

                hour = dates[0].text[:5]
            elif len(a)<6:
                hour = dates[0].text
            else:
                raise Exception('wrong date')
            date = date.format(day, month)
            dict['date'] = date
            dict['hour'] = hour
            #print(dates[0].text[:5])
            #print(date, hour)

            #scraping from columns of the table except the first
            tds = tr.find_all('td')
            c = list(map(int, re.findall(r'[\d]+', str(tds))))  # list of all numbers in each row of the table
            if len(c) > 11:
                rain = int(c[-2]) + int(c[-1])/10
            else:
                rain = 0
            dict['rain_amt'] = rain
            # interesting values:
            # c[4] - temp
            dict['temp'] = float(c[4])
            # c[5] - temp feels like
            # c[6] - wind [km/h]
            wind = round(c[6] * 1000 / 3600., 1)
            dict['wind_speed'] = wind
            # c[9] - humidity
            dict['humidity'] = int(c[9])
            # c[10] - rain chance
            dict['rain_chance'] = int(c[10])
            dicts.append(dict)

    return dicts

if __name__ == '__main__':
    file1 = "timeanddate_com_10-05-2016_berlin_daily.html"
    file2 = "timeanddate_com_10-05-2016_bremen_hourly.html"
    d = scrape(file2)
    print(d)
