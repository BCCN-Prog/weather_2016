
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
        self.description = 'Dummy description'
        self.HistoricalDaily_to_georg={'Maximum Temperature':'high', 'Minimum Temperature':'low', 'Average Temperature':'temperature','Rain            Chance':'rain_chance', 'Rain Amount':'rain_amt', 'Cloud Cover':'cloud_cover'}
        self.HistoricalHourly_to_georg={'Temperature':'temperature', 'Moisture':'humidity', 'Cloud Cover':'cloud_cover', 'Rainfall':'rain_chance', 'Rain Amount':'rain_amt'}#, 'Air Pressure reduced', 'Air Pressure Station', 'Windspeed'


        self.RecentDaily_to_georg={'Maximum Temperature':'high', 'Minimum Temperature':'low', 'Rain chance':'rain_chance', 'Rain Amount':'rain_amt','Air Pressure':'pressure', 'Cloud Cover':'cloud_cover'}
        self.RecentHourly_to_georg={'Temperature':'temp', 'Humidity':'humidity', 'Air Pressure':'pressure', 'Windspeed':'wind_speed', 'Rain Chance':'rain_chance', 'Rain Amount':'rain_amt', 'Cloud Cover':'cloud_cover'}




    def get_data(self,hourly_daily, recent_hist, parameter, station, StartingDateTime, EndingDateTime, StartingTime, EndingTime):
        q = qe.QueryEngine("./daily_database.hdf5", "./hourly_database.hdf5")

        if (station == "All"):
        ###Plot a Map!

            #Historical
            if (recent_hist == "historical"):
                if (hourly_daily == "hourly"):  
                     
                    s = q.smart_slice(hourly_daily, ['station_id', self.HistoricalHourly_to_georg[parameter]], ['date','hour'], [int(StartingDateTime),int(StartingTime)], [int(EndingDateTime), int(EndingTime)])

                    out = q.get_data(hourly_daily, s, ['station_id', self.HistoricalHourly_to_georg[parameter]])

                elif (hourly_daily == "daily"):   
                    print(hourly_daily, recent_hist, parameter, station, StartingDateTime, EndingDateTime, StartingTime, EndingTime) 
                    s = q.smart_slice(hourly_daily, ['station_id', self.HistoricalDaily_to_georg[parameter]], 'date', int(StartingDateTime), int(EndingDateTime))

                    out = q.get_data(hourly_daily, s, ['station_id', self.HistoricalDaily_to_georg[parameter]])
                ids, vals = out[:,0], out[:,1]
                locs = mf.id_to_geo_location(ids, source='historic')
                print(locs[:,0], locs[:,1], vals)
                #mf.hexagon_map(locs[:,90], locs[:,1], vals , hex_grid_size=(50,50))
                mf.interpolated_color_map(locs[:,0], locs[:,1], vals, parameter, interp='linear')
                

            #Scraped ("recent")
            elif (recent_hist == "recent"):
                if (hourly_daily == "hourly"):    

                    s = q.smart_slice(hourly_daily, ['station_id', self.RecentHourly_to_georg[parameter]], ['date', 'site'], [int(StartingDateTime),0], [int(EndingDateTime),0])
                    
                    out = q.get_data(hourly_daily, s, ['station_id', self.RecentHourly_to_georg[parameter]])


                elif (hourly_daily == "daily"):    
                    print(q.daily.f["weather_data"][:])
                    s = q.smart_slice(hourly_daily, ['station_id', self.RecentDaily_to_georg[parameter]], ['date', 'site'], [int(StartingDateTime),5], [int(EndingDateTime),5])
                    print(s)
                    out = q.get_data(hourly_daily, s, ['station_id', self.RecentDaily_to_georg[parameter]])

                ids, vals = out[:,0], out[:,1]
                locs = mf.id_to_geo_location(ids, source='historic')

                #mf.hexagon_map(locs[:,0], locs[:,1], vals , hex_grid_size=(50,50))
                mf.interpolated_color_map(locs[:,0], locs[:,1], vals, interp='linear')

                




        elif (station != "All"):
        ###Plot a graph!


            #historical
            if (recent_hist =="historical"):
                if (hourly_daily == "hourly"):    
                    #print(EndingDateTime, StartingDateTime)
                    t = q.smart_slice(hourly_daily, ['station_id', self.HistoricalHourly_to_georg[parameter]], ['date', 'station_id'], [int(StartingDateTime), ni.name_to_id(station)], [int(EndingDateTime),ni.name_to_id(station)], sort='date')

                    out = q.get_data(hourly_daily, t, ['station_id', self.HistoricalHourly_to_georg[parameter]])
                    #print(out)

                elif (hourly_daily == "daily"):    

                    t = q.smart_slice(hourly_daily, ['date', self.HistoricalDaily_to_georg[parameter]], ['date', 'station_id'], [int(StartingDateTime), ni.name_to_id(station)], [int(EndingDateTime),ni.name_to_id(station)], sort='date')

                    out = q.get_data(hourly_daily, t, ['date', self.HistoricalDaily_to_georg[parameter]])
                    #plt.plot(out[:,1])
                    #plt.show()
                    #print(out)
                    lp.plot_over_time(out,hourly_daily,self.HistoricalDaily_to_georg[parameter])

            #recent 
            elif (recent_hist == "recent"):
                if (hourly_daily == "hourly"):    
                    t = q.smart_slice(hourly_daily, ['station_id', self.HistoricalHourly_to_georg[parameter]], ['date', 'station_id'], [int(StartingDateTime), ni.name_to_id(station)], [int(EndingDateTime),ni.name_to_id(station)], sort='date')

                    out = q.get_data(hourly_daily, t, ['station_id', self.HistoricalHourly_to_georg[parameter]])
                    #print(out)

                elif (hourly_daily == "daily"):    

                    t = q.smart_slice(hourly_daily, ['date', self.HistoricalDaily_to_georg[parameter]], ['date', 'station_id'], [int(StartingDateTime), ni.name_to_id(station)], [int(EndingDateTime),ni.name_to_id(station)], sort='date')

                    out = q.get_data(hourly_daily, t, ['date', self.HistoricalDaily_to_georg[parameter]])
                    plt.plot(out[:,1])
                    plt.show()
                    #print(out)
