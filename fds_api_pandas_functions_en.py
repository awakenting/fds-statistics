# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 16:13:41 2016

@author: andrej
"""

import os
import matplotlib.pyplot as plt
import matplotlib as mpl
from cycler import cycler
#mpl.rcParams['axes.color_cycle'] = ['#5DBA42', '#42BAB2', '#E24A33',
#                                    '#777777', '#348ABD', '#FBC15E', '#E27533']
#mpl.rcParams['axes.prop_cycle'] = cycler('color',['#5DBA42', '#42BAB2', '#E24A33',
#                                    '#777777', '#348ABD', '#FBC15E', '#E27533'])                            
import numpy as np
import pandas as pd

files_path = './figures/'

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
    
def outcomes_in_columns_single(df,column):
    auths = df.groupby(column,as_index=False).size()
    result = pd.DataFrame(auths,columns='total')
    current_keys = list(auths.columns)
    auths_in_percent = auths/auths.sum()*100
    for column_value in list(auths_in_percent.index.levels[1]):
        auths_by_column_value = auths_in_percent.xs(column_value,level=column)
        current_keys.append(column_value)
        result = pd.concat([result,auths_by_column_value],axis = 1)
    result.set_axis(1,current_keys)
    result.fillna(0,inplace=True)
    return result

def plot_outcomes(outcome_df, title, filename, orient='horizontal',
                  text_offset=1.2, p_ticklabels=None,
                  include_descriptions=True, save=False):
    if orient == 'horizontal':    
        barh = outcome_df.ix[:,1:].plot(kind='barh',stacked=True,figsize=(18,14))
        barh.xaxis.set_tick_params(top='off')
        barh.yaxis.set_tick_params(right='off')
        barh.xaxis.set_ticks(np.arange(0,101,10))
        barh.xaxis.set_ticklabels(np.arange(0,101,10))
        
        lgd = plt.legend(loc='lower left', bbox_to_anchor=(0.0,-0.2,1.0,0.1),ncol=3,
                         mode='expand', borderaxespad=0.)
        plt.xlim((0,100))
        plt.xlabel('Percentage of completed requests')
        barh.grid(b=True, which='major', color=[0.5,0.5,0.5], linestyle='-')
        title_artist = plt.title(title)
        
        for i in range(len(outcome_df)):
            barh.text(105, i,
                        '%d' % int(outcome_df.ix[:,0].values[i]),
                        ha='center', va='center')
        texts = barh.text(105, len(outcome_df)*text_offset,'Public requests\nvia FragDenStaat\nfrom 2011 to 2016',
                  ha='center',va='bottom')
                  
    elif orient == 'vertical':
        barv = outcome_df.ix[:,1:].plot(kind='bar',stacked=True, rot=0,figsize=(32,24))
        barv.xaxis.set_tick_params(top='off')
        barv.yaxis.set_tick_params(right='off')
        barv.yaxis.set_ticks(np.arange(0,101,10))
        barv.yaxis.set_ticklabels(np.arange(0,101,10))
        if not p_ticklabels==None:
            barv.xaxis.set_ticklabels(p_ticklabels, rotation=45, ha='right')
            lgd = plt.legend(loc='lower left', bbox_to_anchor=(0.0,-0.4,1.0,0.1),ncol=3,
                             mode='expand', borderaxespad=0., fontsize=18)
        else:
            lgd = plt.legend(loc='lower left', bbox_to_anchor=(0.0,-0.2,1.0,0.1),ncol=3,
                 mode='expand', borderaxespad=0., fontsize=32)
        
        plt.ylim((0,100))
        plt.ylabel('Percentage of completed requests')
        barv.grid(b=True, which='major', color=[0.5,0.5,0.5], linestyle='-',lw=2)
        font = {'size':32}
        title_artist = barv.text((len(outcome_df)-1)/2, 110, title, ha='center',
                                 va='center', fontdict = font)
        
        if include_descriptions:
            for i in range(len(outcome_df)):
                barv.text(i, 105,
                            '%d' % int(outcome_df.ix[:,0].values[i]),
                            ha='center', va='center')
            texts = barv.text(len(outcome_df)*text_offset, 105, 'Public requests\nvia FragDenStaat\nfrom 2011 to 2016',
                      ha='center',va='center')
    
    if save:
        if include_descriptions:
            plt.savefig(files_path+filename+'_' + orient + '.png',
                        bbox_extra_artists=[title_artist,lgd,texts], bbox_inches='tight')
        else:
            plt.savefig(files_path+filename+'_' + orient + '.png',
                        bbox_extra_artists=[title_artist,lgd], bbox_inches='tight')
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