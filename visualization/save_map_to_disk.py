import pickle
from mpl_toolkits.basemap import Basemap, cm

m = Basemap(projection='tmerc', lat_0=51, lon_0=10, llcrnrlat=47, llcrnrlon=5, urcrnrlat=55, urcrnrlon=16, resolution='i')

with open('germany_map.pkl', 'wb') as output:
    pickle.dump(m, output, pickle.HIGHEST_PROTOCOL)
