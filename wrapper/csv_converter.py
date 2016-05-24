import pandas as pd
import numpy as np


df = pd.read_csv("61_daily.csv", usecols=[2,1,10,11,14,6])


df = np.array(df.values)
site = np.array([[np.nan] for i in range(df.shape[0])])
midday =  np.array([[np.nan] for i in range(df.shape[0])])
rain_chance =  np.array([[np.nan] for i in range(df.shape[0])])
df = np.hstack((df, site, midday, rain_chance))[:,[1,6, 0, 3, 4, 7, 8, 5, 2]]

print(df[0])
