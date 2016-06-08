import pickle
import numpy as np
import datetime


def scrape (filename):
    with open(filename, 'rb') as f:
        dat = pickle.load(f)
        f.close()
        fnd, fl3 = get_date_from_fn (filename)
        print (fnd)
        print (fl3)
    if ('hourly_forecast' in dat.keys()):
        res = scrape_hourly (dat)
    elif ('forecast' in dat.keys()):
        res = scrape_daily (dat)
    else: raise Exception ('File data cannot be recognized')
    return res
    
def get_date_from_fn (fn):
    day = fn[13:15]
    month = fn[16:18]
    year = fn[19:23]
    date = int('{}{}{}'.format(year, month, day))
    loc3 = fn[30:33] #first 3 location letters
    return date,loc3
    
    
def scrape_daily (dat):
    res = {}
    res['site'] = 'weather underground' #!add right number once it is  assigned
    res['city'] = dat['location']['city']
    datf = dat['forecast']['simpleforecast']['forecastday']
    month = datf[0]['date']['month']
    day = datf[0]['date']['day']
    year = datf[0]['date']['year']
    date = '{}{}{}'.format(year, month, day)
    res['date'] = int(date) #check for sanity here!
    res['daily'] = {} #day 0 is the forecast for the day the prediction is made. Might be good to check though.
    
    for i in range(len(datf)):
        dr = {}
        dr['high'] = float(datf[0]['high']['celsius'])
        dr['low'] = float(datf[0]['low']['celsius'])
        dr['rain_chance']= float(datf[0]['pop'])
        dr['rain_amt'] = float(datf[0]['qpf_allday']['mm'])
        dr['pressure'] = np.NaN
        dr['cloud_cover']  = np.NaN
        res['daily']["{}".format(str(i))] = dr
        
    return res

def scrape_hourly (dat):
    res = {}
    res['site'] = 'weather underground' #!add right number once it is  assigned
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
        hr['humidity'] = float(dat['hourly_forecast'][i]['humidity'])
        hr['pressure'] = float(dat['hourly_forecast'][i]['mslp']['metric'])
        hr['wind_speed'] = float(dat['hourly_forecast'][i]['wspd']['metric'])
        hr['rain_amt'] = float(dat['hourly_forecast'][i]['qpf']['metric'])
        hr['rain_chance'] = float(dat['hourly_forecast'][i]['pop'])
        hr['cloud_cover'] = float(dat['hourly_forecast'][i]['sky'])
        res['hourly']["{}".format(str(i))] = hr
    return res

if __name__ == '__main__':
    d = scrape('wunderground_08_06_2016_10_36_Berlin_10days.pkl')
    print ('done')
    #print (d)
        
    
    
    
 

