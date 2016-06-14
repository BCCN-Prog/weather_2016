import pickle
import numpy as np
import datetime


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
    try:
        date = int('{}{}{}'.format(year, month, day))
    except ValueError: print ('Filename must have changed, should start with wunderground_dd_mm_yyyy') 
    loc3 = fn[30:33] #first 3 location letters
    return date,loc3
    

def scrape (filename):
    with open(filename, 'rb') as f:
        dat = pickle.load(f)
        f.close()
    if ('hourly_forecast' in dat.keys()):
        res = scrape_hourly (dat)
    elif ('forecast' in dat.keys()):
        res = scrape_daily (dat)
    else: raise Exception ('File data cannot be recognized')
    
    fnd, fl3 = get_data_from_fn (filename)
    if not (res['date'] == fnd): raise Exception ('File name date and date of data not coherent')
    if not (res['city'][:3] == fl3): raise Exception ('File name locaction and location in data not coherent')
    return res
    

    
    
def scrape_daily (dat):
    res = {}
    res['site'] = 5 # weather underground has ID 5
    res['city'] = dat['location']['city']
    datf = dat['forecast']['simpleforecast']['forecastday']
    month = str(datf[0]['date']['month'])
    if len (month)<2: month = '0' + month
    day = str(datf[0]['date']['day'])
    if len(day)<2: day = '0' + day
    year = datf[0]['date']['year']
    date = '{}{}{}'.format(year, month, day)
    res['date'] = int(date) #check for sanity here!
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
    return res
    
    

def scrape_hourly (dat):
    res = {}
    res['site'] = 5 # weather underground has ID 5
    res['city'] = dat['location']['city']
    month = (dat['hourly_forecast'][0]['FCTTIME']['mon_padded'])
    day = (dat['hourly_forecast'][0]['FCTTIME']['mday_padded'])
    year = (dat['hourly_forecast'][0]['FCTTIME']['year'])
    date = '{}{}{}'.format(year, month, day)
    res['date'] = int(date) #check for sanity here!
    res['hourly'] = {}
    maxp = len(dat['hourly_forecast']) #modify this depending on how much and how the data shall be stored
    for i in range(maxp):
        hr = {}
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
        res['hourly']["{}".format(str(i))] = hr
    return res

if __name__ == '__main__':
    d = scrape('./ex_data/wunderground_08_06_2016_10_36_Berlin_10days.pkl')
    print ('done daily')
    h = scrape('./ex_data/wunderground_08_06_2016_10_36_Berlin_hourly.pkl')
    print ('done daily')
    #print (d)
        
    
    
    
 

