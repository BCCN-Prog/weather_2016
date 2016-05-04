from bs4 import BeautifulSoup
from glob import glob
import numpy as np
import pprint

# dates to process
dates = ['26-04-2016']

# list fo all cities we are scraping from
cities = ["berlin", "hamburg", "muenchen",
            "koeln", "frankfurt", "stuttgart",
            "bremen", "leipzig", "hannover",
            "nuernberg", "dortmund", "dresden",
            "kassel", "kiel", "bielefeld",
            "saarbruecken", "rostock", "freiburg",
            "magdeburg", "erfurt"]

def scrape_hourly(date, city):
    # define dict
    hourly_dic = {}

    # try to open the file
    path = "../data/wetter_com_" + date + "_" + city + '_hourly.html'
    try:
        print("Scraping "+ path)
        soup = BeautifulSoup(open(path), "lxml")
    except FileNotFoundError:
        print("Data file missing, PATH: " + path)

    # define hourly scraping classes
    hour_class = '[ half-left ][ bg--white ][ cover-top ][ text--blue-dark ]'
    temp_class = '[ half-left ][ bg--white ][ js-detail-value-container ]'
    rainprob_class = 'mt--'
    rainAmount_class = '[ mb-- ][ block ][ text--small ][ absolute absolute--left ][ one-whole ]'
    windDir_class = '[ mb- ][ block ]'
    windAmount_class = '[ js-detail-value-container ][ one-whole ][ mb- ][ text--small ]'
    pressure_class = '[ mb- mt-- ][ block ][ text--small ]'
    humidity_class = '[ mb-- ][ block ][ text--small ]'

    hours = soup.find_all('div', class_ = hour_class)
    # get the starting hour of the hour table
    starting_hour = int((hours[0].string.split()[0])[1])
    # define the hour string list for indexing the dictionary correctly
    hour_strs = []
    # this is because the data on the website does not start at 00 hours but at "starting_hour” hours
    for i in range(24):
        s = "{:0>2}".format(np.mod(i+starting_hour,24))
        hour_strs.append(s)
        hourly_dic[s] = {}


    # SCRAPE TEMPERATURE
    # get all the temperature divs
    temps = soup.find_all('div', class_ = temp_class)
    # for every div, get the string, take the temperature value and save it in the matrix
    assert(len(temps)==24)
    for j, div in enumerate(temps):
        hourly_dic[hour_strs[j]]['temp'] = int(div.string.split()[0])

    # SCRAPE Rain probs
    probs = soup.find_all('p', class_ = rainprob_class)[:24]
    for j, p in enumerate(probs):
        hourly_dic[hour_strs[j]]['rain_chance'] = int(p.string.split()[0])

    # SCRAPE Rain amounts
    amounts = soup.find_all('span', class_ = rainAmount_class)
    for j, span in enumerate(amounts):
        hourly_dic[hour_strs[j]]['rain_amt'] = float(span.text.split()[0])

    # SCRAPE Wind directions
    windDirs = soup.find_all('span', class_=windDir_class)
    for j, span in enumerate(windDirs):
        hourly_dic[hour_strs[j]]['wind_dir'] = span.text

    # SCRAPE Wind speed
    wstr = soup.find_all('div', class_=windAmount_class)
    for j, div in enumerate(wstr):
        # convert to m/s
        hourly_dic[hour_strs[j]]['wind_speed'] = round(float(div.string.split()[0])/3.6, 2)

    # SCRAPE pressure
    airpress = soup.find_all('span', class_ = pressure_class)
    for j, span in enumerate(airpress):
        hourly_dic[hour_strs[j]]['pressure'] = float(span.text.split()[0])

    # SCRAPE air humidity
    airhum = soup.find_all('span', class_=humidity_class)
    for j, span in enumerate(airhum):
        hourly_dic[hour_strs[j]]['humidity'] = float(span.text.split()[0])

    return hourly_dic

def scrape_daily(date, city):
    # define dict
    daily_dic = {}
    days = 16

    # try to open the file
    path = "../data/wetter_com_" + date + "_" + city + '_daily.html'
    try:
        print("Scraping "+ path)
        soup = BeautifulSoup(open(path), "lxml")
    except FileNotFoundError:
        print("Data file missing, PATH: " + path)

    # define daily scraping classes
    temp_low_class = 'inline text--white gamma'
    temp_high_class = 'text--white beta inline'
    rain_class = 'flag__body'


    windDir_class = '[ mb- ][ block ]'
    windAmount_class = '[ js-detail-value-container ][ one-whole ][ mb- ][ text--small ]'
    pressure_class = '[ mb- mt-- ][ block ][ text--small ]'
    humidity_class = '[ mb-- ][ block ][ text--small ]'

    # prelocate dict
    for i in range(16):
        s = "{}".format(i)
        hour_strs.append("{}".format(i))
        hourly_dic[s] = {}

    # SCRAPE TEMPERATURE
    # get all the high temperature divs
    temps_high = soup.find_all('div', class_=temp_high_class)
    # for every div, get the string, take the temperature value and save it in the matrix
    assert(len(temps)==days)
    for j, div in enumerate(temps_high):
        daily_dic[hour_strs[j]]['High'] = float(div.string[0])
    # low
    temps_low = soup.find_all('div', class_=temp_low_class)
    # for every div, get the string, take the temperature value and save it
    assert(len(temps)==days)
    for j, div in enumerate(temps_low):
        daily_dic[hour_strs[j]]['Low'] = float(div.string[3])

    # SCRAPE Rain probs
    """
    probs = soup.find_all('p', class_ = rainprob_class)[:24]
    for j, p in enumerate(probs):
        hourly_dic[hour_strs[j]]['rain_chance'] = int(p.string.split()[0])

    # SCRAPE Rain amounts
    amounts = soup.find_all('span', class_ = rainAmount_class)
    for j, span in enumerate(amounts):
        hourly_dic[hour_strs[j]]['rain_amt'] = float(span.text.split()[0])

    # SCRAPE Wind directions
    windDirs = soup.find_all('span', class_=windDir_class)
    for j, span in enumerate(windDirs):
        hourly_dic[hour_strs[j]]['wind_dir'] = span.text

    # SCRAPE Wind speed
    wstr = soup.find_all('div', class_=windAmount_class)
    for j, div in enumerate(wstr):
        # convert to m/s
        hourly_dic[hour_strs[j]]['wind_speed'] = round(float(div.string.split()[0])/3.6, 2)

    # SCRAPE pressure
    airpress = soup.find_all('span', class_ = pressure_class)
    for j, span in enumerate(airpress):
        hourly_dic[hour_strs[j]]['pressure'] = float(span.text.split()[0])

    # SCRAPE air humidity
    airhum = soup.find_all('span', class_=humidity_class)
    for j, span in enumerate(airhum):
        hourly_dic[hour_strs[j]]['humidity'] = float(span.text.split()[0])
    """
    return daily_dic

# for every date:
for date in dates:
    for city in cities:
        # make dict
        data_dic = {'site': 'wetter.com',
                    'city': city,
                    'date': date,
                    'hourly': scrape_hourly(date, city)}
        daily_dic = scrape_daily(date, city)
        pprint.pprint(daily_dic)
        break
