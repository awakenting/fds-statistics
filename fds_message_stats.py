# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 10:02:53 2016

@author: andrej
"""

import os
import matplotlib.pyplot as plt
import matplotlib as mpl
from cycler import cycler
import numpy as np
import pandas as pd
from pandas import ExcelWriter
from fds_api_pandas_functions import *
import loading

plt.style.use('ggplot')
# for matplotlib versions below 1.5:
#mpl.rcParams['axes.color_cycle'] = ['#5DBA42', '#42BAB2', '#E24A33',
#                                    '#777777', '#348ABD', '#FBC15E', '#E27533']
mpl.rcParams['axes.prop_cycle'] = cycler('color',['#5DBA42', '#42BAB2', '#E24A33',
                                    '#777777', '#348ABD', '#FBC15E', '#E27533'])
plt.rc('axes',prop_cycle=cycler('color',['#5DBA42', '#42BAB2', '#E24A33',
                                    '#777777', '#348ABD', '#FBC15E', '#E27533']))
mpl.rcParams['font.size'] = 20
mpl.rcParams['axes.facecolor'] = 'white'

files_path = './data/'

#%% load data from files
df_requests = loading.load_requests()

df_messages = loading.load_messages()

#%% create filters for dataframe
is_unique = df_requests['same_as'].isnull()
is_complete = (df_requests['status']=='asleep') | \
               (~(df_requests['resolution']==''))
               
escalted_req_ids = df_messages.loc[df_messages['is_escalation']==True,'request_id']
is_escalated_req = df_requests['id'].isin(escalted_req_ids.tolist())

# all completed requests
df_uniq = df_requests[is_unique & is_complete]

df_req_escalated = df_requests[is_escalated_req & is_complete & is_unique]


df_esc_list = [df_uniq, df_req_escalated]
df_esc_titles = ['Alle Anfragen (ohne Massenanfragen)',
                 'Anfragen nach Einschaltung der BfDI']
      
dfs = []
dfs_abs = []
for i,df in enumerate(df_esc_list):
    dfout = df.groupby('completed_as').size()
    dfout_rel = dfout/dfout.sum()*100
    df_outcomes = pd.DataFrame(columns=dfout_rel.index.get_values())
    df_outcomes = df_outcomes.append(dfout_rel,ignore_index=True)
    df_outcomes[''] = df.groupby('completed_as').size().sum()
    dfs.append(df_outcomes)
    
    df_outcomes_abs = pd.DataFrame(columns=dfout.index.get_values())
    df_outcomes_abs = df_outcomes.append(dfout,ignore_index=True)
    df_outcomes_abs[''] = df.groupby('completed_as').size().sum()
    dfs_abs.append(df_outcomes_abs)
    

    
df_all = dfs[0].append(dfs[1])
df_all.index = ['Alle Anfragen (ohne Massenanfragen)',
                 'Anfragen nach Einschaltung der Beauftragten']
                 
cols = df_all.columns.tolist()
last = [cols[-1]]
last.extend(cols[0:-1])
plot_outcomes(df_all[last], title = 'Beauftragten für Datenschutz und Informationsfreiheit',
              filename = 'einschaltung_anfragen',
              orient='vertical', text_offset = 1.01, save=True)
              
#%% only for uniq requests              
dfout = df_req_escalated.groupby('completed_as').size()
dfout = dfout/dfout.sum()*100
df_outcomes = pd.DataFrame(columns=dfout.index.get_values())
df_outcomes = df_outcomes.append(dfout,ignore_index=True)
df_outcomes[''] = df.groupby('completed_as').size().sum()
df_outcomes.index = ['']
cols = df_outcomes.columns.tolist()
last = [cols[-1]]
last.extend(cols[0:-1])
plot_outcomes(df_outcomes[last], title = 'Beauftragten für Datenschutz und Informationsfreiheit', 
              filename = 'einschaltung_anfragen_unique',orient='vertical',
              text_offset=1.05, include_descriptions=False, save=True)
              
#%% save excel table of absolute values
                 
df_all_abs = dfs_abs[0].append(dfs_abs[1])
df_all_abs.index = ['Alle Anfragen (ohne Massenanfragen) in Prozent',
                    'Alle Anfragen (ohne Massenanfragen) absolut', 
                 'Anfragen nach Einschaltung der BfDI in Prozent',
                 'Anfragen nach Einschaltung der BfDI absolut']
                 #%%
cfiles_path = './data/'

writer = ExcelWriter(files_path + 'escalation_outcomes.xlsx')
df_all_abs.to_excel(writer)
writer.save()


