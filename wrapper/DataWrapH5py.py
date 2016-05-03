import h5py

class DailyData:
    """"
    f corresponds to the hdf5 file on disk.
    dset is our actual data set; the format works like numpy arrays; it is three-dimensional. x-axis corresponds to the
    date, y-axis correspnds to indexed site (if applicable), z-axis corresponds to [date(redundant, to avoid computation),
    geoloc(converted), high, low, midday, rain_chance, rain_amt, pressure, cloud_cover].
    datePointer stores the index on the x-axis of the first unwritten date.

    """
    def __init__(self):
        self.f = h5py.File("dailydata.hdf5", "w")
        self.dset = self.f.create_dataset("resizable", (400,8), maxshape=(1000000, 15))

    def add_data_point(self, date, site, geolocation, high, low, midday, rain_chance, rain_amt, cloud_cover):
        pass 

x = DailyData()
print(x.dset[:])




#to do: scrpt that converts PLZ to geolocation
#site indexing
