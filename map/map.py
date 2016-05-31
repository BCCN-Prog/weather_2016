from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from map import station_map
from utils import get_geo_locations

def station_map(coordinates, temperature, hex_grid_size=(50,50)):
    map = Basemap(projection='tmerc', lat_0=51, lon_0=10, llcrnrlat=47, llcrnrlon=5, urcrnrlat=55, urcrnrlon=16, resolution='i')
    map.drawcoastlines()
    map.drawcountries()
    map.drawmapboundary()
    lats = coordinates[:,0]
    lons = coordinates[:,1]
    x, y  = map(lons, lats)
    map.hexbin(x, y, C = temperature, gridsize=hex_grid_size, linewidth=0.5, edgecolor='k')
    map.colorbar(location='bottom')
    plt.show()


def map_mvp():
    
    coordinates = get_geo_locations()
    temperature = 20 * np.random.randn(coordinates.shape[0])
    station_map(coordinates, temperature, hex_grid_size=(20,20))

if __name__ == '__main__':
    map_mvp()
