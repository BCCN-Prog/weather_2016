import urllib.request
import json
import codecs
import pickle

#f = urllib.request.urlopen('http://api.wunderground.com/api/944b3f3c879d2394/geolookup/forecast10day/q/IA/Cedar_Rapids.json')

loc_list = ['Berlin', 'Munich', 'Hamburg', 'Cologne', 'Frankfurt', 'Stuttgart', 'Bremen', 'Leipzig', 'Hannover', 'Nuremberg', 'Dortmund', 'Dresden', 'Kassel', 'Kiel', 'Bielefeld', 'Saarbruecken', 'Rostock', 'Freiburg', 'Erfurt', 'Magdeburg']

#download daily 10 day forecast
for loc in loc_list:
    f = urllib.request.urlopen('http://api.wunderground.com/api/944b3f3c879d2394/geolookup/forecast10day/q/Germany/'+loc+'.json')
    #need to convert byte object to string
    print (type(f))
    reader = codecs.getreader('utf-8') #how is data encoded? 
    parsed_json = json.load(reader(f)) #
    print (parsed_json['location']['city'])
    
#
with open('try_Berlin.pkl', 'wb') as p:
    pickle.dump(parsed_json, p, pickle.HIGHEST_PROTOCOL)
print ('Done')
print (parsed_json['location']['city'])
#echo (parsed_json | python -m json.tool())
    
#print (parsed_json)
#location = parsed_json['location']['city']
#temp_f = parsed_json['current_observation']['temp_f']
#print ("Current temperature in %s is: %s" % (location, temp_f))
f.close()
