# This script is taking in all the parameter files of hourly data and outputing combined hourly data for every station.
import numpy as np
import pandas as pd
import timeit

start = timeit.default_timer()


for stationid in range(0,500):
    try:
        air = pd.read_table("./hourly_data/air_temperature_"+str(stationid)+".csv", sep=",",index_col=0)
        air = air.set_index('Date')
        air = air[['Air_temperature','Moisture']]
        #print("found air")
    except OSError:
        air = pd.DataFrame(np.nan, index=[], columns=['Air_temperature','Moisture'])
    try:
        cloudiness = pd.read_table("./hourly_data/cloudiness_"+str(stationid)+".csv", sep=",",index_col=0)
        cloudiness = cloudiness.set_index('Date')
        cloudiness = cloudiness[['Cloudiness']]
        #print("found clouds")
    except OSError:
        cloudiness = pd.DataFrame(np.nan, index=[], columns=['Cloudiness'])
    try:
        precip = pd.read_table("./hourly_data/precipitation_"+str(stationid)+".csv", sep=",",index_col=0)
        precip = precip.set_index('Date')
        precip = precip[['Rain_fall_ind','Rain_height']]
        #print("found prep")
    except OSError:
        precip = pd.DataFrame(np.nan, index=[], columns=['Rain_fall_ind','Rain_height'])
    try:
        pressure = pd.read_table("./hourly_data/pressure_"+str(stationid)+".csv", sep=",",index_col=0)
        pressure = pressure.set_index('Date')
        pressure = pressure[['Airpressure_reduced','Airpressure_station']]
        #print("found pressure")
    except OSError:
        pressure = pd.DataFrame(np.nan, index=[], columns=['Airpressure_reduced','Airpressure_station'])
    #try:
    #    solar = pd.read_table("./hourly_data/solar_"+str(i)+".csv", sep=",",index_col=0)
    #    solar = solar.set_index('Date')
    #    solar = solar[['Stations_id',]]
    #    print("found solar")
    #except OSError:
    #    solar = pd.DataFrame(np.nan, index=[], columns=[])
    #try:
    #    sun = pd.read_table("./hourly_data/sun_"+str(i)+".csv", sep=",",index_col=0)
    #    sun = sun.set_index('Date')
    #    sun = sun[['Stations_id',]]
    #    print("found sun")
    #except OSError:
    #    sun = pd.DataFrame(np.nan, index=[], columns=[])
    try:
        wind = pd.read_table("./hourly_data/wind_"+str(stationid)+".csv", sep=",",index_col=0)
        wind = wind.set_index('Date')
        wind = wind[['Windspeed']]
        #print("found wind")
    except OSError:
        wind = pd.DataFrame(np.nan, index=[], columns=['Windspeed'])
    #cols_to_use = wind.columns - air.columns


    cols_to_use = cloudiness.columns.difference(air.columns)
    merge = air.join(cloudiness[cols_to_use],how='outer')

    cols_to_use = precip.columns.difference(merge.columns)
    merge = merge.join(precip[cols_to_use],how='outer')

    cols_to_use = pressure.columns.difference(merge.columns)
    merge = merge.join(pressure[cols_to_use],how='outer')

    cols_to_use = wind.columns.difference(merge.columns)
    merge = merge.join(wind[cols_to_use],how='outer')
    
    if not (merge.empty):
        merge.to_csv("./hourly_data_clean/"+str(stationid)+"_hourly.csv")
print("done")


stop = timeit.default_timer()

print (stop - start) 
