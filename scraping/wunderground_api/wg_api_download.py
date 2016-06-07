import urllib.request
import json
import codecs
import pickle
import time
import os.path



loc_list = ['Berlin', 'Munich', 'Hamburg', 'Cologne', 'Frankfurt', 'Stuttgart', 'Bremen', 'Leipzig', 'Hannover', 'Nuremberg', 'Dortmund', 'Dresden', 'Kassel', 'Kiel', 'Bielefeld', 'Saarbruecken', 'Rostock', 'Freiburg', 'Erfurt', 'Magdeburg']
#loc_list = ['Berlin', 'Munich'] #short list for testing

def download(datafolder):
    #download daily 10 day forecast
    #example url: http://api.wunderground.com/api/944b3f3c879d2394/geolookup/forecast10day/q/Germany/Berlin.json
    for loc in loc_list:
        #get the json object
        f = urllib.request.urlopen('http://api.wunderground.com/api/944b3f3c879d2394/geolookup/forecast10day/q/Germany/'+loc+'.json')
        #need to convert byte object to string
        reader = codecs.getreader('utf-8') #how is data encoded? 
        parsed_json = json.load(reader(f)) 
        fn_hourly = os.path.join(datafolder,"wunderground_" +    time.strftime("%d_%m_%Y_%H_%M_") + loc + "_hourly.pkl")
        with open(fn_hourly, 'wb') as p:
            pickle.dump(parsed_json, p, pickle.HIGHEST_PROTOCOL)
        print (parsed_json['location']['city'] + ' 10 days downloaded')
        time.sleep(10)
        
    #hourly data
    # example url: http://api.wunderground.com/api/944b3f3c879d2394/geolookup/hourly/q/Germany/Berlin.json
        f = urllib.request.urlopen('http://api.wunderground.com/api/944b3f3c879d2394/geolookup/hourly/q/Germany/'+loc+'.json')
        reader = codecs.getreader('utf-8') #how is data encoded? 
        parsed_json = json.load(reader(f)) 
        fn_10days = os.path.join(datafolder,"wunderground_" +    time.strftime("%d_%m_%Y_%H_%M_") + loc + "_10days.pkl")
        with open(fn_10days, 'wb') as p:
            pickle.dump(parsed_json, p, pickle.HIGHEST_PROTOCOL)
        print (parsed_json['location']['city'] + '  hourly downloaded')
        time.sleep(10)
    f.close()
    

def main():
    print('entered main')
    download('./test/')
    print("done")


if __name__ == "__main__":
    main()
