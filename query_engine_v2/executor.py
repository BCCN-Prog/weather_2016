
import sys
sys.path.append('../visualization')
sys.path.append('../query_engine_v2')
import map_functions as mf
import QueryEngine as qe
import name_to_id as ni
import matplotlib.pyplot as plt
import numpy as np
import linear_plotter as lp



class Executor:


    def __init__(self):
        
        '''
        The xy_to_georg files translate our parameter names to the one that the database uses.
        '''

        self.description = 'Dummy description'
        self.HistoricalDaily_to_georg={'Maximum Temperature':'high', 'Minimum Temperature':'low', 'Average Temperature':'temperature','Rain            Chance':'rain_chance', 'Rain Amount':'rain_amt', 'Cloud Cover':'cloud_cover'}
        self.HistoricalHourly_to_georg={'Temperature':'temperature', 'Moisture':'humidity', 'Cloud Cover':'cloud_cover', 'Rainfall':'rain_chance', 'Rain Amount':'rain_amt'}#, 'Air Pressure reduced', 'Air Pressure Station', 'Windspeed'


        self.RecentDaily_to_georg={'Maximum Temperature':'high', 'Minimum Temperature':'low', 'Rain chance':'rain_chance', 'Rain Amount':'rain_amt','Air Pressure':'pressure', 'Cloud Cover':'cloud_cover'}
        self.RecentHourly_to_georg={'Temperature':'temp', 'Humidity':'humidity', 'Air Pressure':'pressure', 'Windspeed':'wind_speed', 'Rain Chance':'rain_chance', 'Rain Amount':'rain_amt', 'Cloud Cover':'cloud_cover'}
        self.nstations = 20000
        self.parameterrange = [-999,999]

        




    def get_data(self,hourly_daily, recent_hist, parameter, station, StartingDateTime, EndingDateTime, StartingTime, EndingTime):
        '''
        This is the main function here. It is called by GUILogic 
        and is supposed to call the smart_slice, get_data, and visualization
        functions lying aroung in the visualization folder.

        The main distintions are:
        a) All stations selected?
            Yes -> We want to plot a map
            No -> We want to plot a diagram
        b) Historical or Scraped ("recent")?
        c) Hourly or daily?

        So that leaves us with a total of 8 different cases. 

        In each case, we usually call smart_slice with the according parameters, then get_data, and then do some lines which belong to plotting. 
        As you will probably see, in a lot of cases the smart_slice function produces an error or an empty output array. 

        The two cases that are currently working are "All - Historical - Daily (map)" and "Not_All - Historical - Daily (diagram)".
        '''

        q = qe.QueryEngine("daily_database.hdf5", "hourly_database.hdf5")

        if (station == "All"):
        ###Plot a Map!
            #Historical
            if (recent_hist == "historical"):

                
                if (hourly_daily == "hourly"):  
                    '''
                    Case 1: All, Historical, Hourly
                    This is working

                    As we said, we call smart_slice first, then get_data, and then 4 lines of plotting.
                    '''
                    
                    s = q.smart_slice(hourly_daily, ['station_id', self.HistoricalHourly_to_georg[parameter]], ['date','hour', 'station_id'], [int(StartingDateTime),int(StartingTime),0], [int(EndingDateTime), int(EndingTime), self.nstations])
                    out = q.get_data(hourly_daily, s, ['station_id', self.HistoricalHourly_to_georg[parameter]])

                elif (hourly_daily == "daily"):  
                    '''
                    Case 2: All, Historical, Daily
                    This is working
                    '''  
                    s = q.smart_slice(hourly_daily, ['station_id', self.HistoricalDaily_to_georg[parameter]], ['date','station_id','site'], [int(StartingDateTime),0,6], [int(EndingDateTime),self.nstations,6])

                    out = q.get_data(hourly_daily, s, ['station_id', self.HistoricalDaily_to_georg[parameter]])
                ###PLOT###

                #Get geolocations, stuff, call plotting function
                ids, vals = out[:,0], out[:,1]
                
#                locs = mf.id_to_geo_location(ids, hourly_daily, source='historic')
                locs = mf.id_to_geo_location(ids, source='historic')
                #prefer hexagon map?
                #figure = mf.hexagon_map(locs[:,90], locs[:,1], vals , hex_grid_size=(50,50))
                ###We call the "interpolated_color_map" from denis' map_function.py (imported in this file). 
                ###It gives us a figure that we then can show. The self.parameterrange was supposed
                ### to help us do some other stuff, you can ignore it. 
#                figure, self.parameterrange = mf.interpolated_color_map(locs[:,0], locs[:,1], vals, parameter, interp='linear', return_figure=True)
                                
                idx = np.invert(np.isnan(locs[:,0]))
                vals = vals[idx]
                locs = locs[idx]                       
                
                figure = mf.interpolated_color_map(locs[:,0], locs[:,1], vals, parameter, interp='linear', return_figure=True)
                plt.show()





            #Scraped ("recent")
            elif (recent_hist == "recent"):
                if (hourly_daily == "hourly"):    
                    '''
                    Case 3: All, Recent, Hourly
                    NOT working
                    '''
                    s = q.smart_slice(hourly_daily, ['city_id', self.RecentHourly_to_georg[parameter]], ['date', 'station_id','site'], [int(StartingDateTime),0,3], [int(EndingDateTime),self.nstations,3])
                    
                    out = q.get_data(hourly_daily, s, ['station_id', self.RecentHourly_to_georg[parameter]])


                elif (hourly_daily == "daily"):  
                    '''
                    Case 4: All, Recent, Daily
                    NOT working
                    Getting this part working would be especially nice, because then we could plot comparison maps of scraped vs hist data.
                    '''  
                    s = q.smart_slice(hourly_daily, ['city_ID', self.RecentDaily_to_georg[parameter]], ['date', 'site'], [int(StartingDateTime),2], [int(EndingDateTime),2])
                    out = q.get_data(hourly_daily, s, ['station_id', self.RecentDaily_to_georg[parameter]])

                #plot again
                ids, vals = out[:,0], out[:,1]
                locs = mf.id_to_geo_location(ids, hourly_daily, source='historic')

                #mf.hexagon_map(locs[:,0], locs[:,1], vals , hex_grid_size=(50,50))
                mf.interpolated_color_map(locs[:,0], locs[:,1], vals, interp='linear')

                




        elif (station != "All"):
        ###Plot a graph!


            #historical
            if (recent_hist =="historical"):
                if (hourly_daily == "hourly"):   
                    '''
                    Case 5: One Station, Historical, Hourly
                    Working!
                    ''' 
#                    t = q.smart_slice(hourly_daily, ['station_id', self.HistoricalHourly_to_georg[parameter]], ['date', 'station_id'], [int(StartingDateTime), ni.name_to_id(station)], [int(EndingDateTime),ni.name_to_id(station)], sort='date')
#                    t = q.smart_slice(hourly_daily, ['date', self.HistoricalHourly_to_georg[parameter]], ['date', 'station_id'], [int(StartingDateTime), ni.name_to_id(station)], [int(EndingDateTime),ni.name_to_id(station)], sort='date')
                    t = q.smart_slice(hourly_daily, ['date', 'hour', self.HistoricalHourly_to_georg[parameter]], ['date', 'station_id'], [int(StartingDateTime), ni.name_to_id(station)], [int(EndingDateTime),ni.name_to_id(station)], sort='date')

#                    out = q.get_data(hourly_daily, t, ['station_id', self.HistoricalHourly_to_georg[parameter]])
                    out = q.get_data(hourly_daily, t, ['date', 'hour', self.HistoricalHourly_to_georg[parameter]])

                    dates = out[:,0].astype(int).astype(str)
                    hours = out[:,1].astype(int).astype(str)
                    hours = np.core.defchararray.zfill(hours, 2)
                    date_hours = np.core.defchararray.add(dates, hours).astype(float)

                    out_new = np.vstack([date_hours, out[:,2]]).T
                    lp.plot_over_time(out_new,hourly_daily,self.HistoricalHourly_to_georg[parameter])


                elif (hourly_daily == "daily"):    
                    '''
                    Case 6: One Station, Historical, Daily
                    Working
                    '''

                    t = q.smart_slice(hourly_daily, ['date', self.HistoricalDaily_to_georg[parameter]], ['date', 'station_id'], [int(StartingDateTime), ni.name_to_id(station)], [int(EndingDateTime),ni.name_to_id(station)], sort='date')

                    out = q.get_data(hourly_daily, t, ['date', self.HistoricalDaily_to_georg[parameter]])
                    print(out)
                    lp.plot_over_time(out,hourly_daily,self.HistoricalDaily_to_georg[parameter])

            #recent 
            elif (recent_hist == "recent"):
                if (hourly_daily == "hourly"):  
                    '''
                    Case 7: One Station, Recent, Hourly
                    NOT working
                    
                    For the "Not_all - recent - hourly/daily" cases (7&8), visualization is not implemented. 
                    Although it might work to just copy the lp.plot_over_time from above. Who knows...
                    '''  
                    t = q.smart_slice(hourly_daily, ['station_id', self.HistoricalHourly_to_georg[parameter]], ['date', 'station_id'], [int(StartingDateTime), ni.name_to_id(station)], [int(EndingDateTime),ni.name_to_id(station)], sort='date')

                    out = q.get_data(hourly_daily, t, ['station_id', self.HistoricalHourly_to_georg[parameter]])
                    #print(out)

                elif (hourly_daily == "daily"):    
                    '''
                    Case 8: One Station, Historical, Daily
                    NOT working
                    '''
                    t = q.smart_slice(hourly_daily, ['date', self.HistoricalDaily_to_georg[parameter]], ['date', 'station_id'], [int(StartingDateTime), ni.name_to_id(station)], [int(EndingDateTime),ni.name_to_id(station)], sort='date')

                    out = q.get_data(hourly_daily, t, ['date', self.HistoricalDaily_to_georg[parameter]])
                    plt.plot(out[:,1])
                    plt.show()

