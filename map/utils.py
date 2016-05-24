import pandas as pd
import numpy as np

def convert_stations_specs():
    data = pd.read_table('KL_Tageswerte_Beschreibung_Stationen_pandas_import.txt', sep='[ ]{2,}')
    chosen = data[['Stations_id', 'geoBreite', 'geoLaenge', 'Stationshoehe', 'Stationsname', 'Bundesland']]
    chosen.columns = ['id', 'lat', 'lon', 'height', 'name', 'state']
    chosen.to_csv('./dwd_station_specs.csv', index=False)

def id_to_geo_location(id_):
    specs = pd.read_csv('./dwd_station_specs.csv', encoding = "ISO-8859-1")
    coordinates = np.empty((id_.size, 2))
    for i, j in enumerate(id_):
        coordinates[i,:] = specs[specs['id'] == j][['lat', 'lon']].values
    return coordinates

def get_geo_locations():
    specs = pd.read_csv('./dwd_station_specs.csv', encoding = "ISO-8859-1")
    coordinates = id_to_geo_location(specs['id'].values)
    return coordinates

if __name__ == '__main__':
    #idx = np.array([44,73,167])
    #idx = 44
    #c = id_to_geo_location(idx)
    #print(c)
    c = get_geo_locationas()
    print(c)


        


