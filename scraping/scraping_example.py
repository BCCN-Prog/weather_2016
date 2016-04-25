from bs4 import BeautifulSoup
import urllib.request

# load website dynamically, e.g., wetter.info main site for berlin
# we probably won't do it this way because we want to download all the html files
# we are scraping in case anything goes wront and we want to do it again.
"""
url="http://www.wetter.info/wetter-deutschland/berlin/17746530"
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page,"lxml")

# search urls within the main website we just loaded, e.g., sub regions of Berlin
berlinList = soup.find_all("span", class_="pwic_city_text")

# for urls, e.g., sub regions of Berlin scrape the data
for loc in berlinList:
    print(soup.span.get_text())
"""

# Second possibility: download the website html file and scrape it offline
soup = BeautifulSoup(open("index.html"), "lxml")
"""
the soup is the python representation of the html file. we can search for html
objects using "find_all" or we can access them directly, e.g., using soup.title,
soup.p, soup.span, to get the title, all paragraphs or all span objects,
respectively
"""

# define css classes to search for
class_date = "Tfwvdate"
class_rain = "Tfwvnsr"
class_temp_high = "Tfwvhigh Tfwvd"
class_temp_low = "Tfwvlow Tfwvd"

# log the location
print(soup.title.string)

# get the data
# look for all 'span' objects in the html file that have the given class
#this returns a list of soup objects with certain attributes, e.g., soup.string
datelist = soup.find_all('span', class_=class_date)
rainlist = soup.find_all('p', class_=class_rain)
highlist = soup.find_all('p', class_=class_temp_high)
lowlist = soup.find_all('p', class_=class_temp_low)

# log results
for i in range(len(datelist)):
    print(datelist[i].string + ' Niederschlag '+ rainlist[i].string + " Temp " + lowlist[i].string + " - " + highlist[i].string)
