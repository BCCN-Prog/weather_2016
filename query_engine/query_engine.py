import sys
sys.path.append('../')

from wrapper.DataWrapH5py import Daily_DataBase

class QueryEngine:

    def get_data_point(self, loc, date_time, daily_hourly, historical_scraping, parameters):
        if daily_hourly == 'd':
            db = Daily_DataBase()
            return db.extract_data_point(loc, date_time, parameters)