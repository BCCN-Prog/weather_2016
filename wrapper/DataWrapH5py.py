import h5py
import datetime
import pandas as pd
import numpy as np
import glob

class DataBase:
    """"
    This class stores two datasets in the binary dailydata.hdf5:

    "weather_data" := matrix with every row representing a database entry with
                      the respective properties.
                      a new matrix is initialized with dimensions (400, 9)
                      400 is the initial row count (with hard limit at 2*1e6)
                      9 is the number of categories of data (hard limit 15)
    "metadata" := contains in its first entry the pointer to the first unwritten
                  row of the matrix, in the second the time and day the database
                  was last changed.
    """
    def __init__(self, file_name, row_num_init, row_num_max, categ_num_init, categ_num_max, make_new=False):
        self.cities = {'berlin': 1, 'hamburg': 2, 'munich': 3, 'muenchen': 3,
                       'koeln': 4, 'cologne': 4, 'frankfurt': 5, 'stuttgart': 6,
                       'bremen': 7, 'leipzig': 8, 'hannover': 9, 'hanover': 9,
                       'nuernberg': 10, 'nuremburg': 10, 'nuremberg': 10, 'dortmund': 11, 'dresden': 12,
                       'kassel': 13, 'cassel': 13, 'kiel': 14, 'bielfeld': 15, 'bielefeld': 15, 'saarbrucken': 16,
                       'saarbruecken': 16, 'rostock': 17, 'freiburg': 18,
                       'magdeburg': 19, 'erfurt': 20}

        if make_new == False:
            try:
                self.f = h5py.File(file_name, "r+")
            except:
                self.f = h5py.File(file_name, "w")
                self.f.create_dataset("weather_data",
                                    (row_num_init, categ_num_init),
                                    maxshape=(row_num_max, categ_num_max),
                                    dtype='float64')
                self.f.create_dataset("metadata", (2, ), dtype='uint64')

                # initialize row pointer and intial write time
                self.f["metadata"][0] = 0
                self.f["metadata"][1] = self.get_cur_datetime_int()
        else:
                self.f = h5py.File(file_name, "w")
                self.f.create_dataset("weather_data",
                                    (row_num_init, categ_num_init),
                                    maxshape=(row_num_max, categ_num_max),
                                    dtype='float64')
                self.f.create_dataset("metadata", (2, ), dtype='uint64')

                # initialize row pointer and intial write time
                self.f["metadata"][0] = 0
                self.f["metadata"][1] = self.get_cur_datetime_int()


    def get_cur_datetime_int(self):
        '''
        returns an int of the form YearMonthDayHourMinuteSecond.
        '''
        now = datetime.datetime.now()
        return int(now.strftime('%Y%m%d%H%M%S'))

    def add_data_matrix(self, matrix):
        '''
        vectorized implementation of add_data_point
        add_data_matrix adds a matrix of data after checking if a resize is in order.
        '''
        assert(matrix.shape[1] == self.f["weather_data"].shape[1])
        while self.f["metadata"][0] >= self.f["weather_data"].shape[0]-matrix.shape[0]:
            self.f["weather_data"].resize(self.f["weather_data"].shape[0]*2, 0)
        assert self.f["weather_data"][self.f["metadata"][0]:int(self.f["metadata"][0])+matrix.shape[0], :].shape == \
            matrix.shape
        self.f["weather_data"][self.f["metadata"][0]:int(self.f["metadata"][0])+matrix.shape[0], :] = matrix

        self.f["metadata"][0] += matrix.shape[0]
        self.f["metadata"][1] = self.get_cur_datetime_int()

    def get_capacity(self):
        return self.f['weather_data'].shape

    def number_entries(self):
        return self.f['metadata'][0]

    def get_sort_indices(self, param):
        '''
        Gets indices for dataset sorted along the param-entry. This can and should be used
        for presorting- and slicing the matrix ahead of time in order to increase performance.
        '''
        assert(param < self.f["weather_data"].shape[1])
        return np.argsort(self.f["weather_data"][:self.f["metadata"][0], param])
	#what if nan-->sorted to the end, keep in mind.

    def create_presorted(self, params):
        '''
        Creates presorted datasets in f, corresponding to params (a list).
        If, for example params=['date', 'high'], we will get 2 new datasets named
        "date_indices" and "high_indices" which contain the sorted indices wrt to
        date and high.
        '''
        params_int = [self.categories_dict[i] for i in params]
        for i in range(len(params)):
            ind = self.get_sort_indices(params_int[i])
            database_name = "{}_indices".format(params[i])
            #temp = self.f["weather_data"][:,params_int[i]][ind]
            self.f.create_dataset(database_name, data=ind)

            #also, watch out for nans

class Daily_DataBase(DataBase):
    def __init__(self, db_name="daily_database.hdf5", make_new=False):
        daily_categories = ['date', 'site', 'station_id', 'high', 'low', 'midday',
                            'rain_chance', 'rain_amt', 'cloud_cover', 'city_ID', 'day']

        DataBase.__init__(self,
                          file_name=db_name,
                          row_num_init=400,
                          row_num_max=4000000000,
                          categ_num_init=len(daily_categories),
                          categ_num_max=15,
                          make_new=make_new
                          )

    params_dict = {0:'date', 1:'site', 2:'station_id', 3:'high', 4:'low', 5:'midday', \
                   6:'rain_chance', 7:'rain_amt', 8:'cloud_cover', 9:'city_ID', 10:'day'}
    categories_dict = {'date':0, 'site':1, 'station_id':2,'high':3, 'low':4, 'midday':5, \
                       'rain_chance':6, 'rain_amt':7, 'cloud_cover':8, 'city_ID':9, 'day':10}

    def add_data_point(self, date, site, day, station_id, high, low, midday,
                       rain_chance, rain_amt, cloud_cover, city_ID):
        '''
        Adds a data point to the first empty row of the matrix pointed to by
        self.f['metadata'][0] then advances it and updates f["metadata"][1].

        If the pointer is at the last row, the weather_data matrix is resized.
        '''
        if self.f["metadata"][0] == self.f["weather_data"].shape[0]:
            self.f["weather_data"].resize(self.f["weather_data"].shape[0]*2, 0)

        self.f["weather_data"][self.f["metadata"][0], 0] = date
        self.f["weather_data"][self.f["metadata"][0], 1] = site  # website (0-4) or historical (5)
        self.f["weather_data"][self.f["metadata"][0], 2] = station_id
        self.f["weather_data"][self.f["metadata"][0], 3] = high
        self.f["weather_data"][self.f["metadata"][0], 4] = low
        self.f["weather_data"][self.f["metadata"][0], 5] = midday
        self.f["weather_data"][self.f["metadata"][0], 6] = rain_chance
        self.f["weather_data"][self.f["metadata"][0], 7] = rain_amt
        self.f["weather_data"][self.f["metadata"][0], 8] = cloud_cover
        self.f["weather_data"][self.f["metadata"][0], 9] = city_ID  # city
        self.f["weather_data"][self.f["metadata"][0], 10] = day  # how many days in future forecasted


        self.f["metadata"][1] = self.get_cur_datetime_int()
        self.f["metadata"][0] += 1

    def import_from_csv(self, file_name):
        '''
        Adds data from csv structure of historic group. So far, this is all specific to
        the fixed structures in this class.
        '''
        df = pd.read_csv(file_name, usecols=[2, 1, 10, 11, 14, 6])

        df = np.array(df.values)
        site = np.ones((df.shape[0],1))*5
        midday = np.array([[np.nan] for i in range(df.shape[0])])
        rain_chance = np.array([[np.nan] for i in range(df.shape[0])])
        city_id = np.array([[np.nan] for i in range(df.shape[0])])
        day = np.array([[np.nan] for i in range(df.shape[0])])

        df = np.hstack((df, site, midday, rain_chance, city_id, day))[:, [1, 6, 0, 3, 4, 7, 8, 5, 2, 9, 10]]

        self.add_data_matrix(df)
        # should be more general.

    def auto_csv(self):
        for f in glob.glob("./*_daily.csv"):
            self.import_from_csv(f)

    def save_dict(self, daily_dict):

        params = ['station_id', 'high', 'low', 'midday', 'rain_chance', 'rain_amt', 'cloud_cover']

        try:
            date = daily_dict['date']
        except:
            print('save_daily_dict: No date')
            return 0

        try:
            website = daily_dict['site']
        except:
            print('save_daily_dict: No site')
            return 0

        data = daily_dict['daily']
        city_ID = self.cities[daily_dict['city']]

        for day_key, _d in data.items():
            arg_dict = {'date': date, 'site': website, 'day': int(day_key),
                        'city_ID': city_ID}

            for param in params:
                try:
                    if _d[param] == None:
                        arg_dict[param] = np.nan
                    else:
                        arg_dict[param] = _d[param]
                except:
                    arg_dict[param] = np.nan

            self.add_data_point(**arg_dict)

    def extract_data_point(self, location_id, time, param):
        '''
        function just for mvp, not efficient and uses items not to be used later.
        '''
        data = self.f["weather_data"]

        n = data.shape[0]
        idx = data[:, 2] == location_id
        idx = np.arange(n)[idx]

        temp = data[idx, :]

        n = temp.shape[0]
        idx = temp[:, 0] == time
        idx = np.arange(n)[idx]

        ret = temp[idx, :]
        # print(ret.shape)

        if(len(ret.shape) > 1):
            return ret[0, param]
        return ret[param]


class Hourly_DataBase(DataBase):
    def __init__(self, db_name="hourly_database.hdf5", make_new=False):
        hourly_categories = ['date', 'hour', 'site', 'geolocation', 'temperature', 'humidity',
                             'wind_speed', 'rain_chance', 'rain_amt', 'cloud_cover', 'city_ID']

        DataBase.__init__(self,
                          file_name=db_name,
                          row_num_init=4000,
                          row_num_max=300000000,
                          categ_num_init=len(hourly_categories),
                          categ_num_max=15,
                          make_new=make_new
                          )

    def add_data_point(self, date, hour, site, station_id, temperature, humidity,
                       wind_speed, rain_chance, rain_amt, cloud_cover, city_ID):
        if self.f["metadata"][0] == self.f["weather_data"].shape[0]:
            self.f["weather_data"].resize(self.f["weather_data"].shape[0]*2, 0)

        self.f["weather_data"][self.f["metadata"][0], 0] = date
        self.f["weather_data"][self.f["metadata"][0], 1] = hour
        self.f["weather_data"][self.f["metadata"][0], 2] = site
        self.f["weather_data"][self.f["metadata"][0], 3] = station_id
        self.f["weather_data"][self.f["metadata"][0], 4] = temperature
        self.f["weather_data"][self.f["metadata"][0], 5] = humidity
        self.f["weather_data"][self.f["metadata"][0], 6] = wind_speed
        self.f["weather_data"][self.f["metadata"][0], 7] = rain_chance
        self.f["weather_data"][self.f["metadata"][0], 8] = rain_amt
        self.f["weather_data"][self.f["metadata"][0], 9] = cloud_cover
        self.f["weather_data"][self.f["metadata"][0], 10] = city_ID

        self.f["metadata"][1] = self.get_cur_datetime_int()
        self.f["metadata"][0] += 1

    def save_dict(self, hourly_dict):
        params = ['station_id', 'temperature', 'humidity', 'wind_speed',
                  'rain_chance', 'rain_amt', 'cloud_cover']

        try:
            date = hourly_dict['date']
        except:
            raise Exception('save_hourly_dict: hourly dictionary has no date')

        try:
            website = hourly_dict['site']
        except:
            raise Exception('save_hourly_dict: hourly dictionary has no site')

        data = hourly_dict['hourly']
        city_ID = self.cities[hourly_dict['city']]

        for hour_key, _d in data.items():
            arg_dict = {'date': date, 'site': website, 'hour': int(hour_key),
                        'city_ID': city_ID}

            for param in params:
                try:
                    if _d[param] == None:
                        arg_dict[param] = np.nan
                    else:
                        arg_dict[param] = _d[param]
                except:  # item doesn't exist
                    arg_dict[param] = np.nan


            self.add_data_point(**arg_dict)






# before creating database: unique timestamp for files already down and new files
# convert cities to PLZ
# to do: scrpt that converts PLZ to geolocation
# site indexing
# delete function
# change HourlyData
