from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from map import station_map
from utils import get_geo_locations

def map_mvp():
    
    coordinates = get_geo_locations()
    temperature = 20 * np.random.randn(coordinates.shape[0])
    station_map(coordinates, temperature, hex_grid_size=(20,20))

if __name__ == '__main__':
    map_mvp()
