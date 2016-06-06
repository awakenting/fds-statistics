# -*- coding: utf-8 -*-
"""
Created on Fri May 20 10:44:33 2016

@author: andrej
"""

import os
import matplotlib.pyplot as plt
import matplotlib as mpl
from cycler import cycler
import numpy as np
import pandas as pd
from pandas import ExcelWriter
from fds_api_pandas_functions_en import *
import loading

plt.style.use('ggplot')
#mpl.rcParams['axes.color_cycle'] = ['#5DBA42', '#42BAB2', '#E24A33',
#                                    '#777777', '#348ABD', '#FBC15E', '#E27533']
mpl.rcParams['axes.prop_cycle'] = cycler('color',['#5DBA42', '#42BAB2', '#E24A33',
                                    '#777777', '#348ABD', '#FBC15E', '#E27533'])
mpl.rcParams['font.size'] = 32
mpl.rcParams['axes.facecolor'] = 'white'

#%% load data from files
dataframe = loading.load_requests(translate_to_german=False)

#%% create filters for dataframe
is_unique = dataframe['same_as'].isnull()
is_complete = (dataframe['status']=='asleep') | \
                         (~(dataframe['resolution']==''))
is_highrank = dataframe['juris_rank'] < 3
is_highbody = dataframe['pbody_class'] == 'Oberste Bundesbehörde'
whout_potsdam = ~(dataframe['public_body'] == 'Stadtverwaltung Potsdam')
is_chancellor = dataframe['public_body'] == 'Bundeskanzleramt'
            
#%% create different dataframes
            
# all completed requests
df_uniq = dataframe[is_unique & is_complete]
df_nonuniq = dataframe[is_complete]

#%% only for uniq requests              
dfout = df_uniq.groupby('completed_as').size()
dfout = dfout/dfout.sum()*100
df_outcomes = pd.DataFrame(columns=dfout.index.get_values())
df_outcomes = df_outcomes.append(dfout,ignore_index=True)
df_outcomes[''] = df_uniq.groupby('completed_as').size().sum()
df_outcomes.index = ['']
cols = df_outcomes.columns.tolist()
last = [cols[-1]]
last.extend(cols[0:-1])
plot_outcomes(df_outcomes[last], title = 'Overall requests', 
              filename = 'all_requests_unique',orient='vertical',
              text_offset=1.05, include_descriptions=False, save=True)