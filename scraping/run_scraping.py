"""
Python script to download all html files from all providers.
Import all providers you want to download from and call their download() function to start the downloads.
"""

import wetter_com

data_path = './data/'
wetter_com.download(data_path)
