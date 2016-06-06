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
plt.rc('axes',prop_cycle=cycler('color',['#5DBA42', '#42BAB2', '#E24A33',
                                    '#777777', '#348ABD', '#FBC15E', '#E27533']))
mpl.rcParams['font.size'] = 20
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
    resolved_msgs = msg_group[msg_group['status']=='resolved']
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
                         
df_resp = df_messages.groupby('request_id').apply(compute_response_time)
df_resp['days'] = df_resp['response_time'].dt.days

                         
#%%
state_slug = '_rheinland'

def generate_response_time_stats(state_name,state_slug):
    is_state = df_requests['jurisdiction'] == state_name
                   
    state_req_ids = df_requests.loc[is_state & is_complete,'id']
    is_state_msg = df_messages['request_id'].isin(state_req_ids.tolist())
    
    df_state_msgs = df_messages[is_state_msg]
    msgs_grouped = df_state_msgs.groupby('request_id')
    
    msg_resp_times = msgs_grouped.apply(compute_response_time)
    msg_resp_times_resolved = msg_resp_times[msg_resp_times['status']=='resolved'][['public_body','response_time']]
    msg_resp_times_resolved['days'] = msg_resp_times_resolved['response_time'].dt.days
    
    resp_times_by_pbody = msg_resp_times_resolved.groupby('public_body')['days'].agg({'avg_response_time':np.mean,\
                                                                    'n_requests':np.size})
    resp_times_by_pbody.sort_values('avg_response_time',ascending=False,inplace=True)
    resp_times_by_pbody.iloc[0:15]['avg_response_time'].plot(kind='barh')
    plt.xlabel('Tage')
    plt.legend([])
    plt.title('Durchschnittliche Antwortzeiten')
    plt.savefig(figures_path+'response_times'+state_slug+'.png', bbox_inches='tight',dpi=120)
    plt.close()
    
    writer = ExcelWriter(files_path + 'response_times_per_pbody'+state_slug+'.xlsx')
    resp_times_by_pbody.to_excel(writer)
    writer.save()
    
    writer = ExcelWriter(files_path + 'response_times_raw'+state_slug+'.xlsx')
    msg_resp_times_resolved.to_excel(writer)
    writer.save()
    
#%%
state_names = ['Baden-Württemberg', 'Bayern', 'Berlin', \
             'Brandenburg', 'Bremen', 'Hamburg', 'Hessen',\
             'Mecklenburg-Vorpommern', 'Niedersachsen',\
             'Nordrhein-Westfalen', 'Rheinland-Pfalz',\
             'Saarland', 'Sachsen', 'Sachsen-Anhalt',\
             'Schleswig-Holstein', 'Thüringen']
state_slugs = ['_BadenW', '_Bayern', '_Berlin', \
             '_Brandenburg', '_Bremen', '_Hamburg', '_Hessen',\
             '_MecklenburgV', '_NiederS',\
             '_Nordrhein', '_Rheinland',\
             '_Saarland', '_Sachsen', '_SachsenA',\
             '_SchleswigH', '_Thueringen']
             
for (state_name,state_slug) in zip(state_names,state_slugs):
    print(state_name,state_slug)
    generate_response_time_stats(state_name,state_slug)

