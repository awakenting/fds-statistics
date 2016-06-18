# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 12:29:31 2015

@author: andrej
"""
import os
import matplotlib.pyplot as plt
import numpy as np

import matplotlib as mpl
mpl.rcParams['font.size'] = 20
mpl.rcParams['axes.facecolor'] = 'white'
plt.style.use('ggplot')

ls = os.listdir()
datanames = [ls[i] for i in range(len(ls)) if ls[i].startswith('request_data_until')]

datasets = []
for file in datanames:
    datasets.extend(np.load(file))

resolutions = {}
for data_decoded in datasets:
    for request in data_decoded['objects']:
        if request['resolution'] in resolutions:
            resolutions[request['resolution']] += 1
        else:
            resolutions[request['resolution']] = 1
    
reslist = np.array(list(resolutions.values()))
labels = np.array(list(resolutions.keys()))
#labels[0] = '
sorting = np.argsort(np.array(reslist))
sorting = sorting[::-1]




plt.pie(reslist[sorting], labels=labels[sorting],autopct='%1.1f%%', startangle=0)
plt.title('Results of all requests ('+str(np.sum(reslist))+')')