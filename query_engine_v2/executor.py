
import sys
sys.path.append('../visualization')
sys.path.append('../query_engine_v2')
import map_functions as mf
import QueryEngine as qe


class Executor:

    def __init__(self):
        self.description = 'Dummy description'
        


    def get_data(self,hourly_daily, recent_hist, parameter, station, StartingDateTime, EndingDateTime):
        #print("hi")
    #    print(args)


    #Stuff below here will be put into get_data function once stuff is working.



        q = qe.QueryEngine()

        s = q.smart_slice('daily', ['station_id', 'temperature'], 'date', 20160101, 20160101)
        #t = q.smart_slice('daily', ['station_id', 'temperature'], 'station_id', 100, 100, sort='date')
        out = (q.get_data('daily', s, ['station_id', 'temperature']))

        ids, vals = out[:,0], out[:,1]
        #print(ids)
        locs = mf.id_to_geo_location(ids, source='historic')
        #mf.hexagon_map(locs[:,0], locs[:,1], vals , hex_grid_size=(50,50))
        mf.interpolated_color_map(locs[:,0], locs[:,1], vals, interp='linear')
