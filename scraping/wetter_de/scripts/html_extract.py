import time
import urllib.request

FILE_BASE = 'wetter_de_'

DATE_TIME = time.strftime("%d_%m_%Y")

# cities need to be paired with ID
CITIES = ['berlin-18228265', 'muenchen-18225562', 'hamburg-18219464', 'cologne-18220679',
          'frankfurt-18221009', 'stuttgart-18224193', 'bremen-18220609', 'leipzig-18232916',
          'hannover-18219670', 'nuernberg-18227303', 'dortmund-18220926', 'dresden-18232486',
          'kassel-18221338', 'kiel-18218132', 'bielfeld-18220854', 'saarbrücken-18228213',
          'rostock-18230410', 'magdeburg-18233836', 'freiburg-18224951', 'erfurt-18234542']


for city in CITIES:

    HOURLY_URL = 'http://www.wetter.de/deutschland/wetter-' + city + '/wetterbericht-aktuell.html'
    FIFTEEN_URL = 'http://www.wetter.de/deutschland/wetter-' + city + '/wetterprognose.html'

    urllib.request.urlretrieve(HOURLY_URL, FILE_BASE + DATE_TIME + '_' + city.split('-')[0] + '.html')
    urllib.request.urlretrieve(FIFTEEN_URL, FILE_BASE + DATE_TIME + '_' + city.split('-')[0] + '.html')
