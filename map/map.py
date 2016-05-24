from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
#from matplotlib import cm as CM
#from matplotlib import mlab as ml
import numpy as np

#lats = np.array([47.813, 50.7827])
#lons = np.array([8.8493, 6.0941])
temperature = np.array([20.0, -6.0])
coordinates = np.array([ [47.813, 8.8493], [50.7827, 6.09419] ])

#def station_map(lats, lons, temperature):
def station_map(coordinates, temperature):
#    map = Basemap(projection='lcc', lat_0 = 51, lon_0 = 10, resolution = 'i', width = 850000, height = 1000000)
    map = Basemap(projection='tmerc', lat_0=51, lon_0=10, llcrnrlat=47, llcrnrlon=5, urcrnrlat=55, urcrnrlon=16, resolution='i')
    map.drawcoastlines()
    map.drawcountries()
    map.drawmapboundary()
    lats = coordinates[:,0]
    lons = coordinates[:,1]
    x, y  = map(lons, lats)
#    map.hexbin(x,y)
    map.hexbin(x, y, C = temperature, gridsize=(9,9), linewidth=0.5, edgecolor='k')
    map.colorbar(location='bottom')
    plt.show()
