#This script takes in recent and historical data from the deep folders we downloaded. It returns merged versions for each parameter in a separate parameter file. 

import numpy as np
import pandas as pd
import glob
import timeit  
#STATIONS_ID; MESS_DATUM; QUALITAETS_NIVEAU; STRUKTUR_VERSION; LUFTTEMPERATUR;REL_FEUCHTE;eor
foldernames = ["air_temperature","cloudiness","precipitation","pressure","solar","sun","wind"] #<- problem^^
parameter_columnnames=[['Stations_id', 'Date', 'Quality', 'Structure_version', 'Air_temperature', 'Moisture', 'eor'],
                      ['Stations_id', 'Date', 'Quality', 'Cloudiness','eor'],
                      ['Stations_id', 'Date', 'Quality', 'Rain_fall_ind', 'Rain_height','Type_of_rain' ,'eor'],
                      ['Stations_id', 'Date', 'Quality', 'Airpressure_reduced', 'Airpressure_station', 'eor'],
                      ['Stations_id', 'Date', 'Quality', 'Sun_duration', 'DIFFUS_HIMMEL_KW_J', 'GLOBAL_KW_J','ATMOSPHAERE_LW_J','SONNENZENIT','MESS_DATUM_WOZ' ,'eor'],
                      ['Stations_id', 'Date', 'Quality', 'Structure_version', 'STUNDENSUMME_SONNENSCHEIN', 'eor'],
                      ['Stations_id', 'Date', 'Quality', 'Structure_version', 'WINDGESCHWINDIGKEIT','WINDRICHTUNG' ,'eor']]
name_param_dict = {} #value must be missing or too much in the line of wind!
for i in range(len(foldernames)):
    name_param_dict[foldernames[i]] = parameter_columnnames[i]

#hourly_filenames = [produkt_temp_Terminwerte_18930101_20151231_03987,
#                    produkt_synop_Terminwerte_19490101_19500630_01260
#                   produkt_synop_Terminwerte_19950901_19951023_03538
#                   produkt_synop_Terminwerte_19490101_19500630_01260
#                   solar: produkt_strahlung_Stundenwerte_19451231_20160331_03987
#                   produkt_sonne_Terminwerte_18900101_20151231_01580
#                   produkt_wind_Terminwerte_18930101_20151231_03987]

#NIEDERSCHLAG_GEFALLEN_IND;NIEDERSCHLAGSHOEHE;NIEDERSCHLAGS
#STATIONS_ID; MESS_DATUM; QUALITAETS_NIVEAU; LUFTDRUCK_REDUZIERT;LUFTDRUCK_STATIONSHOEHE;eor
#STATIONS_ID; MESS_DATUM; QUALITAETS_NIVEAU; ERDBODENTEMPERATUR;MESS_TIEFE; ERDBODENTEMPERATUR;MESS_TIEFE; ERDBODENTEMPERATUR;MESS_TIEFE; ERDBODENTEMPERATUR;MESS_TIEFE; ERDBODENTEMPERATUR;MESS_TIEFE;eor
#STATIONS_ID; MESS_DATUM; QUALITAETS_NIVEAU; SONNENSCHEINDAUER;DIFFUS_HIMMEL_KW_J;GLOBAL_KW_J;ATMOSPHAERE_LW_J;SONNENZENIT;MESS_DATUM_WOZ;eor
#STATIONS_ID; MESS_DATUM; QUALITAETS_NIVEAU; STRUKTUR_VERSION; STUNDENSUMME_SONNENSCHEIN;eor
#STATIONS_ID; MESS_DATUM; QUALITAETS_NIVEAU; STRUKTUR_VERSION; WINDGESCHWINDIGKEIT;WINDRICHTUNG;eor

def get_hist_and_rec_hourly(station_number, parametertype):
    if parametertype != "solar":
        #create "artificial" wildcard path for historical data. For every station imaginable. 
        histpath_temp = './ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/hourly/'
        histpath_temp += parametertype+'/historical/produkt*'
        histpath_temp += str(station_number).zfill(5)+'.txt'
        #create "artificial" wildcard path for recent data. For the station we're looking at right now.       
        recpath_temp = './ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/hourly/'
        recpath_temp += parametertype+'/recent/produkt*'
        recpath_temp += str(station_number).zfill(5)+'.txt'   
        
        
    #"solar" data are not divided into hist an recent - we need to introduce an exception for that case
    elif parametertype == 'solar':
        histpath_temp = './ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/hourly/solar/produkt*'
        histpath_temp += str(station_number).zfill(5)+'.txt'
        recpath_temp = ''
    
    
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

#(a,b) = get_hist_and_rec_hourly(3987,'solar')
#print(b)
        
def merge_hist_rec_hourly(hist,rec,stationnumber, parametertype):    
    if len(hist) != 0:
        hist.columns = name_param_dict[parametertype]
        hist = hist.ix[:len(hist)-2] #cut last line - it's empty
        last_date = hist.Date[len(hist)-1] #extract last date of historical data
        if len(rec) == 0:
            complete_data = hist

    if len(rec) != 0:
        rec.columns = name_param_dict[parametertype]

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


    complete_data = complete_data.replace(-999, np.nan, regex=True)
    #note: this replaces existing files.   
    complete_data.to_csv('./hourly_data/'+parametertype+"_"+str(stationnumber)+".csv")

    
start = timeit.default_timer()

for params in foldernames:
    for stationnumber in range(0,16000):
        (hist_out, rec_out) = get_hist_and_rec_hourly(stationnumber,params)
        if (len(hist_out) != 0) or (len(rec_out) != 0):
            merge_hist_rec_hourly(hist_out,rec_out, stationnumber, params)

stop = timeit.default_timer()

print (stop - start) 
print("done")

