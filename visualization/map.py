from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


def convert_stations_specs():
    data = pd.read_table('KL_Tageswerte_Beschreibung_Stationen_pandas_import.txt', sep='[ ]{2,}')
    chosen = data[['Stations_id', 'geoBreite', 'geoLaenge', 'Stationshoehe', 'Stationsname', 'Bundesland']]
    chosen.columns = ['id', 'lat', 'lon', 'height', 'name', 'state']
    chosen.to_csv('./dwd_station_specs.csv', index=False)


def id_to_geo_location(id_):
    f = os.path.join(os.path.dirname(__file__), './dwd_station_specs.csv')
    specs = pd.read_csv(f, encoding = "ISO-8859-1")
    coordinates = np.empty((id_.size, 2))
    for i, j in enumerate(id_):
        coordinates[i,:] = specs[specs['id'] == j][['lat', 'lon']].values
    return coordinates


def get_geo_locations():
    f = os.path.join(os.path.dirname(__file__), './dwd_station_specs.csv')
    specs = pd.read_csv(f, encoding = "ISO-8859-1")
    coordinates = id_to_geo_location(specs['id'].values)
    return coordinates


def station_map(coordinates, temperature, hex_grid_size=(50,50)):
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


def map_mvp():
    
    coordinates = get_geo_locations()
    temperature = 20 * np.random.randn(coordinates.shape[0])
    station_map(coordinates, temperature, hex_grid_size=(20,20))

if __name__ == '__main__':
    map_mvp()
