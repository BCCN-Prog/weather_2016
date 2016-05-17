import pandas as pd
import numpy as np

entry_dict ={"date":0, "site": 1, "geo":2, "hi":3, "lo":4, "midday":5, "rain_chance":6, "rain_amt":7, "cloud":8}

df = pd.read_csv("61_daily.csv", usecols=[2,1,10,11,14,6])

read_in_dict = {0:"geo", 1:"date", 2:"cloud", 3:"hi", 4:"lo", 5:"rain_amt"}

indices = [entry_dict[read_in_dict[k]] for k in range(len(read_in_dict))]

df = np.array(df.values)
site = np.array([[np.nan] for i in range(df.shape[0])])
midday =  np.array([[np.nan] for i in range(df.shape[0])])
rain_chance =  np.array([[np.nan] for i in range(df.shape[0])])
df = np.hstack((df, site, midday, rain_chance))[:,[1,6, 0, 3, 4, 7, 8, 5, 2]]

print(indices)
