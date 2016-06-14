from mpl_toolkits.basemap import Basemap, cm
from matplotlib.mlab import griddata
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


def hexagon_map(coordinates, temperature, hex_grid_size=(50,50)):
    m = Basemap(projection='tmerc', lat_0=51, lon_0=10, llcrnrlat=47, llcrnrlon=5, urcrnrlat=55, urcrnrlon=16, resolution='i')
    lats = coordinates[:,0]
    lons = coordinates[:,1]
    x, y  = m(lons, lats)
    plt.ion()
    for i in range(len(temperature)):
        plt.clf()
        m.drawcoastlines()
        m.drawcountries()
        m.drawmapboundary()
        m.hexbin(x, y, C = temperature[:,i], gridsize=hex_grid_size, linewidth=0.5, edgecolor='k', vmin=np.amin(temperature), vmax=np.amax(temperature))
        cb = m.colorbar(location='bottom', label='Random data')
        plt.show()
        plt.pause(0.005)


def interpolated_color_map(lats, lons, values, spatial_resolution=0.1, interp='nn', cmap=None):#cm.s3pcpn):

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

    lats = np.array(lats)
    lons = np.array(lons)
    values = np.array(values)
   
    lat_inum = (lat_max - lat_min) / spatial_resolution
    lon_inum = (lon_max - lon_min) / spatial_resolution
#    xi = np.linspace(lat_min, lat_max + spatial_resolution, xinum)
#    yi = np.linspace(lon_min, lon_max + spatial_resolution, yinum)
    lat_i = np.linspace(lat_min, lat_max, lat_inum)
    lon_i = np.linspace(lon_min, lon_max, lon_inum)
    lat_i, lon_i = np.meshgrid(lat_i, lon_i)
   
    value_i = griddata(lats, lons, values, lat_i, lon_i, interp=interp)

    lat_grid, lon_grid = m.makegrid(value_i.shape[1], value_i.shape[0])
    x_grid, y_grid = m(lat_grid, lon_grid)
    m.contourf(x_grid, y_grid, value_i, cmap=cmap)
    m.scatter(lats, lons, color='k', s=50, latlon=True)
   
    plt.show()


def map_mvp():
    
    coordinates = get_geo_locations()
    temperature = 20 * np.random.randn(coordinates.shape[0],coordinates.shape[0])
    hexagon_map(coordinates, temperature, hex_grid_size=(20,20))
    #interpolated_color_map(coordinates[:,0], coordinates[:,1], temperature)

if __name__ == '__main__':
    map_mvp()

