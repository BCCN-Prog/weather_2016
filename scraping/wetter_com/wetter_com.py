# Scraping wetter.com
from bs4 import BeautifulSoup
import urllib.request
import time
import os.path

# path to the data folder where the html files are saved
datafolder = "../data"

# list fo all cities we are scraping from
cities = ["berlin", "hamburg", "muenchen",
            "koeln", "frankf2urt", "stuttgart",
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

# flag for downloading the hourly forcast in detailed version
detailed = True

# loop over all cities
for i, city in enumerate(cities):
    # construct url from city name and city ID, build filenname
    if detailed:
        cityUrl = "http://www.wetter.com/wetter_aktuell/wettervorhersage/heute/deutschland/" + city + IDs[i] + ".html?showDiagram=true#detailsDiagram"
        filename = os.path.join(datafolder, "wetter_com_" + time.strftime("%d-%m-%Y_") + city + "_detailed.html")
    else:
        # example url: http://www.wetter.com/deutschland/berlin/DE0001020.html
        cityUrl = "http://www.wetter.com/deutschland/" + city + IDs[i]  + ".html"
        # join filename and data folder path, add timestamp
        filename = os.path.join(datafolder, "wetter_com_" + time.strftime("%d-%m-%Y_") + city + "_basic.html")
    # download and save html file with given url and filename
    urllib.request.urlretrieve(cityUrl, filename)
