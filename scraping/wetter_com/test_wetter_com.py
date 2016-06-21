"""Tests the scrape_wetter_com methods in scrape_wetter_com.py"""

import pprint
import os
import scrape_wetter_com as scraper
from scrape_wetter_com import OKException
import traceback

data_path = 'some_wetter_com_data'
processed_path = '../data/processed'

# dates to process
dates = ['02-05-2016']

# list fo all cities we are scraping from
cities = ["berlin"] # testing
# cities = ["berlin", "hamburg", "munich",
#              "cologne", "frankfurt", "stuttgart",
#              "bremen", "leipzig", "hanover",
#              "nuremberg", "dortmund", "dresden",
#              "kassel", "kiel", "bielefeld",
#              "saarbruecken", "rostock", "freiburg",
#              "magdeburg", "erfurt"]
# cities_german = ["berlin", "muenchen",
#              "koeln", "frankfurt", "stuttgart",
#              "bremen", "leipzig", "hannover",
#              "nuernberg", "dortmund", "dresden",
#              "kassel", "kiel", "bielefeld",
#              "saarbruecken", "rostock", "freiburg",
#              "magdeburg", "erfurt"]

processed_dates = []
processed_cities = []

# for every date:
for date in dates:
    for i,city in enumerate(cities):
        # make dict
        try:
            scraper.scrape(date, city, data_path)
        except(OKException):
            print(traceback.print_exc())


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
