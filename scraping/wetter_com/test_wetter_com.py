"""Tests the scrape_wetter_com methods in scrape_wetter_com.py"""

import pprint
import os
import scrape_wetter_com as scraper

data_path = '../data'
processed_path = '../data/processed'

# dates to process
dates = ['30-05-2016']

# list fo all cities we are scraping from
cities = ["berlin"] # testing
# cities = ["berlin", "hamburg", "munich",
#             "cologne", "frankfurt", "stuttgart",
#             "bremen", "leipzig", "hanover",
#             "nuremberg", "dortmund", "dresden",
#             "cassel", "kiel", "bielefeld",
#             "saarbruecken", "rostock", "freiburg",
#             "magdeburg", "erfurt"]

processed_dates = []
processed_cities = []

# for every date:
for date in dates:
    for i,city in enumerate(cities):
        # make dict
        data_dic = scraper.scrape(date, city)
        pprint.pprint(data_dic)
        processed_dates.append(date)
        processed_cities.append(city)

# move processed files to 'processed' folder
testing = True
if not(testing):
    for date in processed_dates:
        for city in processed_cities:
            filename = get_filename('../data', date, city, mode='hourly')
            oldpath = data_path + '/' + filename
            newpath = processed_path + '/' + filename
            os.rename(oldpath, newpath)
            filename = get_filename('../data', date, city, mode='daily')
            oldpath = data_path + '/' + filename
            newpath = processed_path + '/' + filename
            os.rename(oldpath, newpath)
