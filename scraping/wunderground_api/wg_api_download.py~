import urllib.request
import json
import codecs

f = urllib.request.urlopen('http://api.wunderground.com/api/944b3f3c879d2394/geolookup/conditions/q/IA/Cedar_Rapids.json')
#need to convert byte object to string
reader = codecs.getreader('utf-8')
parsed_json = json.load(reader(f))
location = parsed_json['location']['city']
temp_f = parsed_json['current_observation']['temp_f']
print ("Current temperature in %s is: %s" % (location, temp_f))
f.close()
