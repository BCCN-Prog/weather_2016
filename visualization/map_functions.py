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


def id_to_geo_location(id_, hourly_daily, source='historic'):

    if source == 'historic':
        if hourly_daily == "daily":
            csv_file = './dwd_station_specs_daily.csv'
        elif hourly_hourly == "daily":
            csv_file = './dwd_station_specs_hourly.csv'
    elif source == 'scraping':
        csv_file = './scraper_geo_locations.csv'
    else:
        raise ValueError("source argument has to be 'historic' or 'scraping'")

    f = os.path.join(os.path.dirname(__file__), csv_file)
    specs = pd.read_csv(f, encoding = "ISO-8859-1")
    coordinates = np.empty((id_.size, 2))
    for i, j in enumerate(id_):
        #print(coordinates[i,:].shape, specs[specs['id'] == j][['lon', 'lat']].values.shape, specs[specs['id'] == j][['lon', 'lat']].values)
        try:        
            coordinates[i,:] = specs[specs['id'] == j][['lon', 'lat']].values
        except:
            coordinates[i,:] = [np.nan, np.nan]
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


def hexagon_map(station_lon, station_lat, station_val, hex_grid_size=(50,50)):
    """
    Creates a map of values for different stations, using hexagons per station location.

    Params:
        station_lon (1D arrya): longitutes of station locations
        station_lat (1D arrya): latitudes of station locations
        station_val (1D arrya): values to plot per stations
        hex_grid_size (tuple, optional): number of hexagons in x and y dimension
    """

    m = Basemap(projection='tmerc', lat_0=51, lon_0=10, llcrnrlat=47, llcrnrlon=5, urcrnrlat=55, urcrnrlon=16, resolution='i')
    #with open('germany_map.pkl', 'rb') as input:
        #m = pickle.load(input) # open map from disk
    m.drawcoastlines()
    m.drawcountries()
    m.drawmapboundary()
    x, y  = m(station_lon, station_lat)
    m.hexbin(x, y, C = station_val, gridsize=hex_grid_size, linewidth=0.5, edgecolor='k', vmin=np.nanmin(station_val), vmax=np.nanmax(station_val))
    #m.colorbar(location='bottom')
    cb = m.colorbar(location='bottom', label='Random Data', ticks=[np.nanmin(station_val), 0,  np.nanmax(station_val)])
    plt.show()


def interpolated_color_map(station_lon, station_lat, station_val, param_input = "Parameter", grid_dim=(80,110), interp='nn', return_figure=False):
    """
    Creates a map of values for different stations. The station location can be on an irregular grid,
    for intermediate locations interpolation is used.

    Params:
        station_lon (1D arrya): longitutes of station locations
        station_lat (1D arrya): latitudes of station locations
        station_val (1D arrya): values to plot per stations
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

    m = Basemap(projection='tmerc', lat_0=lat_0, lon_0=lon_0, 
                llcrnrlat=lat_min, llcrnrlon=lon_min, urcrnrlat=lat_max, 
                urcrnrlon=lon_max, resolution='i')
    #with open('germany_map.pkl', 'rb') as input:
        #m = pickle.load(input) # open map from disk

    m.drawcoastlines()
    m.drawcountries()
    m.drawmapboundary()

    # coordinate axes of shapes (grid_dim[i],)
    lat_axis = np.linspace(lat_min, lat_max, grid_dim[0])
    lon_axis = np.linspace(lon_min, lon_max, grid_dim[1])

    # coordinate axes meshgrip of shape (grid_dim[0], grid_dim[1])
    lon_mesh, lat_mesh = np.meshgrid(lon_axis, lat_axis)
    
    # contour levels
    levels = np.linspace(np.nanmin(station_val), np.nanmax(station_val))
   
    # data points and mesh in x/y coordinates
    station_x, station_y = m(station_lon, station_lat)
    x_min, y_min = m(lon_min, lat_min)
    x_max, y_max = m(lon_max, lat_max)
    x_axis = np.linspace(x_min, x_max, grid_dim[0])
    y_axis = np.linspace(y_min, y_max, grid_dim[1])
    x_mesh, y_mesh = np.meshgrid(x_axis, y_axis)
    value_mesh = griddata(station_x, station_y, station_val, x_mesh, y_mesh, interp=interp)
    cont = m.contourf(x_mesh, y_mesh, value_mesh, vmin=np.nanmin(station_val), vmax=np.nanmax(station_val), levels=levels)

    # interpolate datapoints for (station_lon, station_lat) to meshgrid (lat_mesh, lot_mesh)
    #value_mesh = griddata(station_x, station_y, station_val, lon_mesh, lat_mesh, interp=interp)

    lon_grid, lat_grid = m.makegrid(value_mesh.shape[1], value_mesh.shape[0])

    x_grid, y_grid = m(lon_grid, lat_grid)
    #m.contourf(x_grid, y_grid, value_mesh, cmap=cmap)
    #m.contourf(lon_grid, lat_grid, value_mesh, cmap=cmap, latlon=True)

    m.scatter(station_lon, station_lat, color='k', s=5, latlon=True)
    print(station_val)
    cb = m.colorbar(cont, location='bottom', label=param_input, ticks=[np.nanmin(station_val), 0,  np.nanmax(station_val)])
   
    if return_figure:
        return plt.gcf()
    else:
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
    #coordinates, values = get_test_scraping_data()

    # HISTORIC
    coordinates = get_geo_locations(unique_coords=True)
    values = 20 * np.random.randn(coordinates.shape[0])

    hexagon_map(coordinates[:,0], coordinates[:,1], values, hex_grid_size=(20,20))
    #interpolated_color_map(coordinates[:,0], coordinates[:,1], values, return_figure=False)
    #triangulation_map(coordinates[:,0], coordinates[:,1], temperature)

if __name__ == '__main__':
    map_mvp()

