# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 17:37:41 2016

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
request_example = datasets[0]['objects'][0]
keys = list(request_example.keys())
keys.remove('messages')
request_example.pop('messages')
dataframe = pd.DataFrame(request_example,columns = keys)

for data_decoded in datasets:
    rlist = data_decoded['objects']
    tempDf = pd.DataFrame(rlist,columns = keys)
    dataframe = dataframe.append(tempDf, ignore_index = True)

#%% add columns juris_rank and pbody_class
dataframe['juris_rank'] = dataframe['jurisdiction'].map(pbody_juris_rank)
dataframe['pbody_class'] = dataframe['public_body'].map(pbody_classes)

#%% replace uri's with actual names of jurisdictions and public bodies
dataframe['jurisdiction'] = dataframe['jurisdiction'].map(pbody_juris)
dataframe['public_body'] = dataframe['public_body'].map(pbody_names)

#%% add outcome categorical column which includes all resolutions and the 
#   status asleep and replace english with german names

dataframe['completed_as'] = dataframe['resolution']
dataframe.ix[dataframe['status']=='asleep','completed_as'] = 'asleep'
dataframe['completed_as'] = dataframe['completed_as'].astype('category')

outcome_order = ['successful','partially_successful', 'refused',
                 'not_held', 'asleep', 'user_withdrew', 'user_withdrew_costs','']
outcomes_german = ['Erfolgreich','Teilweise erfolgreich','Abgelehnt',
                   'Info nicht vorhanden', 'Eingeschlafen',
                   'Zurückgezogen', 'Zurückgezogen wegen Kosten','']
dataframe['completed_as'].cat.reorder_categories(outcome_order,ordered=True,
                                                 inplace=True)
dataframe['completed_as'].cat.rename_categories(outcomes_german,inplace=True)

#%% create filters for dataframe

is_unique = dataframe['same_as'].isnull()
is_complete = (dataframe['status']=='asleep') | \
                         (~(dataframe['resolution']==''))
is_highrank = dataframe['juris_rank'] < 3
is_highbody = dataframe['pbody_class'] == 'Oberste Bundesbehörde'
whout_potsdam = ~(dataframe['public_body'] == 'Stadtverwaltung Potsdam')
is_chancellor = dataframe['public_body'] == 'Bundeskanzleramt'
            
#%% create different dataframes
            
# filter by jurisdictions
df_uniq_highrank = dataframe[is_unique & is_complete & is_highrank]
df_nonuniq_highrank = dataframe[is_complete & is_highrank]
df_sames_highrank = dataframe[~is_unique & is_complete & is_highrank]
highrank_sames = len(df_sames_highrank['same_as'].unique())

# filter by public bodies
df_uniq_highbody = dataframe[is_unique & is_complete & is_highbody]
df_nonuniq_highbody = dataframe[is_complete & is_highbody]
df_sames_highbody = dataframe[~is_unique & is_complete & is_highbody]
pbody_sames = len(df_sames_highrank['same_as'].unique())

# dataframes for top 10 lists
df_uniq_pbody = dataframe[is_unique & is_complete]
df_nonuniq_pbody = dataframe[is_complete]
df_uniq_pbody_whout_potsdam = dataframe[is_unique & is_complete & whout_potsdam]
df_nonuniq_pbody_whout_potsdam = dataframe[is_complete & whout_potsdam]

# dataframes only with chancellor house as public body
df_chancellor_uniq = dataframe[is_unique & is_complete & is_chancellor]
df_chancellor_nonuniq = dataframe[is_complete & is_chancellor]
                                           

#%% put dataframes and according titles in lists
                                           
df_juris_list = [df_uniq_highrank, df_nonuniq_highrank, df_sames_highrank]
juris_df_titles = ['Oberste Verwaltungsebenen (ohne Massenanfragen)',\
                   'Oberste Verwaltungsebenen (mit Massenanfragen)',\
                   'Oberste Verwaltungsebenen (nur Massenanfragen, '\
                   '%d unterschiedliche)' % highrank_sames]

df_highbody_list = [df_uniq_highbody, df_nonuniq_highbody, df_sames_highbody]
highbody_df_titles = ['Oberste Bundesbehörden (ohne Massenanfragen)',\
                   'Oberste Bundesbehörden (mit Massenanfragen)',\
                   'Oberste Bundesbehörden (nur Massenanfragen, '\
                   '%d unterschiedliche)' % pbody_sames]

df_pbody_list = [df_uniq_pbody, df_nonuniq_pbody,
                 df_uniq_pbody_whout_potsdam, df_nonuniq_pbody_whout_potsdam]
pbody_df_titles = ['Top 10 Behörden (ohne Massenanfragen)',\
                   'Top 10 Behörden (mit Massenanfragen)',\
                   'Top 10 Behörden ohne Potsdam (ohne Massenanfragen)',\
                   'Top 10 Behörden ohne Potsdam (mit Massenanfragen)']
                   
df_chancellor_list = [df_chancellor_uniq, df_chancellor_nonuniq]
chancellor_df_titles = ['Bundeskanzleramt (ohne Massenanfragen)',
                        'Bundeskanzleramt (mit Massenanfragen)']

#%% generate plots for all dataframes

for i,df in enumerate(df_juris_list):
    outcome_df = outcomes_in_columns(df,'jurisdiction','completed_as')
    outcome_df.sort_values('total',inplace=True)
    
    plot_outcomes(outcome_df, title = juris_df_titles[i],
                  filename= juris_df_titles[i], save=True)

for i,df in enumerate(df_highbody_list):
    pbody_outcome_df = outcomes_in_columns(df,'public_body','completed_as')
    pbody_outcome_df.sort_values('total',inplace=True)
    
    plot_outcomes(pbody_outcome_df, title = highbody_df_titles[i],
                  filename= highbody_df_titles[i],save=True)

# Top 10 plots (by taking only the last 10 entries)
for i,df in enumerate(df_pbody_list):
    pbody_outcome_df = outcomes_in_columns(df,'public_body','completed_as')
    pbody_outcome_df.sort_values('total',inplace=True)
    
    plot_outcomes(pbody_outcome_df[-10:-1], title = pbody_df_titles[i],
                  filename= pbody_df_titles[i],save=True)
         
# example comparison of unique vs. nonunique for chancellor house
dfs = []
for i,df in enumerate(df_chancellor_list):
    dfs.append(outcomes_in_columns(df,'public_body','completed_as'))
    
df_chanc = dfs[0].append(dfs[1])
df_chanc.index = ['Ohne Massenanfragen','Mit Massenanfragen']
    
plot_outcomes(df_chanc, title = 'Bundeskanzleramt im Vergleich',
              filename= 'Bundeskanzleramt',save=True)


#%% generate spreadsheets for jurisdictions and public bodies with rankings for 
#   single outcomes
    
outcomes = list(df_uniq_highrank['completed_as'].unique())

writer = ExcelWriter(files_path + 'jurs_by_outcomes.xlsx')

for outcome in outcomes:
    result = generate_ranked_df(dataframe,'jurisdiction','completed_as',outcome, 50)
    result.to_excel(writer,outcome)
writer.save()

writer = ExcelWriter(files_path + 'pbodies_by_outcomes.xlsx')

for outcome in outcomes:
    result = generate_ranked_df(dataframe,'public_body','completed_as',outcome, 50)
    result.to_excel(writer,outcome)
writer.save()

# total request rankings spreadsheets 
writer = ExcelWriter(files_path + 'ranked_by_requests.xlsx')
jur_reqs = rank_by_requests(dataframe,'jurisdiction')
jur_reqs.to_frame('total_requests').to_excel(writer,'jurisdiction')
pbody_reqs = rank_by_requests(dataframe,'public_body')
pbody_reqs.to_frame('total_requests').to_excel(writer,'public_body')
writer.save()

#%% how to plot cumulative sum over the years
dates = pd.to_datetime(dataframe['first_message'])
dates.groupby(dates.dt.year).size().cumsum().plot()
# barplot for requests per year
dates.groupby(dates.dt.year).size().plot(kind='bar')
                         

