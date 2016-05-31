import sys
sys.path.append('../')

from wrapper.DataWrapH5py import Daily_DataBase

city_dict = {'berlin': 91}
param_dict = {'high': 3, 'low': 4}

class QueryEngine:

    def __init__(self):
        self.db = Daily_DataBase()
    
    def get_data_point(self, loc, date_time, daily_hourly, historical_scraping, param):
        if daily_hourly == 'd':
            return self.db.extract_data_point(city_dict[loc], date_time, param_dict[param])
        elif daily_hourly == 'h':
            return self.db.extract_data_point(city_dict[loc], date_time, param_dict[param])