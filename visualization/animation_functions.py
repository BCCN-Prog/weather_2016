from mpl_toolkits.basemap import Basemap, cm
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import os
import h5py
import pickle


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
        coordinates[i,:] = specs[specs['id'] == j][['lon', 'lat']].values[0]
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


def hexagon_animation(station_lon, station_lat, station_val, hex_grid_size=(50,50)):
    """
    Creates an animation of values over time for different stations, using hexagons per station location.

    Params:
        station_lon (1D array): longitutes of station locations
        station_lat (1D array): latitudes of station locations
        station_val (2D array): values to plot per stations over time
        hex_grid_size (tuple, optional): number of hexagons in x and y dimension
    """

    m = Basemap(projection='tmerc', lat_0=51, lon_0=10, llcrnrlat=47, llcrnrlon=5, urcrnrlat=55, urcrnrlon=16, resolution='i')
    #with open('germany_map.pkl', 'rb') as input:
        #m = pickle.load(input) # open map from disk
    x, y  = m(station_lon, station_lat)
    plt.ion()
    for i in range(np.shape(station_val)[1]):
        plt.clf()
        m.drawcoastlines()
        m.drawcountries()
        m.drawmapboundary()
        m.hexbin(x, y, C = station_val[:,i], gridsize=hex_grid_size, linewidth=0.5, edgecolor='k', vmin=np.amin(station_val), vmax=np.amax(station_val))
        cb = m.colorbar(location='bottom', label='Random Data', ticks=[np.amin(station_val), 0,  np.amax(station_val)])
        plt.title('{}. day'.format(i + 1))
        plt.show()
        plt.pause(0.005)
    

def interpolated_color_map(station_lon, station_lat, station_val, grid_dim=(80,110), interp='nn', return_figure=False):
    """
    Creates a map of values for different stations. The station location can be on an irregular grid,
    for intermediate locations interpolation is used.

    Params:
        station_lon (1D array): longitutes of station locations
        station_lat (1D array): latitudes of station locations
        station_val (2D array): values to plot per stations over time
        grid_dim (tuple, optional):
            number of interpolated data points in lon/lat dimension
        interp ('nn' or 'linear', optional):
            interpolation type, 'nn': Natgrid nearest neighbour interpolation method
        return_figure (bool, optional):
            weather or not to return the figure object, if True, plt.show() is not called
    """


    # map boundries
    lat_0 = 51
    lat_min = 47
    lat_max = 55

    lon_0 = 10
    lon_min =  5
    lon_max = 16
    
    #with open('germany_map.pkl', 'rb') as input:
        #m = pickle.load(input) # open map from disk

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
    
    levels = np.linspace(np.amin(station_val), np.amax(station_val))
    #norm = mpl.colors.Normalize(clip=False, vmin=np.amin(station_val), vmax=np.amax(station_val))
    
    plt.ion()
    for i in range(np.shape(station_val)[1]):
        plt.clf()
        m.drawcoastlines()
        m.drawcountries()
        m.drawmapboundary()
        value_mesh = griddata(station_x, station_y, station_val[:,i], x_mesh, y_mesh, interp=interp) #for python 2.7 interp = 'linear
        cont = m.contourf(x_mesh, y_mesh, value_mesh, vmin=np.amin(station_val), vmax=np.amax(station_val), levels=levels)
        #cont.set_clim([np.amin(station_val), np.amax(station_val)])
        #cont = m.contourf(x_mesh, y_mesh, value_mesh, levels, origin='lower')
        m.scatter(station_lon, station_lat, color='k', s=5, latlon=True)
        cb = m.colorbar(cont, location='bottom', label='Random Data', ticks=[np.amin(station_val), 0,  np.amax(station_val)])
        #plt.clim(np.amin(station_val), np.amax(station_val))
        plt.title('{}. day'.format(i + 1))
        if return_figure:
            return plt.gcf()
        else:
            plt.show()
            plt.pause(0.001)

    # interpolate datapoints for (station_lon, station_lat) to meshgrid (lat_mesh, lot_mesh)
    #value_mesh = griddata(station_x, station_y, station_val, lon_mesh, lat_mesh, interp=interp)

    #lon_grid, lat_grid = m.makegrid(value_mesh.shape[1], value_mesh.shape[0])

    #x_grid, y_grid = m(lon_grid, lat_grid)
    #m.contourf(x_grid, y_grid, value_mesh, cmap=cmap)
    #m.contourf(lon_grid, lat_grid, value_mesh, cmap=cmap, latlon=True)

    #m.scatter(station_lon, station_lat, color='k', s=5, latlon=True)
   
    #if return_figure:
        #return plt.gcf()
    #else:
        #plt.show()


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



def animation_mvp():
    
    # SCRAPING
    #coordinates, values = get_test_scraping_data()

    # HISTORIC
    days_n = 20
    coordinates = get_geo_locations(unique_coords=True)
    #values = 20 * np.random.randn(coordinates.shape[0])
    values = np.random.randn(coordinates.shape[0],days_n)

    #hexagon_animation(coordinates[:,0], coordinates[:,1], values, hex_grid_size=(20,20))
    interpolated_color_map(coordinates[:,0], coordinates[:,1], values, return_figure=False)
    #triangulation_map(coordinates[:,0], coordinates[:,1], temperature)

if __name__ == '__main__':
    animation_mvp()

