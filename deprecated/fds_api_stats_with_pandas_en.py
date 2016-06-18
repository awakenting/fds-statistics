# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 17:37:41 2016

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
mpl.rcParams['font.size'] = 24
mpl.rcParams['axes.facecolor'] = 'white'



#%% load data from files
dataframe = loading.load_requests()

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

df_all_list = [df_uniq, df_nonuniq]
df_all_titles = ['All requests',
                 'All requests (with mass requests)']
                                           
df_juris_list = [df_uniq_highrank, df_nonuniq_highrank, df_sames_highrank]
juris_df_titles = ['Bund und Bundesländer',\
                   'Oberste Verwaltungsebenen (mit Massenanfragen)',\
                   'Oberste Verwaltungsebenen (nur Massenanfragen, '\
                   '%d unterschiedliche)' % highrank_sames]

df_highbody_list = [df_uniq_highbody, df_nonuniq_highbody, df_sames_highbody]
highbody_df_titles = ['Oberste Bundesbehörden',\
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

#%% dictionaries with abbreviations for bundesländer and bundesministerien

juris_map = {'Baden-Württemberg':'BW', 'Bayern':'BY', 'Berlin':'BE', \
             'Brandenburg':'BB', 'Bremen':'HB', 'Bund':'Bund', 'Hamburg':'HH',\
             'Hessen':'HE', 'Mecklenburg-Vorpommern':'MV', 'Niedersachsen':'NI',\
             'Nordrhein-Westfalen':'NW', 'Rheinland-Pfalz':'RP',\
             'Saarland':'SL', 'Sachsen':'SN', 'Sachsen-Anhalt':'ST',\
             'Schleswig-Holstein':'SH', 'Thüringen':'TH'}

highbody_map =  {  'Auswärtiges Amt':'AA',
                   'Beauftragte der Bundesregierung für Kultur und Medien':'BfKM',
                   'Bundeskanzleramt':'BK',
                   'Bundesministerium der Finanzen':'BMF',
                   'Bundesministerium der Justiz und für Verbraucherschutz':'BMJV',
                   'Bundesministerium der Verteidigung':'BMVg',
                   'Bundesministerium des Innern':'BMI',
                   'Bundesministerium für Arbeit und Soziales':'BMAS',
                   'Bundesministerium für Bildung und Forschung':'BMBF',
                   'Bundesministerium für Ernährung und Landwirtschaft':'BMEL',
                   'Bundesministerium für Familie, Senioren, Frauen und Jugend':'BMFSFJ',
                   'Bundesministerium für Gesundheit':'BMG',
                   'Bundesministerium für Umwelt, Naturschutz, Bau und Reaktorsicherheit':'BMUB',
                   'Bundesministerium für Verkehr und digitale Infrastruktur':'BMVI',
                   'Bundesministerium für Wirtschaft und Energie':'BMWi',
                   'Bundesministerium für wirtschaftliche Zusammenarbeit und Entwicklung':'BMZ',
                   'Bundespräsidialamt':'BPräA',
                   'Bundesrechnungshof':'BRH',
                   'Presse- und Informationsamt der Bundesregierung':'PA'}

#%% generate plots for all dataframes
for i,df in enumerate([df_uniq_highrank]):
    outcome_df = outcomes_in_columns(df,'jurisdiction','completed_as')
    outcome_df.sort_values('total',inplace=True)
    # letzten 5 bundesländer haben zu wenig anfragen
    df_cutted = outcome_df[-12:]
    df_cutted.sort_values('Erfolgreich', inplace=True)
    #df_cutted.rename(index=juris_map,inplace=True)
    
    new_index = (5,0,1,2,3,4,6,7,8,9,10,11)
    df_new = df_cutted.iloc[new_index,:]
    plot_outcomes(df_new, title = juris_df_titles[i],
                  filename= juris_df_titles[i],orient='vertical',
                  p_ticklabels=df_new.index.tolist(), save=True)
    
#%%
for i,df in enumerate(df_highbody_list):
    pbody_outcome_df = outcomes_in_columns(df,'public_body','completed_as')
    pbody_outcome_df.sort_values('total',inplace=True)
    top10_pbody = pbody_outcome_df[-10:]
    top10_pbody.sort_values('Erfolgreich',inplace=True)
    top10_pbody.rename(index=highbody_map,inplace=True)
    
    plot_outcomes(top10_pbody, title = highbody_df_titles[i],
                  filename= highbody_df_titles[i],orient='vertical',save=True)
    
#%%    # Top 10 plots (by taking only the last 10 entries)
for i,df in enumerate(df_pbody_list):
    pbody_outcome_df = outcomes_in_columns(df,'public_body','completed_as')
    pbody_outcome_df.sort_values('total',inplace=True)
    top10_pbody = pbody_outcome_df[-10:]
    top10_pbody.sort_values('Erfolgreich',inplace=True)
    top10_pbody.rename(index=highbody_map,inplace=True)
    
    plot_outcomes(top10_pbody, title = pbody_df_titles[i],
                  filename= pbody_df_titles[i],orient='vertical',save=True)
   
#%%          
    # example comparison of unique vs. nonunique for chancellor house
#    dfs = []
#    for i,df in enumerate(df_chancellor_list):
#        dfs.append(outcomes_in_columns(df,'public_body','completed_as'))
#        
#    df_chanc = dfs[0].append(dfs[1])
#    df_chanc.index = ['Ohne Massenanfragen','Mit Massenanfragen']
#        
#    plot_outcomes(df_chanc, title = 'Bundeskanzleramt im Vergleich',
#                  filename= 'Bundeskanzleramt',save=True)
                  

#%%
dfs = []
for i,df in enumerate(df_all_list):
    dfout = df.groupby('completed_as').size()
    dfout = dfout/dfout.sum()*100
    df_outcomes = pd.DataFrame(columns=dfout.index.get_values())
    df_outcomes = df_outcomes.append(dfout,ignore_index=True)
    df_outcomes[''] = df.groupby('completed_as').size().sum()
    dfs.append(df_outcomes)
        
df_all = dfs[0].append(dfs[1])
df_all.index = ['Ohne Massenanfragen','Mit Massenanfragen']
cols = df_all.columns.tolist()
last = [cols[-1]]
last.extend(cols[0:-1])
plot_outcomes(df_all[last], title = '', 
              filename = 'alle_anfragen',orient='vertical', save=True)


#%% only for uniq requests              
dfout = df_uniq.groupby('completed_as').size()
dfout = dfout/dfout.sum()*100
df_outcomes = pd.DataFrame(columns=dfout.index.get_values())
df_outcomes = df_outcomes.append(dfout,ignore_index=True)
df_outcomes[''] = df.groupby('completed_as').size().sum()
df_outcomes.index = ['']
cols = df_outcomes.columns.tolist()
last = [cols[-1]]
last.extend(cols[0:-1])
plot_outcomes(df_outcomes[last], title = '', 
              filename = 'all_requests_unique',orient='vertical',
              text_offset=1.05, include_descriptions=True, save=True)


#%% generate spreadsheets for jurisdictions and public bodies with rankings for 
#   single outcomes
    
outcomes = list(df_uniq_highrank['completed_as'].unique())

writer = ExcelWriter(files_path + 'jurs_by_outcomes.xlsx')

for outcome in outcomes:
    result = generate_ranked_df(dataframe,'jurisdiction','completed_as',outcome, 50)
    result.to_excel(writer,outcome)
writer.save()

writer = ExcelWriter(files_path + 'pbodies_by_outcomes_unique_requests_min20.xlsx')

for outcome in outcomes:
    result = generate_ranked_df(dataframe[is_unique],'public_body','completed_as',outcome, 20)
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
dates = pd.to_datetime(dataframe.loc[is_unique,'first_message'])
#dates.groupby(dates.dt.year).size().cumsum().plot()
# barplot for requests per year
g_dates = dates.groupby([dates.dt.weekofyear]).size()
g_dates.plot(kind='bar', stacked=True,rot=0)
                         

