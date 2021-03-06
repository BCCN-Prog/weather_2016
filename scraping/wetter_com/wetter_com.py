def download(datafolder = "../data"):
    """ download html files from wetter.com
    @param datafolder   path to folder where files are saved
    """
    # importing
    from bs4 import BeautifulSoup
    import urllib.request
    import time
    import os.path

    # flog for downloading the detailed 6 day forecast
    do_6D_forecast = False

    # list fo all cities we are scraping from
    cities = ["berlin", "hamburg", "muenchen",
                "koeln", "frankfurt", "stuttgart",
                "bremen", "leipzig", "hannover",
                "nuernberg", "dortmund", "dresden",
                "kassel", "kiel", "bielefeld",
                "saarbruecken", "rostock", "freiburg",
                "magdeburg", "erfurt"]
    cities_english = ["berlin", "hamburg", "munich",
                "cologne", "frankfurt", "stuttgart",
                "bremen", "leipzig", "hanover",
                "nuremberg", "dortmund", "dresden",
                "kassel", "kiel", "bielefeld",
                "saarbruecken", "rostock", "freiburg",
                "magdeburg", "erfurt"]

    # corresponding list of IDs used by wetter.com
    IDs = ["/DE0001020", "/DE0004130", "/DE0006515",
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
        filename = "wetter_com_" + time.strftime("%d-%m-%Y_%H_%M_%S_") + cities_english[i] + "_hourly.html"
        filename = file_existence_check(datafolder, filename)
        # download and save html file with given url and filename
        urllib.request.urlretrieve(cityUrl, os.path.join(datafolder, filename))
        ### 16 DAYS FORECAST
        # construct url from city name and city ID, build filenname
        # example url: http://www.wetter.com/wetter_aktuell/wettervorhersage/16_tagesvorhersage/deutschland/flensburg/DE0002929.html
        urlbase = "http://www.wetter.com/wetter_aktuell/wettervorhersage/16_tagesvorhersage/deutschland/"
        cityUrl = urlbase + city + IDs[i] + ".html"
        filename = "wetter_com_" + time.strftime("%d-%m-%Y_%H_%M_%S_") + cities_english[i] + "_daily.html"
        filename = file_existence_check(datafolder, filename)
        # download and save html file with given url and filename
        urllib.request.urlretrieve(cityUrl, os.path.join(datafolder, filename))

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
                cityUrl = urlbase + daystring + "/deutschland/" + cities_english[i] + IDs[i]  + ".html"
                # join filename and data folder path, add timestamp
                filename = "wetter_com_" + time.strftime("%d-%m-%Y_%H_%M_%S_") + cities_english[i] + "_detailed_daily.html"
                filename = file_existence_check(datafolder, filename)
                # download and save html file with given url and filename
                urllib.request.urlretrieve(cityUrl, os.path.join(datafolder, filename))
#
def file_existence_check(path, filename):
    """Checks for existence, appends counter to file if it already exists.
        Watch out, it's recursive :)
    """
    import os.path
    if  not(os.path.exists(os.path.join(path, filename))):
        return filename
    else:
        # file exists, check for counter
        if filename.split('_')[-1].split('.')[0]=='hourly' or filename.split('_')[-1].split('.')[0]=='daily':
            # there is no counter, append counter
            newfname = filename.split('.')[0] + '_1.html'
        else:
            # there is a counter, get it and increment
            count = int(filename.split('_')[-1].split('.')[0]) + 1
            counterstr = '_{}.html'.format(count)
            newfname = '_'.join(filename.split('_')[:-1]) + counterstr
        # return new filename
        return file_existence_check(path, newfname)
