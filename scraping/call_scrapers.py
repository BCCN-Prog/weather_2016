import sys

import scraping.wetter_com.scrape_wetter_com as sc_wc
import itertools

cities_german = {"berlin", "hamburg", "muenchen", "koeln", "frankfurt",
                 "stuttgart", "bremen", "leipzig", "hannover",
                 "nuernberg", "dortmund", "dresden", "kassel", "kiel", "bielefeld",
                 "saarbruecken", "rostock", "freiburg",
                 "magdeburg", "erfurt"}

cities_english = {"berlin", "hamburg", "munich",
                  "cologne", "frankfurt", "stuttgart",
                  "bremen", "leipzig", "hanover",
                  "nuremberg", "dortmund", "dresden",
                  "cassel", "kiel", "bielefeld",
                  "saarbruecken", "rostock", "freiburg",
                  "magdeburg", "erfurt"}

cities = cities_english.union(cities_german)


def prepend_0_if_single_digit(x):
    return '0' + x if len(x) == 1 else x


days = map(prepend_0_if_single_digit, [str(i) for i in range(1, 32)])
months = map(prepend_0_if_single_digit, [str(i) for i in range(4, 8)])
year = '2016'

for day, month, city in itertools.product(days, months, cities):
    date_string = '{}-{}-{}'.format(day, month, year)
    try:
        sc_wc.scrape(date_string, city)
    except:
        err = sys.exc_info()[0]
        print('Excepted error in {}.\n\n{}'.format('wetter_com', err))
