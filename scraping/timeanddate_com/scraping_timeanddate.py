# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re

## need a date and time stamp for every row of c
def scrape(file):
    soup = BeautifulSoup(open(file), "lxml")

    # log the location
    # print(soup.title.string)

    #scraping table: soup.find_all('tr')

    ## get the daily data
    if 'extended' in soup.title.string:
        for tr in soup.find_all('tr')[2:-1]:
            tds = tr.find_all('td')

        #a = tds[1].text
            c=list(map(int,re.findall(r'\d+', str(tds)))) #list of all numbers in each row of the table
            #interesting values:
            #c[4] - temp min
            #c[5] - temp max
            #c[7] - wind [km/h]
            #c[10] - humidity
            #c[11] - rain chance
            if len(c)>17:
                rain= int(c[-7]) + int(c[-6])/10
            else:
                rain = 0
            wind = round(c[7]*1000/3600.,1)
            print('temp min: {}, temp max: {}, wind: {} m/s, humidity: {}, chance: {}, amount: {}'.format(str(c[4]), str(c[5]),
                                                                                                          str(wind),
                                                                                                          str(c[10]),
                                                                                                          str(c[11]), str(rain)))

    ## get the hourly data
    else:
        for tr in soup.find_all('tr')[2:-1]:
            tds = tr.find_all('td')
            c = list(map(int, re.findall(r'[\d]+', str(tds))))  # list of all numbers in each row of the table
            print(c, len(c))
            if len(c) > 11:
                rain = int(c[-2]) + int(c[-1]) / 10
            else:
                rain = 0

            # interesting values:
            # c[4] - temp
            # c[5] - temp feels like
            # c[6] - wind [km/h]
            # c[9] - humidity
            # c[10] - rain chance
            wind = round(c[6] * 1000 / 3600., 1)

    return c

if __name__ == '__main__':
    file = "time_and_date_26-04-2016_berlin_hourly.html"
    scrape(file)
