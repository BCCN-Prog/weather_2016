import h5py
import datetime

class DailyData:
    """"
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
        self.f = h5py.File("dailydata.hdf5", "w")
        self.dset = self.f.create_dataset("weather_data", (400,9), maxshape=(1000000, 15))
        self.metadata = self.f.create_dataset("metadata",(2,), dtype='uint64') 
        self.metadata[0] = 0
        self.metadata[1] = self.get_cur_datetime_int()    

    def add_data_point(self, date, site, geolocation, high, low, midday, rain_chance, rain_amt, cloud_cover):
        self.dset[self.metadata[0],0] = date
        self.dset[self.metadata[0],1] = site
        self.dset[self.metadata[0],2] = geolocation
        self.dset[self.metadata[0],3] = high
        self.dset[self.metadata[0],4] = low
        self.dset[self.metadata[0],5] = midday
        self.dset[self.metadata[0],6] = rain_chance
        self.dset[self.metadata[0],7] = rain_amt
        self.dset[self.metadata[0],8] = cloud_cover
        
        self.metadata[1] = self.get_cur_datetime_int()
        self.metadata[0] += 1



x = DailyData()
print(x.dset[:])



#before creating database: unique timestamp for files already down and new files
#convert cities to PLZ
#to do: scrpt that converts PLZ to geolocation
#site indexing
#load function
