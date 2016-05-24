import pickle
import numpy as np

def scrape (filename):
    with open(filename, 'rb') as f:
        dat = pickle.load(f)
        f.close()
    if ('hourly_forecast' in dh.keys()):
        scrape_hourly (dat)
    elif ('forecast' in dh.keys()):
        scrape_daily (dat)
    else: raise Exception ('File data cannot be recognized')
    
def scrape_hourly (dat):
    

