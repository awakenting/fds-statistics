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

plt.style.use('ggplot')
mpl.rcParams['axes.color_cycle'] = ['#5DBA42', '#42BAB2', '#E24A33',
                                    '#777777', '#348ABD', '#FBC15E', '#E27533']
mpl.rcParams['font.size'] = 16
mpl.rcParams['axes.facecolor'] = 'white'


datasets = np.load('request_data_until_10083.npy')
data_juris = np.load('jurisdictions.npy')[0]
data_pbodies = np.load('public_bodies.npy')

#%% build dict that translates from url to actual name of jurisdiction
juri_names = {}
for jur in data_juris['objects']:
    juri_names[jur['resource_uri']] = jur['name']

# with juris from public bodies
pbody_juris = {}
pbody_juris_rank = {}
pbody_names = {}
pbody_classes = {}
for patch in data_pbodies:
    for pbody in patch:
        if not pbody['jurisdiction']['resource_uri'] in pbody_juris:
            pbody_juris[pbody['jurisdiction']['resource_uri']] =\
                                                  pbody['jurisdiction']['name']
            
        if not pbody['jurisdiction']['resource_uri'] in pbody_juris_rank:
            pbody_juris_rank[pbody['jurisdiction']['resource_uri']] = \
                                                  pbody['jurisdiction']['rank']

        if not pbody['resource_uri'] in pbody_names:
            pbody_names[pbody['resource_uri']] = pbody['name']            

        if not pbody['resource_uri'] in pbody_classes:
            pbody_classes[pbody['resource_uri']] = pbody['classification']

#%% create dataframe 
message_example = datasets[0]['objects'][0]['messages'][0]
keys = list(message_example.keys())
keys.remove('content')
message_example.pop('content')
#dataframe = pd.DataFrame(message_example,columns = keys)

for i,data_decoded in enumerate(datasets):
    message_list = []
    [message_list.extend(request['messages']) for request in data_decoded['objects']]
    if i == 0:
        dataframe = pd.DataFrame(message_list,columns = keys)
    else:
        tempDf = pd.DataFrame(message_list,columns = keys)
        dataframe = dataframe.append(tempDf, ignore_index = True)
    
#%% filters
    
has_attachment = dataframe['attachments'].str.len() > 0

nr_pdfs = dataframe['attachments'].str.len().sum()
    
    
    
    
    
    
    