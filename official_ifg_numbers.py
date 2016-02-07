# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 13:12:30 2016

@author: andrej
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import os

plt.style.use('ggplot')
mpl.rcParams['font.size'] = 16
mpl.rcParams['axes.facecolor'] = 'white'

default_colors = mpl.rcParams['axes.color_cycle']
mpl.rcParams['axes.color_cycle'] = [default_colors[1],default_colors[0],default_colors[2]]

files_path = './figures/'

#%% ifg data from bmi website and fragdenstaat.de admin page

years =  ['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']

total = np.array([[2278,1265,1548,1358,1556,3280,6077,4736,8703,0]])
bmf = np.array([[171,135,493,295,245,1179,2967,1390,5347,0]])

fds = np.array([[0,0,0,0,0,352,2405,2416,3049,4017]])
fds_nurBund = np.array([[0,0,0,0,0,349,2253,1793,1627,2515]])
whout_bmf = (total-bmf)-fds_nurBund

fds_in_percent = (fds_nurBund/total)*100

data = np.concatenate((fds_nurBund,bmf,whout_bmf),axis=0)

#%% plot

df = pd.DataFrame(data.T,columns=['FragDenStaat','BM Finanzen','Gesamt ohne BMF und FdS'],
                  index = years)
ax = df[0:-1].plot(kind='area',figsize=(16,12))
ax.xaxis.set_tick_params(top='off')
ax.yaxis.set_tick_params(right='off')

ax.annotate("Start von FragDenStaat",
            xy=(4.5,2500), xycoords='data',
            size=24,
            ha="center", va="center",
            xytext=(3, 5000), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            linewidth=2,
                            fc="k",ec="k",
                            connectionstyle="arc3,rad=0.2")
            )
plt.xlabel('Jahr')
plt.ylabel('Anzahl von Anfragen')
plt.ylim(0,np.max(data.sum(axis=0)))

#%% save figure

if os.path.isdir(files_path):
    plt.savefig(files_path+'ifg_gesamtzahlen.png',dpi=150)
else:
    os.mkdir(files_path)
    plt.savefig(files_path+'ifg_gesamtzahlen.png',dpi=150)
plt.close()




