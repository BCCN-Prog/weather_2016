"""
Python script to download all html files from all providers.
Import all providers you want to download from and call their download() function to start the downloads.
If you want to add a new provider, import it AND add it to provider_list.
"""

import os

import accuweather
import wetter_com
import owm
import wetter_de

provider_list = [wetter_com, 
                 owm, 
                 wetter_de,
                 accuweather]

data_path = './data/'

if not os.path.exists(data_path):
    os.makedirs(data_path)

for provider in provider_list:
    print('RUNNING', provider)
    try:
        provider.download(data_path)
    except:
        err = sys.exc_info()[0]
        print('Excepted error in {}.\n\n{}'.format(provider, err))
