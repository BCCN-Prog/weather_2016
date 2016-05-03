import h5py
import datetime

class DailyData:
    """"
    dset is a twodimensional arraylike object. It contains (unsortedly) all datapoints with attributes: date (integer
    YEARMONTHDAY), site (indexed), geolocation (encoded in one integer), high, low, midday, rain_chance, rain_amt,
    cloud_cover).
    metadata[0] is the pointer to the first unwritten row of dset, metadata[1] is the last date modified in
    YEARMONTHDAY.

    """
    def get_cur_datetime_int(self):
        now = datetime.datetime.now()
        year = str(now.year)
        month = now.month
        if len(str(month)) < 2:
            month = str(0)+str(month)
        else:
            month = str(month)
        day = now.day
        if len(str(day)) < 2:
            day = str(0)+str(day)
        else:
            day = str(day)
        hour = now.hour
        if len(str(hour)) < 2:
            hour = str(0)+str(hour)
        else:
            hour = str(hour)
        minute = now.minute
        if len(str(minute)) < 2:
            minute = str(0)+str(minute)
        else:
            minute = str(minute)
        second = now.second
        if len(str(second)) < 2:
            second = str(0)+str(second)
        else:
            second = str(second)
        return int(year+month+day+hour+minute+second)

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



x = DailyData()
print(x.dset[:])




#to do: scrpt that converts PLZ to geolocation
#site indexing
