import sys
import os
sys.path.append('../wrapper/')
import DataWrapH5py
import numpy as np
import bisect
from functools import reduce

def block_print():
    '''
    Blocks all print output.
    '''
    sys.stdout = open(os.devnull, 'w')

def enable_print():
    '''
    Reenables print output.
    '''
    sys.stdout = sys.__stdout__

class QueryEngine:
    daily_params = ['date', 'site', 'station_id', 'high', 'low', 'temperature', 'rain_chance', 'rain_amt',
    'cloud_cover', 'city_ID'] #only for example
    hourly_params = ['date', 'hour', 'site', 'geolocation', 'temperature', 'humidity', 'wind_speed', 'rain_chance', \
                    'rain_amt', 'cloud_cover', 'city_ID']
    days_dict = {0:'Sunday', 1:'Monday', 2:'Tuesday', 3:'Wednesday', 4:'Thursday', 5:'Friday', 6:'Saturday'}
    days_backdict = {'Sunday':0, 'Monday':1, 'Tuesday':2, 'Wednesday':3, 'Thursday':4, 'Friday':5, 'Saturday':6}


    def __init__(self, make_new=False, loading_path="../historic_csv"):
        self.daily = DataWrapH5py.Daily_DataBase(make_new=make_new)
        self.hourly = DataWrapH5py.Hourly_DataBase(make_new=make_new)

        if make_new == True:
            self.daily.auto_csv(path=loading_path)
            self.hourly.auto_csv(path=loading_path)

            self.daily.create_presorted(self.daily_params)
            self.hourly.create_presorted(self.hourly_params)
    
        self.dset_dict = {"daily":self.daily, "hourly":self.hourly}

    def slice(self, dset, param, lower, upper):
        '''
        Function deprecated (nan handling), use smart_slice instead!
        
        Function takes a dataset and a parameter and extracts all data where the parameter lies between lower and upper
        
        dset: 'daily'/'hourly' --> so far only works for hourly (14.6.)
        param: <str>, category e.g. 'temp'
        lower: Lower bound of parameter to be relevant for slicing (int or float) --> e.g. 10°C 
        upper: 
        
        Problem (14.06.) with sorting
        '''
        dset = self.dset_dict[dset]
        param_int = dset.categories_dict[param]
        
        ind = dset.get_sort_indices(param_int)
        
        lo_ind = np.argmax(dset.f["weather_data"][:,param_int][ind] >= lower)
        hi_ind = np.argmin(dset.f["weather_data"][:,param_int][ind] <= upper) + 1
        
        #nan handling!

        #return dset.f["weather_data"][:][ind][lo_ind:hi_ind]

        #the above line shlould not be used because the returned matrix could
        #still be very large. Instead we are better of gathering all the 
        #lower/upper indices first, computing their intersection and only then take a slice
        
        

        return ind[lo_ind: hi_ind]

    def smart_slice(self, dset, params, lower, upper, return_matrix=True, sort=None):
        '''
        Slices utilizing the presorted indices. By default, all categories are presorted.
        dset: string "hourly" or "daily" specifies the dataset, 
        params: String or list of Strings for category/catebories involved in the slicing, 
        lower, upper: Lower und upper bounds for the categories specified in params. Must have same shape (number or list of umbers) and order as params. 
        
    Returns:
        By default returns a matrix sliced according to the above criteria. If return_matrix==False,
        returns just the indices to be sliced by. This can be used to increase performance if the matrix
        is very large.
        sort (String): order by this parameter

        Nan handling: Nans always considered outside the bounds. This means that slicing wrt to a
        category whose corresponding column contains only nans will always return an empty array.
        '''
        if(type(params) != list and type(lower) != list and type(upper) != list):
            assert(type(params) == str and isinstance(lower, (int, float, np.int64)) and isinstance(upper, (int, float,np.int64)))
            params = [params]
            lower = [lower]
            upper = [upper]
        else:
            assert(len(params) == len(lower) and len(lower) == len(upper))
        #Accomodation for non-list arguments, checking if they are of the same length if the are lists
        
        assert(sort == None or type(sort) == str or type(sort) == list)

        if dset == "daily":
            sorted_params = self.daily_params
        else:
            sorted_params = self.hourly_params

        dset = self.dset_dict[dset]
        
        p_unordered = [dset.categories_dict[params[i]] for i in range(len(params))]
        p_ordered = np.argsort(p_unordered)
        params = list(np.array(params)[p_ordered])
        lower = list(np.array(lower)[p_ordered])
        upper = list(np.array(upper)[p_ordered])
        #here we order the param and upper and lower lists according to the dset.params_dict
        #in order to allow for these to be passed to the function in any order.

        params_intersect = [p for p in params if p in sorted_params]
        params_intersect_int = [dset.categories_dict[params_intersect[i]] for i in range(len(params_intersect))]
        hi_lo_indices = [params.index(params_intersect[i]) for i in range(len(params_intersect))]
        hi_intersect = np.array(upper)[hi_lo_indices]
        lo_intersect = np.array(lower)[hi_lo_indices]
        #modify this to support aliases of params by having dictionary of string to strings
        
        dset_names = ["{}_indices".format(params_intersect[i]) for i in range(len(params_intersect))]
        
        lo_ind = []
        hi_ind = []
        for i in range(len(params_intersect)):
            s = dset.f["weather_data"][:][:,params_intersect_int[i]][dset.f[dset_names[i]]]
            if(np.isnan(np.sum(s))):
                s = s[:np.argmin(s)]
            #above line removes the nans if they exist in the array.

            lo_ind.append(bisect.bisect_left(s, lo_intersect[i]))
            hi_ind.append(bisect.bisect_right(s, hi_intersect[i]))
            #getting the slicing indices wrt to all parameters in params_intersect

        set_list = [dset.f[dset_names[i]][:][lo_ind[i]:hi_ind[i]] for i in range(len(params_intersect))]
        #make a list of array of indices. This is faster then to use sets, because although
        #set.intersection is a lot faster then np.intersect1d, converting arrays to sets takes
        #a lot more time.

        ind = np.sort(reduce(np.intersect1d, set_list))
        #sorting in oder to better comply with h5py.

        if not ind.size:
            print("No matching entries.")
            return np.array([])
        
        output = dset.f["weather_data"][:][ind]

        if sort:
            if type(sort) == str:
                s_ind = np.argsort(output[:][:,dset.categories_dict[sort]])
                output = output[:][s_ind]
            else:
                temp = output
                output = []
                s_ind = []
                for i in range(len(sort)):
                    indices = np.argsort(temp[:][:,dset.categories_dict[sort[i]]])
                    output.append(temp[:][indices])
                    s_ind.append(indices)
                output = tuple(output)
                s_ind = tuple(s_ind)
                
        if return_matrix == True:
            return output
        elif not sort:
            return ind
        else:
            print("return_matrix=False and sorting are not compatible.")
            return None
            

    def sort(self, param, data_matrix, dset=None):
        '''
        Sorts any matrix wrt to one column.

        param: int or str, designates either the index of the column to be sorted by,
            or (if str) the category of the respective dataset. In the latter case
            dset must be specified.
        data_matrix: numpy array or h5py dataset. The matrix to be sorted.
        dset: "daily" or "hourly", designates the datased to wich the data belongs.

        returns: numpy array that is data_matrix sorted wrt to the column designated by
            param.
        '''
        if type(param) == int:
            assert(param < data_matrix.shape[1])

            if dset:
                dset = self.dset_dict[dset]
                endpoint = np.minimum(np.int64(dset.f["metadata"][0]), data_matrix.shape[0])
            else:
                endpoint = data_matrix.shape[0]

            sort_ind = np.argsort(data_matrix[:][:endpoint][:,param])
            return data_matrix[:][sort_ind]

        else:
            assert(type(param) == str)
            assert(dset != None)
            dset = self.dset_dict[dset]
            assert(data_matrix.shape[1] == len(dset.params_dict))
            param = dset.categories_dict[param]
            endpoint = np.minimum(np.int64(dset.f["metadata"][0]), data_matrix.shape[0])

            sort_ind = np.argsort(data_matrix[:][:endpoint][:,param])
            return data_matrix[:][sort_ind]

    def n_days_in_month_of_year(self, month, year):
        '''
        Computes the number of days in a month of a year.

        month: int in (1,12), signifies the month.
        year: int, signifies the year.

        Returns: int, the number of days in specified month and year.
        '''
        assert(type(month) == int and month >= 1 and month <= 12)
        assert(type(year) == int and year > 0)

        return 28 + (month + int(month/8))%2 + 2%month + 2*int(1/month) + (1 - int(int(year%4)/4 + 0.75))

    def get_dates(self, lo_year, lo_month, lo_day, hi_year, hi_month, hi_day):
        '''
        Computes all existing dates in the given boundaries.

        lo_year: int, lower bound of years. (4 digits)
        lo_month: int, lower bound of months.
        lo_day: int, lower bound of days.
        hi_year: int, upper bound of years. (4 digits)
        hi_month: int, upper bound of months.
        hi_day: int, upper bound of days.

        Returns: list of ints, all dates within specified boundaries. (one int = YYYYMMDD) 
        '''
        assert(type(lo_year) == int and type(lo_month) == int and type(lo_day) == int and type(hi_year) == int \
                and type(hi_month) == int and type(hi_day) == int)

        dates = []
        for i in range(lo_year, hi_year+1):
            if i == lo_year: 
                l_month = lo_month
            else:
                l_month = 1
            if i == hi_year:
                h_month = hi_month
            else:
                h_month = 12
            for j in range(l_month, h_month+1):
                if i == lo_year and j == lo_month:
                    l_day = lo_day
                else:
                    l_day = 1
                if i == hi_year and j == hi_month:
                    end = np.minimum(hi_day, self.n_days_in_month_of_year(j,i))
                else:
                    end = self.n_days_in_month_of_year(j, i)
                    enable_print()
                    print(j,i)
                    block_print()
                days = list(range(l_day,end+1))
                                                                                                                                                                                                                                                        
                if j/10 < 1:
                    str_month = str(0)+str(j)
                else:
                    str_month = str(j)
                str_year = str(i)
                                                                                                                                                                                                                                                                                                                                                
                str_days = [str(0)+str(day) if day/10<1 else str(day) for day in days]
                                                                                                                                                                                                                                                                                                                                                                        
                dates += [int(str_year+str_month+str(str_days[i])) for i in range(len(days))]

        return dates

    def partition(self, dset, param, lo, hi, interval=0, slicing_params=None, lower_slice=None, upper_slice=None, sort=None):
        '''
        Partitions the dataset wrt. to a category, i.e. 
        q.partition("daily", "site", 0, 4) returns five matrices, the first of which contains
        all data that has 0 as its entry for station_id, the second 1 and so on. In other words,
        this is all scraping data (as historical has index 5), partitioned by site index.
        
        Instead of getting a matrix for every value, by setting interval to something other than
        0, it is possible partition the data with an interval of that size, i.e.
        q.partition("daily", "high", -10, 40, interval=10) gives us five matrices the first of which
        has all data where "high" is between -10 and 0 degrees, the second 0 and 10 and so on.

        It is also possible to slice the partitions additionally.
        q.partition("daily", "high", -10, 40, interval=10, 
        slicing_params=["date"], lower_slice=[19900101], upper_slice=[20000101])
        gives us again five matrices like in the previous example, but this time we only
        take datapoints where the date lies between 01.01.1990 and 01.01.2000.

        The matrices can also be returned sorted wrt. to one parameter.

        dset: "daily" or "hourly", specifies used dataset.
        param: str, parameter wrt. to wich we want to partition.
        lo: int or float, lower boundary for the values of the category param over which we partition.
        hi: int or float, upper boundary for the values of the category param over which we partition.
        interval: int or float, If 0, a partition is created for each value within (lo,hi). 
        If not 0, specifies the size of the intervals, into which (lo,hi) is divided. For each
            of those, a partition is created then.
        slicing_params: List of strings which represent the parameters by which each of the
            partitions is sliced.
        lower_slice: List of lower boundaries wrt. to which we slice using the corresponding
        enry of slicing_params.
        upper_slice: List of upper boundaries wrt. to which we slice using the corresponding
            enry of slicing_params.
        sort: None or str. If not None, we sort wrt. to the specified parameter.

        '''

        #add string/int support for slicing_params!!!
        assert(type(lo) == int)
        assert(type(hi) == int)
        assert(interval >= 0)
        dataset = self.dset_dict[dset]
        assert(type(param) == str or type(param) == int)
        if type(param) == int:
            param = dataset.params_dict[param]

        if not slicing_params:
            slicing_params = []
        if not upper_slice:
            upper_slice = []
        if not lower_slice:
            lower_slice = []
        
        if type(slicing_params) == list:
            assert(len(slicing_params) == len(upper_slice) and len(upper_slice) == len(lower_slice))
        else:
            slicing_params = [slicing_params]
            upper_slice = [upper_slice]
            lower_slice = [lower_slice]

        output = []
        slicing_params.append(param)

        if param == "date":
            lo_year = int(str(lo)[:4])
            lo_month = int(str(lo)[4:6])
            hi_year = int(str(hi)[:4])
            hi_month = int(str(hi)[4:6])
            if lo_year != hi_year or lo_month != hi_month:
                print('''
                        Partitioning over multiple years or months is not supported yet
                        (and not a great idea from a performance standpoint). If you really
                        need to, use n_days_in_month to compute the numbers of days in 
                        the months and use multiple function calls. Support for this feature
                        may be implemented in the future. An empty list will be returned now.
                        ''' )
                return []

        block_print()
        #block print in order to evade "no matching entries" warnings.
        iter_ind = range(lo, hi+1)
        if interval == 0:
            for i in iter_ind:
                upper_slice.append(i)
                lower_slice.append(i)
                output.append(self.smart_slice(dset, slicing_params, lower_slice, upper_slice, sort=sort))
                del(upper_slice[-1])
                del(lower_slice[-1])
        else:
            for i in iter_ind[:-1:interval]:
                upper_slice.append(np.minimum(i+interval, hi))
                if i != iter_ind[0]:
                    lower_slice.append(i+0.0001)
                else:
                    lower_slice.append(i)
                output.append(self.smart_slice(dset, slicing_params, lower_slice, upper_slice, sort=sort))                    
                del(lower_slice[-1])
                del(upper_slice[-1])

        enable_print()

        return output
        
    def get_val_range(self, dset, param, data_matrix):
        '''
        Computes the range of values in one category of a dataset-shaped matrix.

        dset: "daily" or "hourly", specifies dataset dat_matrix was derived from.
        param: int or str, specifies category for which to get the range.
        data_matrix: numpy array, the data matrix for which the range is computed.

        Returns: Tuple, first value being the lowest value encountered in specified category,
            second the highest.
        '''
        assert(type(param) == int or type(param) == str)
        dset = self.dset_dict[dset]
        if type(param) == str:
            param = dset.categories_dict[param]
        assert(data_matrix.shape[1] == len(dset.params_dict))
        assert(param < data_matrix.shape[1])

        return np.amin(data_matrix[:][:,param]), np.amax(data_matrix[:][:,param])
 
        pass

    def get_dataset(self, dset):
        '''
        Gets the specified dataset, discarding unwritten rows.

        dset: "daily" or "hourly", specifies the dataset to be returned.

        retuns: All written rows of the specified dataset, entry "weather_data".
        '''
        dset = self.dset_dict[dset]
        return dset.f["weather_data"][:][:dset.f["metadata"][0]]
        

    def get_category(self, dset, data, category):
        '''
        Gets the column for the specified category from the specified matrix with
        shape[1] the same as the dataset's, discarding yet unwritten rows.

        dset: "daily" or "hourly", specifies database data is derived from.
        data: numpy array, the data from which the category is selected. Must have
            the same number of columns as the dataset as specified by dset.
        category: int or str, specifies the category or just column number
            that is to be extracted.

        returns: One column of data, as specified by category.
        '''
        dset = self.dset_dict[dset]
        assert(type(category) == str or type(category) == int)
        if type(category) == str:
            category = dset.categories_dict[category]
        assert(data.shape[1] == len(dset.params_dict))
        assert(category < data.shape[1])

        endpoint = np.minimum(np.int64(dset.f["metadata"][0]), data.shape[0])

        return data[:][:endpoint][:,category]     

    def compute_weekday(self, date, return_int=False):
        '''
        Implements the doomsday-algorithm to compute the weekday of any given date.

        date: int of the format yearmonthday.
        return_int: boolean. If true, instead of a string, the function will return an int,
            where 0 corresponds to Sunday, 1 to Monday and so on.

        Returns: Str or int, the weekday of specified day.
        '''
        year = int(str(date)[:4])
        month = int(str(date)[4:6])
        day = int(str(date)[6:8])
    
        year_ones = int(str(year)[2:4])
        year_hundreds = int(str(year)[:2])
    
        n_1 = int(year_ones/12)
        n_2 = year_ones - n_1*12
        n_3 = int(n_2/4)
        if year_hundreds == 18:
            anchor = 5
        if year_hundreds == 19:
            anchor = 3
        if year_hundreds == 20:
            anchor = 2
        n_5 = n_1 + n_2 + n_3 + anchor
    
        doomsday = n_5 - (n_5%7)*7
    
        days_in_month = [self.n_days_in_month_of_year(i, year) for i in range(1,13)]
    
        if month == 12 and day == 12:
            if not return_int:
                return self.days_dict[doomsday]
            else:
                return doomsday
        elif month == 12 and day >12:
            count = 19
            while abs(day-count) > 7:
                count += 7
            if not return_int:
                return self.days_dict[(day-count + doomsday)%7]
            else:
                return (day-count + doomsday)%7
        else:
            c_day = 12
            c_month = 12
            while not (c_month == month and abs(day-c_day)<7):
                if c_day <= 7:
                    c_month -= 1
                    c_day = days_in_month[c_month-1] + c_day - 7
                else:
                    c_day -= 7
            if not return_int:
                return self.days_dict[(doomsday + (day - c_day) + 7)%7]
            else:
                return (doomsday + (day - c_day) + 7)%7
    
    def compute_weekday_vectorized(self, date, return_ints=False):
        '''
        Vectorized version of compute_weekday. For dosumentation, see there.
        '''
        def f():
            return np.vectorize(self.compute_weekday)
        return f()(date, return_ints)

    def extract_weekdays(self, dset, days, data_matrix, lo_date=None, hi_date=None):
        '''
        Extracts datapoints corresponding to a certain weekday or a list of such.

        dset: "daily" or "hourly", sgnifies dataset.
        days: str or list of str containing the day or the days for which the datapoints will
            be extracted.
        data_matrix: numpy array, the data on which the function will be performend.
        lo_date: int, lower bound for the regarded dates.
        hi_date: int, upper bound for the reagrded dates.

        Returns: numpy array containing only datapoints for which the date falls on specified
            weekdays.

        TODO: Implement lo_date, hi_date. Also: Why so slow?
        '''
        assert(type(days) == list or type(days) == str)
        if lo_date or hi_date:
            assert(type(lo_date) == int and type(hi_date) == int)

        dset = self.dset_dict[dset]

        if type(days) == str:
            days = [days]
        days_int = [self.days_backdict[i] for i in days]

        weekdays = self.compute_weekday_vectorized(data_matrix[:][:,0], return_ints=True)

        inds = np.where(reduce(np.logical_or, [weekdays==i for i in days_int]))
        return data_matrix[:][inds]



