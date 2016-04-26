"""
Python script to download all html files from all providers.
Import all providers you want to download from and call their download() function to start the downloads.
"""

import os

import wetter_com
import owm
import wetter_de

data_path = './data/'

if not os.path.exists(data_path):
    os.makedirs(data_path)

wetter_com.download(data_path)
owm.download(data_path)
wetter_de.download(data_path)
