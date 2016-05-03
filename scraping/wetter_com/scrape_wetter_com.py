from bs4 import BeautifulSoup
from glob import glob
import numpy as np

# download the website html file and scrape it offline
# get the list of daily data
daily_list = glob("../data/*daily.html")
# get the list of hourly data
hourly_list = glob("../data/*hourly.html")

# do hourly scraping
# prelocate temperature matrix
temp_mat = np.zeros((len(hourly_list), 24))
for i, filename in enumerate(hourly_list):
    print("Scraping "+ filename)
    soup = BeautifulSoup(open(filename), "lxml")
    hours = soup.find_all('div', class_ = '[ half-left ][ bg--white ][ cover-top ][ text--blue-dark ]')
    # get the starting hour of the hour table
    starting_hour = int((hours[0].string.split()[0])[1])
    # get all the temperature divs
    temps = soup.find_all('div', class_ = '[ half-left ][ bg--white ][ js-detail-value-container ]')
    # for every div, get the string, take the temperature value and save it in the matrix
    assert(len(temps)==24)
    for j, div in enumerate(temps) :
        temp_mat[i, j] = int(div.string.split()[0])


    # for testing do it for only one file
    #break

print(temp_mat)
