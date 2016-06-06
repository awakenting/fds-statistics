# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 12:12:28 2016

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

mpl.rcParams['font.size'] = 28
mpl.rcParams['axes.facecolor'] = 'white'

files_path = './data/'
figures_path = './figures/'
#%% load data from files
df_requests = loading.load_requests()

df_messages = loading.load_messages()

#%% create filters for dataframe
is_unique = df_requests['same_as'].isnull()
is_complete = (df_requests['status']=='asleep') | \
               (~(df_requests['resolution']==''))



def compute_response_time(msg_group):
    first_msg = pd.to_datetime(msg_group.iloc[0]['timestamp'])
    resolved_list = ['resolved', 'refused', 'successful',
       'not_held', 'partially_successful', 'request_redirected',
       'user_withdrew_costs', 'user_withdrew']
    is_resolved = msg_group['status'].isin(resolved_list)
    resolved_msgs = msg_group[is_resolved]
    pbody = msg_group.iloc[0]['public_body']
    if not len(resolved_msgs) < 1:
        resolved_on = pd.to_datetime(resolved_msgs.iloc[0]['timestamp'])
        resp_time = resolved_on - first_msg
        status = 'resolved'
    else:
        resp_time = pd.datetime.today() - first_msg
        status = msg_group.iloc[-1]['status']        
    return pd.DataFrame([{'n_messages' : len(msg_group),
                         'response_time' : resp_time,
                         'status' : status,
                         'public_body':pbody}])
                         
#%%
                         
df_resp = df_messages.groupby('request_id',as_index=False).apply(compute_response_time)
df_resp['days'] = df_resp['response_time'].dt.days
df_resp_reso = df_resp[df_resp['status']=='resolved']

#%% plot
resp_plot = df_resp_reso['days'].plot.hist(bins=300,use_index=False,figsize=(28,24))
plt.plot([30,30],[0,500],'r--',lw=4)
resp_plot.text(30,550, 'Legal time limit (1 Month)',ha='center', va='center')
plt.xlim([0,100])
plt.xlabel('Response time in days')
plt.ylabel('Number of requests')
plt.title('Response time of ' + str(int(len(df_resp_reso))) + ' completed requests')
plt.savefig(figures_path+'response_times_all_en.png', bbox_inches='tight',dpi=300)
plt.close()

                         
