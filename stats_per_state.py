# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 09:21:50 2016

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
is_highrank = df_requests['juris_rank'] < 3
is_highbody = df_requests['pbody_class'] == 'Oberste Bundesbehörde'

def generate_state_stats(state_name, state_slug):
    is_state = df_requests['jurisdiction'] == state_name
                   
    escalted_req_ids = df_messages.loc[df_messages['is_escalation']==True,'request_id']
    is_escalated_req = df_requests['id'].isin(escalted_req_ids.tolist())
    
    # all completed requests
    df_uniq = df_requests[is_unique & is_complete & is_state]
    
    df_req_escalated = df_requests[is_escalated_req & is_complete & is_unique & is_state]
    
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
                  filename = 'einschaltung_anfragen'+state_slug,
                  orient='vertical', text_offset = 1.01, save=True)
                  
    # save excel table of absolute values
                     
    df_all_abs = dfs_abs[0].append(dfs_abs[1])
    df_all_abs.index = ['Alle Anfragen (ohne Massenanfragen) in Prozent',
                        'Alle Anfragen (ohne Massenanfragen) absolut', 
                     'Anfragen nach Einschaltung der BfDI in Prozent',
                     'Anfragen nach Einschaltung der BfDI absolut']
    #   
    writer = ExcelWriter(files_path + 'escalation_outcomes'+state_slug+'.xlsx')
    df_all_abs.to_excel(writer)
    writer.save()
    
    #    # Top 10 plots (by taking only the last 10 entries)
    pbody_outcome_df = outcomes_in_columns(df_uniq,'public_body','completed_as')
    pbody_outcome_df.sort_values('total',inplace=True)
    top10_pbody = pbody_outcome_df[-10:]
    top10_pbody.sort_values('Erfolgreich',inplace=True)
    
    plot_outcomes(top10_pbody, title = 'Top 10 Behörden',
                  filename= 'pbody_outcomes'+state_slug,orient='horizontal',
                  text_offset = 1.01, save=True)
                      
    # generate spreadsheets for jurisdictions and public bodies with rankings for 
    #   single outcomes
        
    outcomes = list(df_requests['completed_as'].unique())
    
    writer = ExcelWriter(files_path + 'pbodies_by_outcomes_unique_requests_min1'+state_slug+'.xlsx')
    
    for outcome in outcomes:
        result = generate_ranked_df(df_uniq[is_unique],'public_body','completed_as',outcome, 1)
        result.to_excel(writer,outcome)
    writer.save()
    
    writer = ExcelWriter(files_path + 'pbodies_by_outcomes_unique_requests_min4'+state_slug+'.xlsx')
    
    for outcome in outcomes:
        result = generate_ranked_df(df_uniq[is_unique],'public_body','completed_as',outcome, 4)
        result.to_excel(writer,outcome)
    writer.save()
    
    # total request rankings spreadsheets 
    writer = ExcelWriter(files_path + 'ranked_by_requests'+state_slug+'.xlsx')
    pbody_reqs = rank_by_requests(df_uniq,'public_body')
    pbody_reqs.to_frame('total_requests').to_excel(writer,'public_body')
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
             '_Mecklenburg-Vorpommern', '_NiederS',\
             '_Nordrhein', '_Rheinland',\
             '_Saarland', '_Sachsen', '_SachsenA',\
             '_SchleswigH', '_Thueringen']
             
for (state_name,state_slug) in zip(state_names,state_slugs):
    print(state_name,state_slug)
    generate_state_stats(state_name,state_slug)
