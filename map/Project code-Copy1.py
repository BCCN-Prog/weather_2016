
# coding: utf-8

# In[15]:

import numpy as np
import pandas as pd


#Modify the text file with coordinates into a format more easily accessible to load into a panda dataframe
with open('KL_Tageswerte_Beschreibung_Stationen3.txt', 'r', encoding='ISO-8859-1') as ro, \
   open('coordinates.txt', 'a') as rw: #create a new file with the name coordinated
     for line in ro.readlines():
       #Stations_id=line[0:11] #define where to split the string of information based on number of characters
       #von_datum=line[12:20]
       #bis_datum=line[21:29]
       #Stationshoehe=line[30:44]
       geoBreite=line[45:56]
       geoLaenge=line[57:66]
       #Stationsname=line[67:108]
       #Bundesland=line[108:]        #Stations_id_strip=Stations_id.strip() #remove space before and after the value
       #von_datum_strip=von_datum.strip()
       #bis_datum_strip=bis_datum.strip()
       #Stationshoehe_strip=Stationshoehe.strip()
       geoBreite_strip=geoBreite.strip()
       geoLaenge_strip=geoLaenge.strip()
       #Stationsname_strip=Stationsname.strip()
       #Bundesland_strip=Bundesland.strip()
       
seq = (geoBreite_strip,geoLaenge_strip)        #seq = (Stations_id_strip, von_datum_strip,bis_datum_strip,Stationshoehe_strip,geoBreite_strip,geoLaenge_strip,Stationsname_strip,Bundesland_strip)
rw.write(';'.join(seq) + '\n') #write a new file with the different columns joined but separated with a :wink:
       
stations_temp=pd.read_table('coordinates.txt', sep=';') #read the newly created date file
coord=stations_temp.ix[1:] # remove the first row
coord
