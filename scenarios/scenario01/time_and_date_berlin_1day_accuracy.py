from wrapper.DataWrapH5py import Daily_DataBase
import pandas as pd
import numpy as np
import pudb

pu.db  # @XXX
station_id = 1270
city_id = 20
site_id = 1
days_ahead = 1
hist_period = [20160601, 20160630]

HIST_DB = pd.read_csv('../../databases/daily_data_clean/{}_daily.csv'.format(station_id), \
                      usecols=['Date', 'Rain'], header=0, index_col=0)

hist_data = HIST_DB[hist_period[0] : hist_period[1]]

SCRAPE_DB = Daily_DataBase('../../databases/daily_database_scraping.hdf5')
scrape_data = SCRAPE_DB.f['weather_data']
scrape_indices = SCRAPE_DB.categories_dict

scraping_search = 'rain_chance'
scraping_period = [20160531, 20160629]

city_mat = scrape_data[scrape_data[:, scrape_indices['city_ID']] == city_id, :]
city_site_mat = city_mat[city_mat[:, scrape_indices['site']] == site_id, :]
city_site_day_mat = city_site_mat[city_site_mat[:, scrape_indices['day']] == days_ahead, :]

month_idx = city_site_day_mat[:, scrape_indices['date']] >= scraping_period[0] & \
            city_site_day_mat[:, scrape_indices['date']] <= scraping_period[1]

month_mat = city_site_day_mat[month_idx, scrape_indices['rain_chance']]
