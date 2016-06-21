from mpl_toolkits.basemap import Basemap, cm
#from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

'''
this is not working properly. just trying out some different
functions for visualizing a heat map
'''


def convert_stations_specs():
    data = pd.read_table('KL_Tageswerte_Beschreibung_Stationen_pandas_import.txt', sep='[ ]{2,}')
    chosen = data[['Stations_id', 'geoLaenge', 'geoBreite', 'Stationshoehe', 'Stationsname', 'Bundesland']]
    chosen.columns = ['id', 'lon', 'lat', 'height', 'name', 'state']
    chosen.to_csv('./dwd_station_specs.csv', index=False)


def id_to_geo_location(id_,):
    f = os.path.join(os.path.dirname(__file__), './dwd_station_specs.csv')
    specs = pd.read_csv(f, encoding = "ISO-8859-1")
    coordinates = np.empty((id_.size, 2))
    for i, j in enumerate(id_):
        coordinates[i,:] = specs[specs['id'] == j][['lon', 'lat']].values
    return coordinates


def get_geo_locations(unique_coords=False):
    """ Returns pandas.DataFrame of [latitude, longitude] values extracted from dwd_stations_specs.csv file.
        If unique_coords=True, duplicates of (lon, lat) pairs are dropped (only first occurence kept). """
    f = os.path.join(os.path.dirname(__file__), './dwd_station_specs.csv')
    specs = pd.read_csv(f, encoding = "ISO-8859-1")
    if unique_coords:
        specs.drop_duplicates(['lon', 'lat'], inplace=True)
    coordinates = id_to_geo_location(specs['id'].values)
    return coordinates


def hexagon_map(coordinates, temperature, hex_grid_size=(50,50)):
    m = Basemap(projection='tmerc', lat_0=51, lon_0=10, llcrnrlat=47, llcrnrlon=5, urcrnrlat=55, urcrnrlon=16, resolution='i')
    m.drawcoastlines()
    m.drawcountries()
    m.drawmapboundary()
    lats = coordinates[:,0]
    lons = coordinates[:,1]
    x, y  = m(lons, lats)
    m.hexbin(x, y, C = temperature, gridsize=hex_grid_size, linewidth=0.5, edgecolor='k')
    m.colorbar(location='bottom')
    plt.show()


def interpolated_color_map(station_lon, station_lat, station_val, grid_dim=(80,110), interp='nn', cmap=None):#cm.s3pcpn):

    
    # map boundries
    lat_0 = 51
    lat_min = 47
    lat_max = 55

    lon_0 = 10
    lon_min =  5
    lon_max = 16

    m = Basemap(projection='tmerc', lat_0=lat_0, lon_0=lon_0, 
                llcrnrlat=lat_min, llcrnrlon=lon_min, urcrnrlat=lat_max, 
                urcrnrlon=lon_max, resolution='i')

    m.drawcoastlines()
    m.drawcountries()
    m.drawmapboundary()
    
#    x = np.linspace(0, m.urcrnrx, station_val.shape[1])
#    y = np.linspace(0, m.urcrnry, station_val.shape[0])
#    xx, yy = np.meshgrid(x, y)
    
#    m.contourf(xx, yy, station_val)
    m.contourf(station_lon, station_lat, station_val[:,0], latlon='true')
    
    plt.show()


def map_mvp():
    
    coordinates = get_geo_locations(unique_coords=True)
    temperature = 20 * np.random.randn(coordinates.shape[0],coordinates.shape[0])
    #hexagon_map(coordinates, temperature, hex_grid_size=(20,20))
    interpolated_color_map(coordinates[:,0], coordinates[:,1], temperature)

if __name__ == '__main__':
    map_mvp()

