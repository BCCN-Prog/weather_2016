from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib import cm as CM
from matplotlib import mlab as ml
import numpy as np

lats = np.array([47.813, 50.7827])
lons = np.array([8.8493, 6.0941])
temperature = np.array([20.0, -6.0])

'''
def get_geolocation():
    
    arr = []
    with open('coordinates.txt', 'r', encoding='ISO-8859-1') as f:
        arr = [line.rstrip('\n')  for line in open('coordinates.txt', 'r', encoding='ISO-8859-1')]
    
    arr = arr[1:-1]
    
    return arr
'''
'''
def station_map2(lats, lons, temperature):
    map = Basemap(projection='lcc', lat_0 = 51, lon_0 = 10, resolution = 'i', width = 850000, height = 1000000)
    map.drawcoastlines()
    map.drawcountries()
    map.drawmapboundary()
    
    ny = temperature.shape[0]
#    nx = temperature.shape[1]
    nx = 1
    
    lon_bins = np.linspace(min(lons), max(lons), nx + 1)
    lat_bins = np.linspace(min(lats), max(lats), ny + 1)
    
    density, _, _ = np.histogram2d(lats, lons, [lat_bins, lon_bins])
    lon_bins_2d, lat_bins_2d = np.meshgrid(lon_bins, lat_bins)
    xs, ys = map(lon_bins_2d, lat_bins_2d)
    
    plt.pcolormesh(xs, ys, density)
    plt.colorbar(orientation='horizontal')
    plt.scatter(*map(lons, lats))
    plt.show()
'''

#def station_map(lats, lons, temperature):
def station_map(coordinates, temperature):
    map = Basemap(projection='lcc', lat_0 = 51, lon_0 = 10, resolution = 'i', width = 850000, height = 1000000)
#    map.plot(x, y, 'bo')
    map.drawcoastlines()
    map.drawcountries()
#    map.fillcontinents(color = 'coral')
    map.drawmapboundary()
    
#    ny = temperature.shape[0]
#    nx = temperature.shape[1]
#    lons, lats = map.makegrid(nx, ny)
    lats = coordinates[:,0]
    lons = coordinates[:,1]
    x, y  = map(lons, lats)
    c = temperature
#    map.hexbin(x,y)
    map.hexbin(x, y, C = c, gridsize=(9,9), linewidth=0.5, edgecolor='k')
    map.colorbar(location='bottom')
#    map.plot(x,y,'bo',markersize=10)
#    print(x.shape, y.shape)
#    cs = map.contourf(x,y,temperature)
    plt.show()
'''    
    x, y, z = np.random.rand(3, 1000000)
    x *= 12e6
    y *= 9e6
    z *= 20000
    
    gridsize = 1000
    map.hexbin(x, y, C=z, gridsize=gridsize, cmap=plt.cm.YlGnBu)
    
    cb = map.colorbar()
#    map.set_label('Density')
'''
