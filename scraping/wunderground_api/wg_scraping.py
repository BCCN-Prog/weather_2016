import pickle
import sys
import os
sys.path.append('../')
sys.path.append('../../')
import numpy as np
import datetime
import test_scraper_output as tester
import pprint
import wrapper.DataWrapH5py as wrapper
from itertools import product

'''READ FIRST: In the download function, the daily and hourly data were swapped wrt the filename (yes, that is pretty stupid). Anyway, this code tries to check for any file that is loaded whether the data is daily or hourly by itself.'''

def get_data_from_fn (fn):
    '''extracts data from the filename for chacking
    Input:
    fn, the filename as string
    Returns:
    date: int in format YYYYMMDD
    t_st: int in format YYYYMMDDhhmm (redundant, but used for different things)
    loc3: first 3 letters of the location'''
    
    
    # first step: if the filename is a path, remove everything from the path
    gr =  [pos for pos, char in enumerate(fn) if char == '/']
    gr.append(0)
    os = max(gr)
    fn = fn[os+1:]
    #get date data
    day = fn[13:15]
    month = fn[16:18]
    year = fn[19:23]
    hour = fn[24:26]
    minute = fn[27:29]
    try:
        date = int('{}{}{}'.format(year, month, day))
        t_st = int('{}{}{}{}{}'.format(year, month, day, hour, minute)) #timestamp
    except ValueError: print ('Filename must have changed, should start with wunderground_dd_mm_yyyy') 
    loc3 = (fn[30:33]).lower() #first 3 location letters
    return date,t_st, loc3


def prepend_0_if_single_digit(x):
    return '0' + str(x) if len(x) == 1 else x
    
def dict_type (my_dict):
    '''finds out if dict contains daily hourly, or no data, 
    returns: 'd' for daily, 'h' for hourly, 'e' for empty '''
    if len(my_dict['hourly']) == 0 and len(my_dict['daily']) == 0:
        return 'e'
    elif not len(my_dict['hourly']) == 0 and len(my_dict['daily']) == 0:
        return 'h'
    elif len(my_dict['hourly']) == 0 and not len(my_dict['daily']) == 0:
        return 'd'
    else: raise Exception ('Dict contains data for both hourly and daily')
   
def scrape(date, city, data_path):

    '''Function calls filename scraping function from the given parameters and returns three dictionaries: One with the daily forecasts, Two with the hourly forecasts, one for this, the other for the next day. Downloading function does have a bug so hourly data is stored in file that is named daily and the other way around.'''
    daily_db = wrapper.Daily_DataBase()
    hourly_db = wrapper.Hourly_DataBase()

    #date[2,5] = '_'
    hours = [prepend_0_if_single_digit(str(i)) for i in range(24)]
    minutes = [prepend_0_if_single_digit(str(i)) for i in range(60)] 
    city = city[0].upper() + city[1:] #set first letter of city uppercase
    for hour, minute in product(hours,minutes):
        name1 = data_path + "/wunderground_{}_{}_{}_{}_hourly.pkl".format(date, hour, minute, city)
        name2 = data_path + "/wunderground_{}_{}_{}_{}_10days.pkl".format(date, hour, minute, city)
        if os.path.exists(name1):
            [d, d1] = scrape_from_filename(name1)
            print (tester.run_tests(d))
            print (tester.run_tests(d1))
            for obj in [d, d1]:
                if dict_type(obj) == 'h':
                    hourly_db.save_dict(obj)
                elif dict_type(obj) == 'd':
                    daily_db.save_dict(obj)
        if os.path.exists(name2):
            [h, h1] = scrape_from_filename(name2)
            print (tester.run_tests(h))
            print (tester.run_tests(h1))
            for obj in [h, h1]:
                if dict_type(obj) == 'h':
                    hourly_db.save_dict(obj)
                elif dict_type(obj) == 'd':
                    daily_db.save_dict(obj)          



def scrape_from_filename (filename):
    '''function loads the file, finds out whether the data is hourly or daily and scrapes according to this.
    Returns: Two dicts, one of them does not contain data for daily case'''
    with open(filename, 'rb') as f:
        dat = pickle.load(f)
        f.close()
    fnd, t_st, fl3 = get_data_from_fn (filename)
    res1 = {}
    if ('hourly_forecast' in dat.keys()):
        res, res1 = scrape_hourly (dat, t_st)
    elif ('forecast' in dat.keys()):
        res,res1 = scrape_daily (dat, t_st)
    else: raise Exception ('File data cannot be recognized')
    if not (res['date'] == fnd): raise Exception ('File name date and date of data not coherent')
    if not (res['city'][:3] == fl3): raise Exception ('File name locaction and location in data not coherent')
    return [res, res1]
    
def gen_basic_dict (city, pred_t, date):
    '''produces an empty dictionary with only the basic information'''
    res = {}
    res['site'] = 5 # weather underground has ID 5
    res['city'] = city
    res['prediction_time'] = pred_t
    res['date'] = date
    res['hourly'] = {}
    res['daily'] = {}
    return res
    
    
    
    
    
def scrape_daily (dat, t_st):

    '''scrapes daily data
    Input:
    dat: loaded pkl file with daily dat
    t_st: time stemp, YYYYMMDDhhmm int
    Returns:
    2 dicts, one of them containing the daily data, one  of them empty'''
    
    city = (dat['location']['city']).lower()

    datf = dat['forecast']['simpleforecast']['forecastday']
    month = str(datf[0]['date']['month'])
    if len (month)<2: month = '0' + month
    day = str(datf[0]['date']['day'])
    if len(day)<2: day = '0' + day
    year = datf[0]['date']['year']
    date = '{}{}{}'.format(year, month, day)
    
    res = gen_basic_dict(city, t_st, int(date))
    res1 = gen_basic_dict(city, t_st, int(date)) #both functions should give back two dicts so this one is going to stay empty (a la whatever works)

    for i in range(len(datf)):
        dr = {}
        
        dr['high'] = float(datf[0]['high']['celsius'])
        if dr['high'] > 50. or dr['high'] < -20. : raise Exception ('High temp does not seem realistic')
        
        dr['low'] = float(datf[0]['low']['celsius'])
        if dr['low'] > 50. or dr['low'] < -20. : raise Exception ('Low temp does not seem realistic')
        
        dr['rain_chance']= float(datf[0]['pop'])
        if dr['rain_chance'] > 101. or dr['rain_chance'] < -1. : raise Exception ('Rain chance (daily) does not seem realistic')
        dr['rain_amt'] = float(datf[0]['qpf_allday']['mm'])
        dr['pressure'] = np.NaN
        dr['cloud_cover']  = np.NaN
        res['daily']["{}".format(str(i))] = dr
    pp = pprint.PrettyPrinter(indent = 2)
    #pp.pprint(res)
    return res, res1
    
    

def scrape_hourly (dat, t_st):  
    '''scrapes hourly data
    Input:
    dat: loaded pkl file with hourly data
    t_st: time stemp, YYYYMMDDhhmm int
    Returns:
    2 dicts, first one with the predictions on the day of the scraping, one with the predictions for the following day'''

    city = (dat['location']['city']).lower()
    
    month0 = (dat['hourly_forecast'][0]['FCTTIME']['mon_padded'])
    day0 = (dat['hourly_forecast'][0]['FCTTIME']['mday_padded'])
    year0 = (dat['hourly_forecast'][0]['FCTTIME']['year'])
    date0 = '{}{}{}'.format(year0, month0, day0)
    res = gen_basic_dict(city, t_st, int(date0))
       
    maxp = len(dat['hourly_forecast']) #gets amount of hourly data packages that are stored
    month1 = (dat['hourly_forecast'][maxp-1]['FCTTIME']['mon_padded'])
    day1 = (dat['hourly_forecast'][maxp-1]['FCTTIME']['mday_padded'])
    year1 = (dat['hourly_forecast'][maxp-1]['FCTTIME']['year'])
    date1 = '{}{}{}'.format(year1, month1, day1)
    res1 = gen_basic_dict(city, t_st, int(date1))

    first_day = dat['hourly_forecast'][0]['FCTTIME']['mday_padded']
    for i in range(maxp):
        hr = {}
        this_hr = dat['hourly_forecast'][i]['FCTTIME']['hour']
        hr['temp'] = float(dat['hourly_forecast'][i]['temp']['metric'])
        if hr['temp'] > 50. or hr['temp'] < -20. : raise Exception ('temp (hourly) does not seem realistic')
        
        hr['humidity'] = float(dat['hourly_forecast'][i]['humidity'])
        if hr['humidity'] > 101. or hr['humidity'] < -1. : raise Exception ('Humidity (hourly) does not seem realistic')
        
        hr['pressure'] = float(dat['hourly_forecast'][i]['mslp']['metric'])
        if hr['pressure'] > 1100. or hr['pressure'] < -900. : raise Exception ('Humidity (hourly) does not seem realistic')
        
        hr['wind_speed'] = float(dat['hourly_forecast'][i]['wspd']['metric'])
        hr['rain_amt'] = float(dat['hourly_forecast'][i]['qpf']['metric'])
        
        hr['rain_chance'] = float(dat['hourly_forecast'][i]['pop'])
        if hr['rain_chance'] > 101. or hr['rain_chance'] < -1. : raise Exception ('Rain chance (hourly) does not seem realistic')
        hr['cloud_cover'] = float(dat['hourly_forecast'][i]['sky'])
        if dat['hourly_forecast'][i]['FCTTIME']['mday_padded'] == first_day:
            res['hourly']["{}".format(str(this_hr))] = hr
        else:
            res1['hourly']["{}".format(str(this_hr))] = hr
    #pp = pprint.PrettyPrinter(indent = 2)
    #pp.pprint(res)
    return res, res1

if __name__ == '__main__':
    # CAUTION: There was a mix-up of hourly and daily data, so what looks like
    # the dictionary is the hourly one and vice versa
    data_path = './ex_data'
    date= '08_06_2016'
    city = 'Berlin'
    scrape(date, city, data_path)
    #daily_db = wrapper.Daily_DataBase()
    #hourly_db = wrapper.Hourly_DataBase()
    #[d,  d1] = scrape('./ex_data/wunderground_08_06_2016_10_36_Berlin_10days.pkl'
    #hourly_db.save_dict(d)
    #hourly_db.save_dict(d1)
    #print (tester.run_tests(d))
    #print (tester.run_tests(d1))
    #print ('done daily')
    #h = scrape('./ex_data/wunderground_08_06_2016_10_36_Berlin_hourly.pkl')
    #daily_db.save_dict(h)
    #print ('done hourly')
    #print (tester.run_tests(h))

        
    
    
    
 

