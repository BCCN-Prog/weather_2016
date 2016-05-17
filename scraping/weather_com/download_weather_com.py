def download(datafolder = "/home/brain/Documents/BCCN_Prog/"):
    """ download html files from wetter.com
    @param datafolder   path to folder where files are saved
    """
    print('enter downloads')
    # importing
    from bs4 import BeautifulSoup
    import urllib.request
    import time
    import os.path

    #url example: https://weather.com/weather/today/l/GMXX0007:1:GM (berlin today)
    # https://weather.com/weather/tenday/l/GMXX0007:1:GM
    
    url_base_daily = 'https://weather.com/weather/today/l'
    url_base_10day = 'https://weather.com/weather/tenday/l'

    # list fo all cities 
    cities = ["berlin",  "muenchen", "hamburg",
                "koeln", "frankfurt", "stuttgart",
                "bremen", "leipzig", "hannover",
                "nuernberg", "dortmund", "dresden",
                "kassel", "kiel", "bielefeld",
                "saarbruecken", "rostock",
                "magdeburg",  "freiburg im breisgau", "erfurt"]

    # corresponding list of IDs used by weather.com
    IDs = ["/GMXX0007", "/GMXX1002", "/GMXX0049",
            "/GMXX0049", "/GMXX0040", "/GMXX0128",
            "/GMXX0014", "/GMXX0072", "/GMXX0051",
            "/GMXX0096", "/GMXX0024", "/GMXX0025",
            "/GMXX0153", "/GMXX0064", "/GMXX6175",
            "/GMXX0117", "/GMXX1813", "/GMXX0079",
            "/GMXX0041", "/GMXX0033"]


    for i, ID in enumerate(IDs):

        Url_daily = url_base_daily + ID + ":1:GM"
        Url_10day = url_base_10day + ID + ":1:GM"
        filename_daily = os.path.join(datafolder, "weather_com_daily_" + time.strftime("%d-%m-%Y_") + cities[i] + ".html")
        filename_10day = os.path.join(datafolder, "weather_com_10day_" + time.strftime("%d-%m-%Y_") + cities[i] + ".html")
        #download and save html file with given url and filename
        urllib.request.urlretrieve(Url_daily, filename_daily)
        urllib.request.urlretrieve(Url_10day, filename_10day)
        url_test= "https://weather.com/weather/today/l/GMXX0033:1:GM"
        filename = os.path.join(datafolder, "test.html")
        urllib.request.urlretrieve(url_test, filename)


def main():
    print('entered main')
    download()
    print("done")


if __name__ == "__main__":
    main()
