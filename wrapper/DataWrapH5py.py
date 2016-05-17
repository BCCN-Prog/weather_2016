import h5py
import datetime

class DailyData:
    """"
This class stores two datasets in the binary dailydata.hdf5: "weather_data" and "metadata".
"weather_data" contains a matrix with every row representing a database entry with the respective
properties. "metadata" contains in its first entry the pointer to the last unwritten row of the matrix,
in the second the time and day the database was last changed.
get_cur_datetime_int() returns an int of the form YearMonthDayHourMinuteSecond. Add data point adds
a data point to the first empty row of the matrix, advances f["metadata"][0] and updates f["metadata"][1].
add_data_matrix adds a matrix of data after checking if a resize is in order.

    """
    def get_cur_datetime_int(self):
        now = datetime.datetime.now()
        return int(now.strftime('%Y%m%d%H%M%S'))

    def __init__(self):
        try:
            self.f = h5py.File("dailydata.hdf5", "r+")
        except:
            self.f = h5py.File("dailydata.hdf5", "w")
            self.f.create_dataset("weather_data", (400,9), maxshape=(2000000, 15))
            self.f.create_dataset("metadata",(2,), dtype='uint64') 
            self.f["metadata"][0] = 0
            self.f["metadata"][1] = self.get_cur_datetime_int()
        #f = h5py.File("dailydata", "r+")
        #b = f["weather_data"][:] load whole matrix, otherwise, just load last rows


    def add_data_point(self, date, site, geolocation, high, low, midday, rain_chance, rain_amt, cloud_cover):
        if self.f["metadata"][0] == self.f["weather_data"].shape[0]:
            self.f["weather_data"].resize(self.f["weather_data"].shape[0]*2, 0)

        self.f["weather_data"][self.f["metadata"][0],0] = date
        self.f["weather_data"][self.f["metadata"][0],1] = site
        self.f["weather_data"][self.f["metadata"][0],2] = geolocation
        self.f["weather_data"][self.f["metadata"][0],3] = high
        self.f["weather_data"][self.f["metadata"][0],4] = low
        self.f["weather_data"][self.f["metadata"][0],5] = midday
        self.f["weather_data"][self.f["metadata"][0],6] = rain_chance
        self.f["weather_data"][self.f["metadata"][0],7] = rain_amt
        self.f["weather_data"][self.f["metadata"][0],8] = cloud_cover
        
        self.f["metadata"][1] = self.get_cur_datetime_int()
        self.f["metadata"][0] += 1
   
    def add_data_matrix(self, matrix):
        assert(matrix.shape[1] == self.f["weather_data"].shape[1])
        if self.f["metadata"][0] >= self.f["weather_data"].shape[0]-matrix.shape[0]:
            self.f["weather_data"].resize(self.f["weather_data"].shape[0]*2, 0 )

        self.f["weather_data"][self.f["metadata"][0]:int(self.f["metadata"][0]+matrix.shape[0]),:] = matrix
        self.f["metadata"][0] += matrix.shape[0]
        self.f["metadata"][1] = self.get_cur_datetime_int()

class HourlyData(DailyData):
    """"
    See parent class.
    """
        

    def __init__(self):
        try:
            self.f = h5py.File("hourlydata.hdf5", "r+")
        except:
            self.f = h5py.File("hourlydata.hdf5", "w")
            self.dset = self.f.create_dataset("weather_data", (400,10), maxshape=(300000000, 15))
            self.metadata = self.f.create_dataset("metadata",(2,), dtype='uint64') 
            self.metadata[0] = 0
            self.metadata[1] = self.get_cur_datetime_int()    

    def add_data_point(self, date, hour, site, geolocation, temperature, humidity, wind_speed, rain_chance, rain_amt, cloud_cover):
        if self.f["metadata"][0] == self.f["weather_data"].shape[0]:
            self.f["weather_data"].resize(self.f["weather_data"].shape[0]*2, 0)

        self.f["weather_data"][self.f["metadata"][0],0] = date
        self.f["weather_data"][self.f["metadata"][0],1] = hour 
        self.f["weather_data"][self.f["metadata"][0],2] = site
        self.f["weather_data"][self.f["metadata"][0],3] = geolocation
        self.f["weather_data"][self.f["metadata"][0],4] = temperature
        self.f["weather_data"][self.f["metadata"][0],5] = humidity
        self.f["weather_data"][self.f["metadata"][0],6] = wind_speed
        self.f["weather_data"][self.f["metadata"][0],7] = rain_chance
        self.f["weather_data"][self.f["metadata"][0],8] = rain_amt
        self.f["weather_data"][self.f["metadata"][0],9] = cloud_cover
        
        self.f["metadata"][1] = self.get_cur_datetime_int()
        self.f["metadata"][0] += 1
   



#before creating database: unique timestamp for files already down and new files
#convert cities to PLZ
#to do: scrpt that converts PLZ to geolocation
#site indexing
#delete function
#change HourlyData
