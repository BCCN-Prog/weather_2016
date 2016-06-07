import sys
sys.path.append('../wrapper/')
import DataWrapH5py
import numpy as np
import bisect

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
        Takes dset: "daily" or "hourly", indicates dataset, param: string indicating the 
        category ("date", "high", "low"...), and an upper and lower bound for the values.
        Returns not a true slice (so save resources) but rather just the indices of the 
        original matrix fulfilling these criteria. If we go
        queryObject.daily[slice("daily", "high", 10, 15)], we get the rows of the original
        matrix where the (high) temperature lies between 10 and 15 degrees.
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

    def smart_slice(self, dset, params, lower, upper, return_matrix=True):
        '''
        Slices utilizing the presorted indices. By default, all categories are presorted.
        dset string "hourly" or "daily" specifies the dataset, params is the list of categories involved
        in the slicing, lower and upper the lists of lower and upper limits corresponding to params.
        By default returns a matrix sliced according to the above criteria. If return_matrix==False,
        returns just the indices to be sliced by. This can be used to increase performance if the matrix
        is very large.

        Nan handling: Nans always considered outside the bounds. This means that slicing wrt to a
        category whose corresponding column contains only nans will always return an empty array.
        '''
        assert(len(params) == len(lower) and len(lower) == len(upper))

        if dset == "daily":
            sorted_params = self.daily_params
        else:
            sorted_params = self.hourly_params

        dset = self.dset_dict[dset]
        
        param_order = np.sort([dset.categories_dict[params[i]] for i in range(len(params))])
        params = [dset.params_dict[param_order[i]] for i in range(len(param_order))]
        #here we order the param list according to the dset.params_dict in order to make things easier down the path

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
            s = dset.f["weather_data"][:,params_intersect_int[i]][dset.f[dset_names[i]]]
            if(np.isnan(np.sum(s))):
                s = s[:np.argmin(s)]
            #above line removes the nans if they exist in the array.

            lo_ind.append(bisect.bisect_left(s, lo_intersect[i]))
            hi_ind.append(bisect.bisect_right(s, hi_intersect[i]))
            #getting the slicing indices wrt to all parameters in params_intersect

        set_list = [set(dset.f[dset_names[i]][lo_ind[i]:hi_ind[i]]) for i in range(len(params_intersect))]
        #make a list of sets of indices. I hope this step is not too computation intensive, I do not know how
        #to do it differently

        ind = np.sort(list(set.intersection(*set_list)))
        #sorting in oder to better comply with h5py.


        if not ind.size:
            print("No matching entries.")
            return np.array([])

        if return_matrix == True:
            return dset.f["weather_data"][:][ind]
        else:
            return ind
        #is there a way to return a view here? If the matrix is large, passing by value takes
        #quite a bit of time here. Maybe issue a warning or something if the matrix is too large.
        #Can get problematic for hourly data.
