# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 13:06:58 2015

@author: andrej
"""
import urllib
import logging
import json
import matplotlib.pyplot as plt
import numpy as np

import matplotlib as mpl
mpl.rcParams['font.size'] = 20
mpl.rcParams['axes.facecolor'] = 'white'
plt.style.use('ggplot')


data_decoded = np.load('request_data_until_1000.npy')[0]
print(data_decoded['objects'][0].keys())

req = data_decoded['objects'][0]

######################## RESPOMSE TIMES #############################

duedates = 0
no_duedate = 0
for request in data_decoded['objects']:
    if request['resolved_on'] == None:
        no_duedate += 1
    else:
        duedates += 1

aduedates = 0
ano_duedate = 0
for request in data_decoded['objects']:
    if request['due_date'] == None:
        ano_duedate += 1
    else:
        aduedates += 1
        
statuses = {}
resolved_count = 0
endstatuses = ['refused','successful', 'user_withdrew_costs', 'user_withdrew',\
                'resolved', 'partially_successful', 'request_redirected']
for request in data_decoded['objects']:
    is_resolved = False
#    for message in request['messages']:
#    message = request['messages'][-1]

    for message in request['messages']:
        if message['status'] in endstatuses:
            if message['status'] in statuses:
                statuses[message['status']] += 1
            else:
                statuses[message['status']] = 1
            continue
#    if request['resolved_on'] == None:
#        no_duedate += 1
#    else:
#        duedates += 1

########################## jurisdiction stuff ####################

jurisdictions = {}
public_bodies = {}
for request in data_decoded['objects']:
    if request['jurisdiction'] in jurisdictions:
        jurisdictions[request['jurisdiction']] += 1
    else:
        jurisdictions[request['jurisdiction']] = 1
        
    if request['public_body'] in public_bodies:
        public_bodies[request['public_body']] += 1
    else:
        public_bodies[request['public_body']] = 1



'''
for key in ['resolution', 'tags']:
    value_dict = {}
    for request in data_decoded['objects']:
        if request[key] in value_dict:
            value_dict[request[key]] += 1
        else:
            value_dict[request[key]] = 1
    
    value_list = np.array(list(value_dict.values()))
    labels = np.array(list(value_dict.keys()))
    sorting = np.argsort(np.array(value_list))
    sorting = sorting[::-1]
    
    
    plt.pie(value_list[sorting], labels=labels[sorting],autopct='%1.1f%%', startangle=0)
    plt.title(key)
'''
