# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 19:40:43 2016

@author: andrej
"""

import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
from pandas import ExcelWriter
from fds_api_pandas_functions import *
import loading

plt.style.use('ggplot')
mpl.rcParams['axes.color_cycle'] = ['#5DBA42', '#42BAB2', '#E24A33',
                                    '#777777', '#348ABD', '#FBC15E', '#E27533']
mpl.rcParams['font.size'] = 16
mpl.rcParams['axes.facecolor'] = 'white'

#%% build dict that translates from url to actual name of jurisdiction

dataframe = loading.load_messages()
    
#%% filters
    
has_attachment = dataframe['attachments'].str.len() > 0

nr_pdfs = dataframe['attachments'].str.len().sum()
    
    
    
    
    
    
    