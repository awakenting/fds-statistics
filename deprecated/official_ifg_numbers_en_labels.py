# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 13:12:30 2016

@author: andrej
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from cycler import cycler
import pandas as pd
import os

plt.style.use('ggplot')
mpl.rcParams['font.size'] = 24
mpl.rcParams['axes.facecolor'] = 'white'
#mpl.rcParams['axes.grid'] = True

#default_colors = mpl.rcParams['axes.color_cycle']
#mpl.rcParams['axes.color_cycle'] = ['#5DBA42', '#42BAB2', '#E24A33',
#                                    '#777777', '#348ABD', '#FBC15E', '#E27533']
# followoing hex-codes I would describe as:
# ['#5DBA42', '#42BAB2', '#E24A33','#777777', '#348ABD', '#FBC15E', '#E27533']
# 'green', 'turquise', 'red', 'dark gray', 'blue', 'yellow'
mpl.rcParams['axes.prop_cycle'] = cycler('color',['#E24A33', '#348ABD' , '#777777',
                                    '#5DBA42','#42BAB2', '#FBC15E', '#E27533'])

#E24A33', '#348ABD', '#988ED5', '#777777', '#FBC15E', '#8EBA42', '#FFB5B8']),

files_path = './figures/'

#%% ifg data from bmi website and fragdenstaat.de admin page

years =  ['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']

total = np.array([[2278,1265,1548,1358,1556,3280,6077,4736,8703,9376]])
bmf = np.array([[171,135,493,295,245,1179,2967,1390,5347,4170]])

fds = np.array([[0,0,0,0,0,352,2405,2416,3049,4017]])
fds_nurBund = np.array([[0,0,0,0,0,349,2253,1793,1627,2515]])
whout_bmf = (total-bmf)-fds_nurBund

fds_in_percent = (fds_nurBund/total)*100

data = np.concatenate((bmf,fds_nurBund,whout_bmf),axis=0)

#%% plot

df = pd.DataFrame(data.T,columns=['Ministry of Finances','FragDenStaat','Total whithout Finance und FDS'],
                  index = years)
ax = df.plot(kind='area',figsize=(16,12),alpha=0.9)
ax.plot([4.8,4.8],[0,3000],'k--',lw=4)
ax.xaxis.set_tick_params(top='off')
ax.yaxis.set_tick_params(right='off')
ax.annotate("Start of FragDenStaat (October 2011)",
            xy=(4.8,2500), xycoords='data',
            size=24,
            ha="center", va="center",
            xytext=(3, 5000), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            linewidth=2,
                            fc="k",ec="k",
                            connectionstyle="arc3,rad=0.2")
            )
ax.grid(b=True, which='major', color=[0.5,0.5,0.5], linestyle='-', lw=2)
plt.xlabel('Year')
plt.ylabel('Number of requests')

ax.legend_.set_bbox_to_anchor([1.01,1.0])
lgd = ax.get_legend()
#plt.ylim(0,np.max(data.sum(axis=0)))
plt.ylim(0,10000)

#%% save figure

if os.path.isdir(files_path):
    plt.savefig(files_path+'ifg_gesamtzahlen_en.png',bbox_extra_artists=[lgd],
                bbox_inches='tight',dpi=400)
else:
    os.mkdir(files_path)
    plt.savefig(files_path+'ifg_gesamtzahlen_en.png',bbox_extra_artists=[lgd],
                bbox_inches='tight',dpi=400)
plt.close()




