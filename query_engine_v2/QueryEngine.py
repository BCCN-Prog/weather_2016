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
    daily_params = ['date', 'site', 'station_id', 'high', 'low', 'midday', 'rain_chance', 'rain_amt',
    'cloud_cover', 'city_ID'] #only for example
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
    
        self.dset_dict = {"daily":self.daily, "hourly":self.hourly}

    def slice(self, dset, param, lower, upper):
        '''
        Function deprecated (nan handling), use smart_slice instead!
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
        dset string "hourly" or "daily" specifies the dataset, params is the list of categories involved
        in the slicing, lower and upper the lists of lower and upper limits corresponding to params.
        Alternitively, params can be just a string, lower and upper just numbers.
        By default returns a matrix sliced according to the above criteria. If return_matrix==False,
        returns just the indices to be sliced by. This can be used to increase performance if the matrix
        is very large.

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

    def partition(self, dset, param, lo, hi, interval=0, slicing_params=[], lower_slice=[], upper_slice=[], sort=None):
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
        slicing_params: List of parameters (string-support is coming) by which each of the
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
        
        output = []
        slicing_params.append(param)
        if param == "date":
            print("Warning: Since not all integers correspond to a date, partitioning across them \
                    can produce many empty arrays in the output! To be safe, make your boundaries \
                    such that you know that within them, all integers correspond to a date.")

        block_print()
        #block print in order to evade "no matching entries" warnings.
        if interval == 0:
            for i in range(lo, hi+1):
                upper_slice.append(i)
                lower_slice.append(i)
                output.append(self.smart_slice(dset, slicing_params, lower_slice, upper_slice, sort=sort))
                del(upper_slice[-1])
                del(lower_slice[-1])
        else:
            for i in range(lo, hi, interval):
                lower_slice.append(i+0.0001)
                upper_slice.append(np.minimum(i+interval, hi))
                if i != lo:
                    #output.append(self.smart_slice(dset, param, i+0.0001, np.minimum(i+interval, hi), sort=sort))
                    output.append(self.smart_slice(dset, slicing_params, lower_slice, upper_slice, sort=sort))                    
                else:
                    #output.append(self.smart_slice(dset, param, i, i+interval, sort=sort))
                    output.append(self.smart_slice(dset, slicing_params, lower_slice, upper_slice, sort=sort))
                del(lower_slice[-1])
                del(upper_slice[-1])

        enable_print()

        return output
        
    def get_val_range(self):
        '''
        Gets the range of values in one category given that the values of a list of categories
        lie within specified boundaries.
        '''
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

    def get_weekday(self):
        '''
        Returns the weekday for specified date.
        '''
        pass
