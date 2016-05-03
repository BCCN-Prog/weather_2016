from bs4 import BeautifulSoup
from glob import glob
import numpy as np

# download the website html file and scrape it offline
# get the list of daily data
daily_list = glob("../data/*daily.html")
# get the list of hourly data
hourly_list = glob("../data/*hourly.html")

# do hourly scraping
hour_class = '[ half-left ][ bg--white ][ cover-top ][ text--blue-dark ]'
temp_class = '[ half-left ][ bg--white ][ js-detail-value-container ]'
rainprob_class = 'mt--'
rainAmount_class = '[ mb-- ][ block ][ text--small ][ absolute absolute--left ][ one-whole ]'
windDir_class = '[ mb- ][ block ]'
windAmount_class = '[ js-detail-value-container ][ one-whole ][ mb- ][ text--small ]'
pressure_class = '[ mb- mt-- ][ block ][ text--small ]'
humidity_class = '[ mb-- ][ block ][ text--small ]'

# prelocate data matrices
temp_mat = np.zeros((len(hourly_list), 24))
rainprobs_mat = np.zeros((len(hourly_list), 24))
rainAmount_mat = np.zeros((len(hourly_list), 24))
windDir_dics = [] # use dic for string
windAmount_mat = np.zeros((len(hourly_list), 24))
airpress_mat = np.zeros((len(hourly_list), 24))
airhum_mat = np.zeros((len(hourly_list), 24))

for i, filename in enumerate(hourly_list):
    print("Scraping "+ filename)
    soup = BeautifulSoup(open(filename), "lxml")
    hours = soup.find_all('div', class_ = '[ half-left ][ bg--white ][ cover-top ][ text--blue-dark ]')
    # get the starting hour of the hour table
    starting_hour = int((hours[0].string.split()[0])[1])

    # SCRAPE TEMPERATURE
    # get all the temperature divs
    temps = soup.find_all('div', class_ = '[ half-left ][ bg--white ][ js-detail-value-container ]')
    # for every div, get the string, take the temperature value and save it in the matrix
    assert(len(temps)==24)
    for j, div in enumerate(temps) :
        temp_mat[i, j] = int(div.string.split()[0])

    # SCRAPE Rain probs
    probs = soup.find_all('p', class_ = rainprob_class)[:24]
    for j, p in enumerate(probs):
        rainprobs_mat[i,j] = int(p.string.split()[0])

    # SCRAPE Rain amounts
    amounts = soup.find_all('span', class_ = rainAmount_class)
    for j, span in enumerate(amounts):
        rainAmount_mat[i,j] = float(span.text.split()[0])

    # SCRAPE Wind directions
    windDirs = soup.find_all('span', class_=windDir_class)
    # append to list of dics for saving strings
    windDir_dics.append({})
    for j, span in enumerate(windDirs):
        windDir_dics[i][j] = span.text

    # SCRAPE Wind strength
    wstr = soup.find_all('div', class_=windAmount_class)
    for j, div in enumerate(wstr):
        windAmount_mat[i,j] = int(div.string.split()[0])

    # SCRAPE pressure
    airpress = soup.find_all('span', class_ = pressure_class)
    for j, span in enumerate(airpress):
        airpress_mat[i,j] = int(span.text.split()[0])

    # SCRAPE air humidity
    airhum = soup.find_all('span', class_=humidity_class)
    for j, span in enumerate(airhum):
        airhum_mat[i,j] = int(span.text.split()[0])
    # for testing do it for only one file
    break

# for testing
print(airhum_mat)
