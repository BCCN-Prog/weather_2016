
import sys
sys.path.append('../visualization')
sys.path.append('../query_engine_v2')
import map_functions as mf
import QueryEngine as qe
import name_to_id as ni
import matplotlib.pyplot as plt

class Executor:




    def __init__(self):
        self.description = 'Dummy description'
        self.HistoricalDaily_to_georg={'Maximum Temperature':'high', 'Minimum Temperature':'low', 'Average Temperature':'temperature','Rain            Chance':'rain_chance', 'Rain Amount':'rain_amt', 'Cloud Cover':'cloud_cover'}
        self.HistoricalHourly_to_georg={'Temperature':'temperature', 'Moisture':'humidity', 'Cloud Cover':'cloud_cover', 'Rainfall':'rain_chance', 'Rain Amount':'rain_amt'}#, 'Air Pressure reduced', 'Air Pressure Station', 'Windspeed'


    def get_data(self,hourly_daily, recent_hist, parameter, station, StartingDateTime, EndingDateTime):
        q = qe.QueryEngine()
        if (station == "All"):


            

            if (hourly_daily == "hourly"):    
                s = q.smart_slice(hourly_daily, ['station_id', self.HistoricalHourly_to_georg[parameter]], 'date', int(StartingDateTime), int(EndingDateTime))
                #t = q.smart_slice('daily', ['station_id', 'temperature'], 'station_id', 100, 100, sort='date')
                out = q.get_data(hourly_daily, s, ['station_id', self.HistoricalHourly_to_georg[parameter]])


            elif (hourly_daily == "daily"):    
                s = q.smart_slice(hourly_daily, ['station_id', self.HistoricalDaily_to_georg[parameter]], 'date', int(StartingDateTime), int(EndingDateTime))
                #t = q.smart_slice('daily', ['station_id', 'temperature'], 'station_id', 100, 100, sort='date')
                out = q.get_data(hourly_daily, s, ['station_id', self.HistoricalDaily_to_georg[parameter]])

            ids, vals = out[:,0], out[:,1]
            locs = mf.id_to_geo_location(ids, source='historic')
            #mf.hexagon_map(locs[:,0], locs[:,1], vals , hex_grid_size=(50,50))
            mf.interpolated_color_map(locs[:,0], locs[:,1], vals, interp='linear')
            
        elif (station != "All"):
            if (hourly_daily == "hourly"):    
                #s = q.smart_slice(hourly_daily, ['station_id', self.HistoricalHourly_to_georg[parameter]], 'date', int(StartingDateTime), int(EndingDateTime))

                t = q.smart_slice(hourly_daily, ['station_id', self.HistoricalHourly_to_georg[parameter]], ['date', 'station_id'], [int(StartingDateTime), ni.name_to_id(station)], [int(EndingDateTime),ni.name_to_id(station)], sort='date')

                out = q.get_data(hourly_daily, t, ['station_id', self.HistoricalHourly_to_georg[parameter]])
                print(out)

            elif (hourly_daily == "daily"):    

                t = q.smart_slice(hourly_daily, ['date', self.HistoricalDaily_to_georg[parameter]], ['date', 'station_id'], [int(StartingDateTime), ni.name_to_id(station)], [int(EndingDateTime),ni.name_to_id(station)], sort='date')

                out = q.get_data(hourly_daily, t, ['date', self.HistoricalDaily_to_georg[parameter]])
                plt.plot(out[:,1])
                plt.show()
                print(out)
