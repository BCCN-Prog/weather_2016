import pickle
import numpy as np

def scrape (filename):
    with open(filename, 'rb') as f:
        dat = pickle.load(f)
        f.close()
    if ('hourly_forecast' in dat.keys()):
        res = scrape_hourly (dat)
    elif ('forecast' in dat.keys()):
        res = scrape_daily (dat)
    else: raise Exception ('File data cannot be recognized')
    return res
    
def scrape_daily (dat):
    pass

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
    d = scrape('test_hourly.pkl')
    print (d)
        
    
    
    
 

