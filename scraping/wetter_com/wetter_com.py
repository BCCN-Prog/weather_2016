# Scraping wetter.com
from bs4 import BeautifulSoup
import urllib.request
import time
import os.path

do_6D_forecast = False

# path to the data folder where the html files are saved
datafolder = "../data"

# list fo all cities we are scraping from
cities = ["berlin", "hamburg", "muenchen",
            "koeln", "frankfurt", "stuttgart",
            "bremen", "leipzig", "hannover",
            "nuernberg", "dortmund", "dresden",
            "kassel", "kiel", "bielefeld",
            "saarbruecken", "rostock", "freiburg",
            "magdeburg", "erfurt"]

# corresponding list of IDs used by wetter.com
IDs = ["/DE0001020", "/DE0001020", "/DE0006515",
        "/DE0005156", "/DE0002989", "/DE0010287",
        "/DE0001516", "/DE0006194", "/DE0004160",
        "/DE0007131", "/DE0002221", "/DE0002265",
        "/DE0005331", "/DE0005426", "/DE0001129",
        "/DE0009173", "/DE0009042", "/DE0003017",
        "/DE0006615", "/DE0002658"]

######################### HOURLY & 16 DAYS FORECASTE ############################
# loop over all cities
for i, city in enumerate(cities):
    #### HOURLY
    # construct url from city name and city ID, build filenname
    # example url: http://www.wetter.com/deutschland/berlin/DE0001020.html
    cityUrl = "http://www.wetter.com/wetter_aktuell/wettervorhersage/heute/deutschland/" + city + IDs[i] + ".html?showDiagram=true#detailsDiagram"
    filename = os.path.join(datafolder, "wetter_com_" + time.strftime("%d-%m-%Y_") + city + "_hourly.html")
    # download and save html file with given url and filename
    urllib.request.urlretrieve(cityUrl, filename)

    ### 16 DAYS FORECAST
    # construct url from city name and city ID, build filenname
    # example url: http://www.wetter.com/wetter_aktuell/wettervorhersage/16_tagesvorhersage/deutschland/flensburg/DE0002929.html
    urlbase = "http://www.wetter.com/wetter_aktuell/wettervorhersage/16_tagesvorhersage/deutschland/"
    cityUrl = urlbase + city + IDs[i] + ".html"
    filename = os.path.join(datafolder, "wetter_com_" + time.strftime("%d-%m-%Y_") + city + "_daily.html")
    # download and save html file with given url and filename
    urllib.request.urlretrieve(cityUrl, filename)

######################### 6 DAYS FORECAST  #####################################
# the 6 day forecast has more information than the 16 day one
if do_6D_forecast:
    days = 6
    urlbase = "http://www.wetter.com/wetter_aktuell/wettervorhersage/"
    # loop over days because wetter.com uses seperate URL for every day forecast
    for day in range(days):
        # loop over all cities
        for i, city in enumerate(cities):
            # construct url from day, city name and city ID, build filenname
            if day==0: # for day 1, use "morgen"
                daystring = "morgen"
            else:
                daystring = "in-{}-tagen".format(day+1) # day runs from 0-6
            # example url: http://www.wetter.com/wetter_aktuell/wettervorhersage/morgen/deutschland/flensburg/DE0002929.html
            # example url: http://www.wetter.com/wetter_aktuell/wettervorhersage/in-2-tagen/deutschland/flensburg/DE0002929.html ...
            cityUrl = urlbase + daystring + "/deutschland/" + city + IDs[i]  + ".html"
            # join filename and data folder path, add timestamp
            filename = os.path.join(datafolder, "wetter_com_" + time.strftime("%d-%m-%Y_") + city + "_daily6.html")
            # download and save html file with given url and filename
            urllib.request.urlretrieve(cityUrl, filename)
