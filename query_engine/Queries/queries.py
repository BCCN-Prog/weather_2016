# -*- coding: utf-8 -*-
"""
Created on Tue May 31 16:05:09 2016

@author: pythonproject
"""
##%%
import QueryEngine as qe

import pandas as pd
import numpy as np


##%%
choices = {1:'Heat map of Germany', 2: 'adafs'}

print('Please enter one of the following choices:')
for i in choices: print(i, choices[i])

userchoice = input()

if userchoice == '1':
    # heat map of Germany
    date = input('Please enter a date (YYYYMMDD):')
    qe.extract_heatmap()
    
elif userchoice == '2':
    print('blah!')