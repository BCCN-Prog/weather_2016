import pandas as pd

def name_to_id(name):
    stations = pd.read_table('stats.txt', sep=",", usecols=['id','name'])
    a = stations.set_index('name').to_dict()
    return (a['id'][name])
