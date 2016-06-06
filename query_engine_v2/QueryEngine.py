import sys
sys.path.append('../wrapper/')
import DataWrapH5py

class QueryEngine:
    daily_params = ['date', 'high'] #only for example
    hourly_params = ['date']

    def __init__(self, make_new=False):
        self.daily = DataWrapH5py.Daily_DataBase(make_new=make_new)
        self.hourly = DataWrapH5py.Hourly_DataBase(make_new=make_new)

        if make_new == True:
            self.daily.auto_csv()
            #call hourly equivalent here

            self.daily.create_presorted(self.daily_params)
            #self.hourly.create_presorted(self.hourly_params)
            #above line does not work yet because hourly database does not
            #have categories_dict yet
