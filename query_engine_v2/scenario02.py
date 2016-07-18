# Scenario 02

#import sys
#sys.path.append('../')
#sys.path.append('../wrapper/')
import QueryEngine
import numpy as np
import datetime
import h5py
import matplotlib.pyplot as plt

categories = {'date': 0, 'site': 1, 'station_id': 2, 'high': 3, 'low': 4, 'temperature': 5,
                   'rain_chance': 6, 'rain_amt': 7, 'cloud_cover': 8, 'city_ID': 9, 'day': 10}

def get_weekday(date_float):
    date_str = str(int(round(date_float)))
    date_obj = datetime.date(int(date_str[:4]), int(date_str[4:6]), int(date_str[6:]))
    return date_obj.weekday()
    
def is_weekend(date_float):
    wd = get_weekday(date_float)
    return wd > 4    

def extract(X, column, predicate, explanation):
    idx = predicate(X[:, explanation[column]])
    return X[idx, :]

def make_data(start):
    qe = QueryEngine.QueryEngine('daily_database.hdf5',
                                   'hourly_database.hdf5', make_new=False)
    
    #print(qe.daily.f['weather_data'][5,:])
    
    data, explanation = qe.smart_slice('daily', ['date', 'low', 'temperature','high', 'site', 'day', 'city_ID', 'station_id'], 'site', 6, 6)
    #data, explanation = qe.smart_slice('daily', ['date'], 'site', 1, 1)
    
#    print(explanation)
    #print(data.shape)
    
    # 20160428 is the first scraping date in this database
    data_2016 = extract(data, 'date', lambda x: x > start - 0.5, explanation)
    # 20160801 will be after the presentation
    data_2016 = extract(data_2016, 'date', lambda x: x < 20160709, explanation)
    
    # berlin-dahlem fu station has id 403
    data_2016_b = extract(data_2016, 'station_id', lambda x: x == 403, explanation)
    
    return data_2016_b, explanation

        
#data, explanation = make_data()
#data.sort(axis=0)
#print(data.shape)

def plot_comp(file_name, title='', day=0):
    h5 = h5py.File(file_name, 'r');
    forecast = h5['weather_data'][:]
    
    # remove zeroes from zero-padding
    forecast = extract(forecast, 'date', lambda x: x > 0, categories)
    # only look at berlin
    forecast = extract(forecast, 'city_ID', lambda x: x == 1, categories)
    # only forecast of 1 day ahead
    forecast = extract(forecast, 'day', lambda x: x == day, categories)
    forecast.sort(axis=0)
    
    data, explanation = make_data(np.min(forecast[:,0]))
    data.sort(axis=0)
    
    N = data.shape[0]
    
    forecast_plot = np.zeros((N, 2))
    delta = 0
    for i in range(N):
        if forecast[i - delta, 0] == data[i, 0]:
            forecast_plot[i, 0] = forecast[i - delta, 4]
            forecast_plot[i, 1] = forecast[i - delta, 3]
        else:
            forecast_plot[i, 0] = np.nan
            forecast_plot[i, 1] = np.nan
            delta += 1
        
    plt.figure(figsize=(8,5))
    plt.plot(forecast_plot[:,0], label='forecast low')
    plt.plot(forecast_plot[:,1], label='forecast high')
    plt.plot(data[:,4], label='actual low')
    plt.plot(data[:,3], label='actual high')
    plt.legend(loc='best')
    plt.title(title)
    plt.xlabel('days after May 5th 2016')
    plt.ylabel('temeprature [°C]')


plot_comp('daily_ow.hdf5', 'openweathermap.org', day=0)
#plot_comp('daily_dt.hdf5', 'timeanddate.com/weather (customweather)')



def we_wd_err(file_name):
    h5 = h5py.File(file_name, 'r');
    forecast = h5['weather_data'][:]
    
    # remove zeroes from zero-padding
    forecast = extract(forecast, 'date', lambda x: x > 0, categories)
    # only look at berlin
    forecast = extract(forecast, 'city_ID', lambda x: x == 1, categories)
    # only forecast of 1 day ahead
    forecast = extract(forecast, 'day', lambda x: x == 1, categories)
    forecast.sort(axis=0)
    
    data, explanation = make_data(np.min(forecast[:,0]))
    data.sort(axis=0)
    
    N = data.shape[0]
    
    delta = 0
    we_err = []
    wd_err = []
    err = []
    for i in range(N):
        if forecast[i - delta, 0] == data[i, 0]:
            if is_weekend(data[i, 0]):
                we_err += [forecast[i - delta, 4] - data[i, 4]]
            else:
                wd_err += [forecast[i - delta, 4] - data[i, 4]]
            err += [forecast[i - delta, 4] - data[i, 4]]
        else:
            delta += 1
    print('average prediction error low:')
    print('total:', np.mean(err))
    print('weekdays:', np.mean(we_err))
    print('weekends:', np.mean(wd_err))
    print()

    delta = 0
    we_err = []
    wd_err = []
    err = []
    for i in range(N):
        if forecast[i - delta, 0] == data[i, 0]:
            if is_weekend(data[i, 0]):
                we_err += [forecast[i - delta, 3] - data[i, 3]]
            else:
                wd_err += [forecast[i - delta, 3] - data[i, 3]]
            err += [forecast[i - delta, 3] - data[i, 3]]
        else:
            delta += 1
    print('average prediction error high:')
    print('total:', np.mean(err))
    print('weekdays:', np.mean(we_err))
    print('weekends:', np.mean(wd_err))

we_wd_err('daily_ow.hdf5')
































