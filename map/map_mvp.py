from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from map import station_map
from utils import get_geo_locationas

def map_mvp():
    
    coordinates = get_geo_locationas()
    temperature = 20 * np.random.randn(coordinates.shape[0])
    station_map(coordinates, temperature)
