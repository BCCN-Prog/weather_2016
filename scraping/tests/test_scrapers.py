import unittest
import os, sys
sys.path.append("../wetter_com")
import wetter_com as downloader
import scrape_wetter_com as scraper
import time
import numpy as np

class Test_wetter_com(unittest.TestCase):

    test_data_path = 'test_data'
    test_date = time.strftime("%d-%m-%Y")

    def test_download(self):
        print("Testing downloading script")
        downloader.download(self.test_data_path)

    def test_scraping(self):
        print("Testing scraping scripts")
        cities = ["berlin", "hamburg", "munich",
                    "cologne", "frankfurt", "stuttgart",
                    "bremen", "leipzig", "hanover",
                    "nuremberg", "dortmund", "dresden",
                    "kassel", "kiel", "bielefeld",
                    "saarbruecken", "rostock", "freiburg",
                    "magdeburg", "erfurt"]
        # test three random cities
        for i in range(3):
            city = cities[np.random.randint(len(cities))]
            scraper.scrape(self.test_date, city, data_path=self.test_data_path)
        # remove test files
        filelist = [ f for f in os.listdir(self.test_data_path) if f.endswith(".html") ]
        for f in filelist:
            os.remove(os.path.join(self.test_data_path, f))

#if __name__ == '__main__':
    #unittest.main()
