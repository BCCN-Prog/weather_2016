from bs4 import BeautifulSoup
from glob import glob
import numpy as np
import pprint
import os, sys
import datetime
sys.path.append("../")
sys.path.append("../../")
import test_scraper_output as tester
import wrapper.DataWrapH5py as wrapper

def scrape(date, city, data_path='../data'):
    """Scrape data for given date and city.
    :param date: should be in the format 30-05-2016
    :param city: should be the english city name, i.e., cologne, kassel, munich
    :param data_path: relative path to the directory where html files live
    """
    year, month, day = date.split('-')[2], date.split('-')[1], date.split('-')[0]
    dateInt = int(year + month + day)

    # the hourly scraping now returns to dicts: an additional one for some hours of the next day
    hourly_today, hourly_tmr = scrape_hourly(date, city, data_path)

    # construct the full dictionary for current day
    data_dict = {'site': 1, # 'wetter.com' id = 1
                'city': city,
                'date': dateInt,
                'hourly': hourly_today,
                'daily': scrape_daily(date, city, data_path)}
    assert(tester.run_tests(data_dict)) # test scraper output

    # add to data base
    daily_db = wrapper.Daily_DataBase()
    hourly_db = wrapper.Hourly_DataBase()
    daily_db.save_dict(data_dict)
    hourly_db.save_dict(data_dict)

    # construct the partial dict for tmr, holding the hourly data for some hours
    # get tmr date
    dateTmr = (datetime.date(int(year),int(month),int(day)) + datetime.timedelta(days=1)).isoformat()
    dateIntTmr = int(dateTmr.split('-')[0]+dateTmr.split('-')[1]+dateTmr.split('-')[2])

    # construct dict, leave daily dict empty
    data_dict_tmr = {'site': 1, # 'wetter.com' id = 1
                    'city': city,
                    'date': dateIntTmr,
                    'hourly': hourly_tmr,
                    'daily': {}}
    assert(tester.run_tests(data_dict_tmr)) # test scraper output
    # add hourly to data base
    hourly_db = wrapper.Hourly_DataBase()
    hourly_db.save_dict(data_dict_tmr)

def scrape_hourly(date, city, data_path='../data'):
    """Scrapes hourly data from html file containing the hourly data of the
    given date and city
    :param date: should be in the format 30-05-2016
    :param city: should be the english city name, i.e., cologne, kassel, munich
    :param data_path: relative path to the directory where html files live
    :return hourly_dict: dictionary holding the hourly data
    """

    # define dict
    hourly_dict = {}

    # try to open the file
    try:
        path = data_path + '/' + get_filename(data_path, date, city, mode='hourly')
    except:
        print("Can't find PATH: " + data_path + ' ' + date + ' ' + city + ' hourly')
        print(traceback.print_exc())
        raise FileNotFoundError

    try:
        print("Scraping "+ path)
        soup = BeautifulSoup(open(path))
    except:
        print("Data file missing, PATH: " + path)
        print(traceback.print_exc())

    # check for country, city and type
    try:
        assert(check_header(soup, city, mode='hourly')), "Wrong city name in header: {}".format(city)
    except:
        print("Wrong header for city =" + city + " hourly")
        print(traceback.print_exc())

    # define hourly scraping classes
    hour_class = '[ half-left ][ bg--white ][ cover-top ][ text--blue-dark ]'
    temp_class = '[ half-left ][ bg--white ][ js-detail-value-container ]'
    rainprob_class = 'mt--'
    rainAmount_class = '[ mb-- ][ block ][ text--small ][ absolute absolute--left ][ one-whole ]'
    windDir_class = '[ mb- ][ block ]'
    windAmount_class = '[ js-detail-value-container ][ one-whole ][ mb- ][ text--small ]'
    pressure_class = '[ mb- mt-- ][ block ][ text--small ]'
    humidity_class = '[ mb-- ][ block ][ text--small ]'

    try:
        hours = soup.find_all('div', class_ = hour_class)
        # get the starting hour of the hour table
        starting_hour = int((hours[0].string.split()[0])[1])
    except:
        print("Scraping failed: starting hour")
        print(traceback.print_exc())

    # define the hour string list for indexing the dictionary correctly
    hour_strs = []
    # this is because the data on the website does not start at 00 hours but at "starting_hour” hours
    for i in range(24):
        s = "{:0>2}".format(np.mod(i+starting_hour,24))
        hour_strs.append(s)
        hourly_dict[s] = {}


    # SCRAPE TEMPERATURE
    try:
        # get all the temperature divs
        temps = soup.find_all('div', class_ = temp_class)
        # for every div, get the string, take the temperature value and save it in the matrix
        assert(len(temps)==24), "html format seems to have changed: missing temp entries"
        for j, div in enumerate(temps):
            hourly_dict[hour_strs[j]]['temp'] = float(div.string.split()[0])
    except:
        print("Scraping failed: temperature")
        print(traceback.print_exc())

    try:
        # SCRAPE Rain probs
        probs = soup.find_all('p', class_ = rainprob_class)[:24]
        for j, p in enumerate(probs):
            hourly_dict[hour_strs[j]]['rain_chance'] = float(p.string.split()[0])
    except:
        print("Scraping failed: rain probs")
        print(traceback.print_exc())

    try:
        # SCRAPE Rain amounts
        amounts = soup.find_all('span', class_ = rainAmount_class)
        for j, span in enumerate(amounts):
            hourly_dict[hour_strs[j]]['rain_amt'] = float(span.text.split()[0])
    except:
        print("Scraping failed: rain amounts")
        print(traceback.print_exc())

    try:
        # SCRAPE Wind directions
        windDirs = soup.find_all('span', class_=windDir_class)
        for j, span in enumerate(windDirs):
            hourly_dict[hour_strs[j]]['wind_dir'] = span.text
            pass
    except:
        print("Scraping failed: hourly wind directions")
        print(traceback.print_exc())

    try:
        # SCRAPE Wind speed
        wstr = soup.find_all('div', class_=windAmount_class)
        for j, div in enumerate(wstr):
            # convert to m/s
            hourly_dict[hour_strs[j]]['wind_speed'] = round(float(div.string.split()[0])/3.6, 2)
    except:
        print("Scraping failed: hourly wind speed")
        print(traceback.print_exc())

    try:
        # SCRAPE pressure
        airpress = soup.find_all('span', class_ = pressure_class)
        for j, span in enumerate(airpress):
            hourly_dict[hour_strs[j]]['pressure'] = float(span.text.split()[0])
            pass
    except:
        print("Scraping failed: hourly pressure")
        print(traceback.print_exc())

    try:
        # SCRAPE air humidity
        airhum = soup.find_all('span', class_=humidity_class)
        for j, span in enumerate(airhum):
            hourly_dict[hour_strs[j]]['humidity'] = float(span.text.split()[0])
    except:
        print("Scraping failed: hourly humidity")
        print(traceback.print_exc())
    """
    wetter.com hourly predicitions always start at 6am. predicting the past
    does not make sense. Thus, we will add the 'past' prediction to a new
    dictionary and use it for the next day.
    """
    # construct next day hour indices
    next_day_idx = ['00', '01', '02', '03', '04', '05']
    # add to new dictionary
    hourly_dict_next_day = {}
    for hourIDX in next_day_idx:
        # add hour to next day dict
        hourly_dict_next_day[hourIDX] = hourly_dict[hourIDX]
        # remove hour from current day dict
        hourly_dict.pop(hourIDX)
    return hourly_dict, hourly_dict_next_day

def scrape_daily(date, city, data_path='../data'):
    """Scrapes daily data from html file containing the daily data of the
    given date and city
    :param date: should be in the format 30-05-2016
    :param city: should be the english city name, i.e., cologne, kassel, munich
    :param data_path: relative path to the directory where html files live
    :return daily_dict: dictionary holding the daily data
    """

    # define dict
    daily_dict = {}
    days = 16

    # try to open the file
    try:
        path = data_path + '/' + get_filename(data_path, date, city, mode='daily')
    except:
        print("Can't find PATH: " + data_path + ' ' + date + ' ' + city + ' daily')
        print(traceback.print_exc())
        raise FileNotFoundError

    try:
        print("Scraping "+ path)
        soup = BeautifulSoup(open(path))
    except FileNotFoundError:
        print("Data file missing, PATH: " + path)
        print(traceback.print_exc())

    # check for country, city and type
    try:
        assert(check_header(soup, city, mode='daily')), "Wrong city name in header: {}".format(city)
    except:
        print("Wrong header for city =" + city + " daily")
        print(traceback.print_exc())

    # define daily scraping classes
    temp_low_class = 'inline text--white gamma'
    temp_high_class = 'text--white beta inline'

    days_strs = []
    # prelocate dict
    for i in range(days):
        s = "{}".format(i+1)
        # make list of dict string keys encoding days: '0', '1',...,'15'
        days_strs.append(s)
        daily_dict[s] = {}

    try:
        # SCRAPE TEMPERATURE
        # get all the high temperature divs
        temps_high = soup.find_all('div', class_=temp_high_class)
        # for every div, get the string, take the temperature value and save it in the matrix
        assert(len(temps_high)==days), "not enough temperatures extracted"
        for j, div in enumerate(temps_high):
            # get the length of the string in div to be sensitive to one/two digit numbers
            # format is 4° vs. 14°
            str_len = len(div.string)
            daily_dict[days_strs[j]]['high'] = float(div.string[:(str_len-1)])
        # low
        temps_low = soup.find_all('div', class_=temp_low_class)
        # for every div, get the string, take the temperature value and save it
        assert(len(temps_low)==days), "not enough temperatures extracted 24!={}".format(len(temps_low))
        for j, div in enumerate(temps_low):
            str_len = len(div.string)
            daily_dict[days_strs[j]]['low'] = float(div.string[3:(str_len-1)])
    except:
        print("Scraping failed: daily temperature")
        print(traceback.print_exc())

    # SCRAPE all other values: it is all hard coded in a big string, buggy

    # get the sun hours idxs as starting point for every day
    div_jungle = soup.findAll('div', {'class':'flag__body'})
    # there are the position of the sun hours for day block in jungle
    start_idxs_detailed = np.arange(12, 96, 12)
    #print("detailed idx {}".format(start_idxs_detailed))
    dayIDX = 0 # need external day idx to use two different for looops

    for idx in start_idxs_detailed:
        rain_offset = 3 # the rain data is 3 lines further down
        wind_offset = 4 # the rain data is 4 lines further down
        measurements = 4 # measurements for the detailed daily data
        rain_chance = rain_amt = wind_speed = 0. # prelocate
        rain_str_threshold = 10
        for k in range(measurements):
            # rainchance, sum up for every measurement
            rain_chance += float(div_jungle[idx+rain_offset+2*k].text[:3])
            # rain amount is only displayed for high chance of rain
            if len(div_jungle[idx+rain_offset+2*k].text)>rain_str_threshold:
                rain_amt += float(div_jungle[idx+rain_offset+2*k].text[8:-5])
            else:
                rain_amt += 0.
            # find comma after wind direction
            commaIdx = div_jungle[idx+wind_offset+2*k].text.find(',')
            wind_speed += float(div_jungle[idx+wind_offset+2*k].text[commaIdx+2:commaIdx+4])
        # log results, take mean over daily measurements
        daily_dict[days_strs[dayIDX]]['rain_chance'] = rain_chance/measurements
        daily_dict[days_strs[dayIDX]]['rain_amt'] = rain_amt/measurements
        daily_dict[days_strs[dayIDX]]['wind_speed'] = wind_speed/measurements
        # save sun hours
        daily_dict[days_strs[dayIDX]]['sun_hours'] = float(div_jungle[idx].text[:-3])
        dayIDX += 1

    # get data for less detailed daily data
    start_idxs = np.arange(96, 132, 4)
    for idx in start_idxs:
        # save sun hours
        daily_dict[days_strs[dayIDX]]['sun_hours'] = float(div_jungle[idx].text[:-3])
        # the length of the string determines whether we have a rain amt in the data
        rain_str_threshold = 10
        rain_chance = float(div_jungle[idx+1].text[:3])
        if len(div_jungle[idx+1].text)>rain_str_threshold:
            rain_amt = float(div_jungle[idx+1].text[5:-5])
        else:
            rain_amt = 0.
        # log results
        daily_dict[days_strs[dayIDX]]['rain_chance'] = rain_chance
        daily_dict[days_strs[dayIDX]]['rain_amt'] = rain_amt

        # increment days idx
        dayIDX += 1

    return daily_dict

def get_filename(dirpath, date, city, mode='hourly'):
    """Looks up filename of the html file in dirpath for given date and city
    :param dirpath: relative path to the data directory
    :param date: date in the format 31-05-2016
    :param city: city as string
    :param mode: daily or hourly data
    """
    path = None
    filelist = os.listdir(dirpath)
    for f in filelist:
        if (date in f) and (city in f) and ( mode in f):
            path = f
    return path

def check_header(soup, city, mode='hourly'):
    """Checks the header in the html file. Ensure that city and county are
    plausible

    :param soup: BeautifulSoup object holding the html file representation
    :param mode: hourly or daily scraping mode
    :return result: True, False if the header test passed, failed, respectively
    """
    result = True
    # map city name from english to german
    if city in ['munich', 'muenchen']:
        city = 'münchen'
    if city in ['nuremberg', 'nuernberg']:
        city = 'nürnberg'
    if city=='saarbruecken':
        city = city.replace('ue', 'ü')
    if city in ['cologne', 'koeln']:
        city = 'köln'
    if city=='frankfurt':
        city = 'frankfurt am main'
    if city=='hanover':
        city = 'hannover'
    if city in ['cassel', 'kassel']:
        city = 'kassel'
    header_class = "[ breadcrumb__item ]"
    header = soup.find_all('span', class_ = header_class)
    if not(header[3].text == 'Deutschland'): result = False
    if not(header[5].text.lower() == city): result = False
    if mode=='hourly':
        mode_str = 'Heute'
    elif mode=='daily':
        mode_str = '16-Tage Trend'
    if not(header[6].text==mode_str): result = False
    return result
