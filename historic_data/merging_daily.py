#This seeems (again 90% :)) to be:
#A previous version of recent_hist_merge_daily, with absolute paths. 

import numpy as np
import pandas as pd
import glob

def merge_hist_rec(hist,rec,interval_type,stationnumber):
    

    
    if interval_type == 'daily':
        if len(hist) != 0:
            #rename columns
            hist.columns = ['Stations_id', 'Date', 'Quality', 'Air_temperature', 'Steam_pressure', 'Cloudiness', 'Airpressure_stationsheight',      'relative_moisture', 'Air_speed', 'Air_temperature_max', 'Air_temperature_min', 'Soil_tem_min', 'Wind_speed_max', 'Rain', 'Rain_ind', 'Sunny_hours', 'Snow_height', 'eor']
            hist = hist.ix[:len(hist)-2] #cut last line - it's empty
            last_date = hist.Date[len(hist)-1] #extract last date of historical data
            if len(rec) == 0:
                complete_data = hist

        if len(rec) != 0:
            rec.columns = ['Stations_id', 'Date', 'Quality', 'Air_temperature', 'Steam_pressure', 'Cloudiness', 'Airpressure_stationsheight', 'relative_moisture', 'Air_speed', 'Air_temperature_max', 'Air_temperature_min', 'Soil_tem_min', 'Wind_speed_max', 'Rain', 'Rain_ind', 'Sunny_hours', 'Snow_height', 'eor']

            if len(hist) != 0:
                try:
                    rec_starting_idx = (rec.loc[rec['Date'] == last_date].index.tolist()[0])+1
                #if hist and rec do not overlap, we don't want to cut rec.
                except IndexError:
                    rec_starting_idx=1
                #Assign rec_cut: it's the original rec, but starting from index specified above.
                rec_cut = rec.ix[rec_starting_idx:]
                combined = pd.concat([hist,rec_cut],ignore_index=True)
                complete_data = combined
                
            else:
                complete_data = rec
        
        
        
    #note: this replaces existing files.   
    complete_data.to_csv('/home/pythonproject/Schreibtisch/testfiles/'+str(stationnumber)+'_'+interval_type+".csv")

#merge_hist_rec(hist,rec,'daily')
#loop station number
    #load file
    #if a,b =! []:
    #merge stuff   
    

#hist_paths = glob.glob("/home/pythonproject/Weather/ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/daily/kl/historical/*.txt")
#rec_paths = glob.glob("/home/pythonproject/Weather/ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/daily/kl/rec/*.txt")
#for station_number in range(2):
    
def get_hist_and_rec(station_number):
    #create "artificial" wildcard path for historical data. For every station imaginable. 
    histpath_temp = '/home/pythonproject/Weather/ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/daily/kl/historical/produkt_klima_Tageswerte_*'
    histpath_temp += str(station_number).zfill(5)+'.txt'
    #create "artificial" wildcard path for recent data. For the station we're looking at right now.       
    recpath_temp = '/home/pythonproject/Weather/ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/daily/kl/recent/produkt_klima_Tageswerte_*'
    recpath_temp += str(station_number).zfill(5)+'.txt'   

    #check if that path actually exists. Globglob checks if the histpath file actually exists.
    if len(glob.glob(histpath_temp)) != 0:
        #if file exists, save the path as a string to "histpath" variable.
        histpath = glob.glob(histpath_temp)[0]
        hist_ = pd.read_table(histpath, sep=";", low_memory=False)
        #is_hist = True

    else:
        #is_hist=False
        hist_ = []

        #check if recent data exists
    if len(glob.glob(recpath_temp)) != 0:
        recpath = glob.glob(recpath_temp)[0]
        rec_ = pd.read_table(recpath, sep=";", low_memory=False)
        #is_rec = True

    else:
        #is_rec = False
        rec_ = []
    return (hist_,rec_)



#import timeit
#start = timeit.default_timer()


for stationnumber in range(0,160):
    #print(stationnumber)
    (hist_out, rec_out) = get_hist_and_rec(stationnumber)
    #print(stationnumber)
    if (len(hist_out) != 0) or (len(rec_out) != 0):
        merge_hist_rec(hist_out,rec_out, 'daily', stationnumber)
    

#stop = timeit.default_timer()
#print (stop - start)
 
print("done")
