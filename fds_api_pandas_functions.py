# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 16:13:41 2016

@author: andrej
"""

import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd

files_path = '/home/andrej/Dokumente/OpenKnowledge/FragDenStaat/'

#%% functions

def outcomes_in_columns(df,authority_level,column):
    auths = df.groupby([authority_level,column],as_index=False).size()
    auth_groups = auths.groupby(level=authority_level)
    auth_totals = auth_groups.apply(sum)
    result = pd.DataFrame(auth_totals,columns=['total'])
    current_keys = list(result.columns)
    auths_in_percent = auths/auth_totals*100
    for column_value in list(auths_in_percent.index.levels[1]):
        auths_by_column_value = auths_in_percent.xs(column_value,level=column)
        current_keys.append(column_value)
        result = pd.concat([result,auths_by_column_value],axis = 1)
    result.set_axis(1,current_keys)
    result.fillna(0,inplace=True)
    return result

def plot_outcomes(outcome_df, title, filename, save=False):
    barh = outcome_df.ix[:,1:].plot(kind='barh',stacked=True,figsize=(18,14))
    barh.xaxis.set_tick_params(top='off')
    barh.yaxis.set_tick_params(right='off')
    barh.xaxis.set_ticks(np.arange(0,101,10))
    barh.xaxis.set_ticklabels(np.arange(0,101,10))
    
    lgd = plt.legend(loc='lower left', bbox_to_anchor=(0.0,-0.2,1.0,0.1),ncol=3,
                     mode='expand', borderaxespad=0.)
    plt.xlim((0,100))
    plt.xlabel('Anteil an abgeschlossenen Anfragen in Prozent')
    plt.title(title)
    
    for i in range(len(outcome_df)):
        barh.text(105, i,
                    '%d' % int(outcome_df.ix[:,0].values[i]),
                    ha='center', va='center')
    texts = barh.text(105, len(outcome_df)-0.5,'Jeweilige Gesamtanzahl',
              ha='center',va='bottom')
    
    if save:
        plt.savefig(files_path+filename+'.png',
                    bbox_extra_artists=[lgd,texts], bbox_inches='tight',dpi=180)
        plt.close()

#%% 
# get top juris for percentage refused with over 100 requests

def generate_ranked_df(df,authority_level, column, column_value, min_requests):
    auths = df.groupby([authority_level,column],as_index=False).size()
    auth_groups = auths.groupby(level=authority_level)
    auth_totals = auth_groups.apply(sum)
    auths_in_percent = auths/auth_totals*100
    auths_by_column_value = auths_in_percent.xs(column_value,level=column)
    criterion_mask = auth_totals > min_requests
    auths_valid = auths_by_column_value[criterion_mask]
    result = pd.concat([auths_valid, auth_totals[criterion_mask]],\
                                    keys=['Percentage_'+column_value,'Total number'], axis=1)
                                           
    result.sort(columns=['Percentage_'+column_value],inplace=True,ascending=False)
    result.fillna(0,inplace=True)
    result = result.round(decimals= {'Percentage_'+column_value:2})
    return result
    
#%% rank by number of requests

def rank_by_requests (df,authority_level):
    auths = df.groupby(authority_level,as_index=False).size().sort_values(ascending=False)
    return auths