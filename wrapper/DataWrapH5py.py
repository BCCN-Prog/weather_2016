import h5py
import datetime

class DailyData:
    """"
    DOCUMENTATION DEPRECATED!!!
    get_cur_datetime_int gets the current date and time as an int in the format yearmonthdayhourminutesecond
    dset is a twodimensional arraylike object. It contains (unsortedly) all datapoints with attributes: date (integer
    YEARMONTHDAY), site (indexed), geolocation (encoded in one integer), high, low, midday, rain_chance, rain_amt,
    cloud_cover).
    metadata[0] is the pointer to the first unwritten row of dset, metadata[1] is the last date modified in
    YEARMONTHDAY.

    """
    def get_cur_datetime_int(self):
        now = datetime.datetime.now()
        return int(now.strftime('%Y%m%d%H%M%S'))

    def __init__(self):
        try:
            self.f = h5py.File("dailydata.hdf5", "r+")
        except:
            self.f = h5py.File("dailydata.hdf5", "w")
            self.f.create_dataset("weather_data", (400,9), maxshape=(1000000, 15))
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

class HourlyData:
    """"
    THIS CLASS COES NOT WORK YET!!!
    """
    def get_cur_datetime_int(self):
        now = datetime.datetime.now()
        return int(now.strftime('%Y%m%d%H%M%S'))

    def __init__(self):
        self.f = h5py.File("hourlydata.hdf5", "w")
        self.dset = self.f.create_dataset("weather_data", (400,10), maxshape=(10000000, 15))
        self.metadata = self.f.create_dataset("metadata",(2,), dtype='uint64') 
        self.metadata[0] = 0
        self.metadata[1] = self.get_cur_datetime_int()    

    def add_data_point(self, date, site, geolocation, high, low, midday, rain_chance, rain_amt, cloud_cover):
        if self.metadata[0] == self.dset.shape[0]:
            self.dset.resize(self.dset.shape[0]*2, 0 )
        
        self.dset[self.metadata[0],0] = date
        self.dset[self.metadata[0],1] = hour
        self.dset[self.metadata[0],2] = site
        self.dset[self.metadata[0],3] = geolocation
        self.dset[self.metadata[0],4] = temperature
        self.dset[self.metadata[0],5] = humidity
        self.dset[self.metadata[0],6] = wind_speed
        self.dset[self.metadata[0],7] = rain_chance
        self.dset[self.metadata[0],8] = rain_amt
        self.dset[self.metadata[0],9] = cloud_cover
        
        self.metadata[1] = self.get_cur_datetime_int()
        self.metadata[0] += 1
   
    def add_data_matrix(self, matrix):
        assert(matrix.shape[1] == self.dset.shape[1])
        if self.metadata[0] == self.dset.shape[0]:
            self.dset.resize(self.dset.shape[0]*2, 0 )
        
        self.dset[self.metadata[0]:int(self.metadata[0]+matrix.shape[0]),:] = matrix




#before creating database: unique timestamp for files already down and new files
#convert cities to PLZ
#to do: scrpt that converts PLZ to geolocation
#site indexing
#delete function
#change HourlyData
