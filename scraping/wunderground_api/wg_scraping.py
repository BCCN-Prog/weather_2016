import pickle
import sys
sys.path.append('../')
import numpy as np
import datetime
import test_scraper_output as tester
import pprint


def get_data_from_fn (fn):
    '''extracts data from the filename for chacking
    date in format YYYYMMDD
    loc3 are the first 3 letters of the location'''
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
    

def scrape (filename):
    with open(filename, 'rb') as f:
        dat = pickle.load(f)
        f.close()
    fnd, t_st, fl3 = get_data_from_fn (filename)
    res1 = {}
    if ('hourly_forecast' in dat.keys()):
        res, res1 = scrape_hourly (dat, t_st)
    elif ('forecast' in dat.keys()):
        res = scrape_daily (dat, t_st)
    else: raise Exception ('File data cannot be recognized')
    if not (res['date'] == fnd): raise Exception ('File name date and date of data not coherent')
    if not (res['city'][:3] == fl3): raise Exception ('File name locaction and location in data not coherent')
    if len(res1) == 0: return res
    else: return [res, res1]
    

    
    
def scrape_daily (dat, t_st):
    res = {}
    res['site'] = 5 # weather underground has ID 5
    res['city'] = (dat['location']['city']).lower()
    res['prediction_time'] = t_st
    datf = dat['forecast']['simpleforecast']['forecastday']
    month = str(datf[0]['date']['month'])
    if len (month)<2: month = '0' + month
    day = str(datf[0]['date']['day'])
    if len(day)<2: day = '0' + day
    year = datf[0]['date']['year']
    date = '{}{}{}'.format(year, month, day)
    res['date'] = int(date) #check for sanity here!
    res['hourly'] = {}
    res['daily'] = {} #day 0 is the forecast for the day the prediction is made. Might be good to check though.
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
    return res
    
    

def scrape_hourly (dat, t_st):  
    maxp = len(dat['hourly_forecast']) #gets amount of hourly data packages that are stored
    res = {}
    res1 = {}

    res['site'] = 5 # weather underground has ID 5
    res['city'] = (dat['location']['city']).lower()
    res['prediction_time'] = t_st
    month = (dat['hourly_forecast'][0]['FCTTIME']['mon_padded'])
    day = (dat['hourly_forecast'][0]['FCTTIME']['mday_padded'])
    year = (dat['hourly_forecast'][0]['FCTTIME']['year'])
    date = '{}{}{}'.format(year, month, day)
    res['date'] = int(date) #check for sanity here!
    res['hourly'] = {}
    res['daily'] = {}
    if (dat['hourly_forecast'][0]['FCTTIME']['mday_padded'] == dat['hourly_forecast'][maxp-1]['FCTTIME']['mday_padded']):
        two_dicts = False
    else: two_dicts = True   
    if two_dicts: 
        res1['site'] = 5 # weather underground has ID 5
        res1['city'] = (dat['location']['city']).lower()
        res1['daily'] = {}
        res1['prediction_time'] = t_st
        month = (dat['hourly_forecast'][maxp-1]['FCTTIME']['mon_padded'])
        day = (dat['hourly_forecast'][maxp-1]['FCTTIME']['mday_padded'])
        year = (dat['hourly_forecast'][maxp-1]['FCTTIME']['year'])
        date = '{}{}{}'.format(year, month, day)
        res1['date'] = int(date) #check for sanity here!
        res1['hourly'] = {}

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
        if two_dicts:
            if dat['hourly_forecast'][i]['FCTTIME']['mday_padded'] == first_day:
                res['hourly']["{}".format(str(this_hr))] = hr
            else:
                res1['hourly']["{}".format(str(this_hr))] = hr
        else:
            res['hourly']["{}".format(str(i))] = hr
    pp = pprint.PrettyPrinter(indent = 2)
    #pp.pprint(res)
    return res, res1

if __name__ == '__main__':
    [d,  d1] = scrape('./ex_data/wunderground_08_06_2016_10_36_Berlin_10days.pkl')
    print (tester.run_tests(d))
    print (tester.run_tests(d1))
    print ('done daily')
    h = scrape('./ex_data/wunderground_08_06_2016_10_36_Berlin_hourly.pkl')
    print ('done hourly')
    print (tester.run_tests(h))

        
    
    
    
 

