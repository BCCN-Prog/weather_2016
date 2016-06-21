from mpl_toolkits.basemap import Basemap, cm
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import h5py


def convert_stations_specs():
    data = pd.read_table('KL_Tageswerte_Beschreibung_Stationen_pandas_import.txt', sep='[ ]{2,}')
    chosen = data[['Stations_id', 'geoLaenge', 'geoBreite', 'Stationshoehe', 'Stationsname', 'Bundesland']]
    chosen.columns = ['id', 'lon', 'lat', 'height', 'name', 'state']
    chosen.to_csv('./dwd_station_specs.csv', index=False)


def id_to_geo_location(id_, source='historic'):

    if source == 'historic':
        csv_file = './dwd_station_specs.csv'
    elif source == 'scraping':
        csv_file = './scraper_geo_locations.csv'
    else:
        raise ValueError("source argument has to be 'historic' or 'scraping'")

    f = os.path.join(os.path.dirname(__file__), csv_file)
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

    # coordinate axes of shapes (grid_dim[i],)
    lat_axis = np.linspace(lat_min, lat_max, grid_dim[0])
    lon_axis = np.linspace(lon_min, lon_max, grid_dim[1])

    # coordinate axes meshgrip of shape (grid_dim[0], grid_dim[1])
    lon_mesh, lat_mesh = np.meshgrid(lon_axis, lat_axis)
   
    # data points and mesh in x/y coordinates
    station_x, station_y = m(station_lon, station_lat)
    x_min, y_min = m(lon_min, lat_min)
    x_max, y_max = m(lon_max, lat_max)
    x_axis = np.linspace(x_min, x_max, grid_dim[0])
    y_axis = np.linspace(y_min, y_max, grid_dim[1])
    x_mesh, y_mesh = np.meshgrid(x_axis, y_axis)
    value_mesh = griddata(station_x, station_y, station_val, x_mesh, y_mesh, interp=interp)
    m.contourf(x_mesh, y_mesh, value_mesh)

    # interpolate datapoints for (station_lon, station_lat) to meshgrid (lat_mesh, lot_mesh)
    #value_mesh = griddata(station_x, station_y, station_val, lon_mesh, lat_mesh, interp=interp)

    lon_grid, lat_grid = m.makegrid(value_mesh.shape[1], value_mesh.shape[0])

    x_grid, y_grid = m(lon_grid, lat_grid)
    #m.contourf(x_grid, y_grid, value_mesh, cmap=cmap)
    #m.contourf(lon_grid, lat_grid, value_mesh, cmap=cmap, latlon=True)

    m.scatter(station_lon, station_lat, color='k', s=5, latlon=True)
   
    plt.show()

def triangulation_map(station_lon, station_lat, station_val, cmap=None, *args, **kwargs):
    """ Using matplotlib.pyplot.tricontourf() function to plot contourplot on an irreguar grid by using triangulation. """

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

    m.contourf(station_lon, station_lat, station_val, cmap=cmap, latlon=True, tri=True, *args, **kwargs)
    m.scatter(station_lon, station_lat, color='k', s=5, latlon=True)

    # Set Triangulation manual?:
    #station_x, station_y = m(station_lon, station_lat)
    #triang = tri.Triangulation(station_x, station_y)
    #plt.tricontour(station_x, station_y, station_val, 15, linewidths=0.5, colors='k')
    #plt.tricontourf(x, y, z, 15, cmap=plt.cm.rainbow, norm=plt.Normalize(vmax=abs(zi).max(), vmin=-abs(zi).max()))
   
    plt.show()


def get_test_scraping_data():

    f = h5py.File('../databases/test_data/hourly_database.hdf5', 'r')
    data = f['weather_data']
    date = data[:,0]
    hour = data[:,1]
    city_ids = data[:,10]
    tmp_hum = data[hour == 13, 5]
    date = date[hour == 13]
    city_ids = city_ids[hour == 13]
    humidity = tmp_hum[date == 20160516]
    city_ids = city_ids[date == 20160516]

    coordinates = id_to_geo_location(city_ids, source='scraping')
    return coordinates, humidity



def map_mvp():
    
    # SCRAPING
    coordinates, values = get_test_scraping_data()

    # HISTORIC
#    coordinates = get_geo_locations(unique_coords=True)
#    values = 20 * np.random.randn(coordinates.shape[0])

    #hexagon_map(coordinates, temperature, hex_grid_size=(20,20))
    interpolated_color_map(coordinates[:,0], coordinates[:,1], values)
    #triangulation_map(coordinates[:,0], coordinates[:,1], temperature)

if __name__ == '__main__':
    map_mvp()

