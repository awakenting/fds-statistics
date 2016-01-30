# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 17:37:12 2016

@author: andrej
"""

import numpy as np
import pandas as pd

def load_public_body_info():
    data_pbodies = np.load('./data/public_bodies.npy')
    
    pbody_names = {}
    pbody_classes = {}
    pbody_juris = {}
    pbody_juris_rank = {}
    
    # dictionaries 'translate' from uri of public body or jurisdiction to name,
    # class or rank
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
                
    return pbody_names, pbody_classes, pbody_juris, pbody_juris_rank
    


def load_requests():
    pbody_info = load_public_body_info()
    (pbody_names, pbody_classes, pbody_juris, pbody_juris_rank) = pbody_info
    
    # load raw data (into a numpy ndarray)  
    requests = np.load('./data/request_data.npy')
    
    #%% create dataframe (without messages, they are treated separately)
    keys = list(requests[0].keys())
    keys.remove('messages')
    dataframe = pd.DataFrame(list(requests),columns = keys, ignore_index=True)
    
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
    
    return dataframe
    
def load_messages():
    pbody_info = load_public_body_info()
    (pbody_names, pbody_classes, pbody_juris, pbody_juris_rank) = pbody_info
    
    # load raw data    
    datasets = np.load('./data/request_data_until_10083.npy')
    
    message_example = datasets[0]['objects'][0]['messages'][0]
    keys = list(message_example.keys())
    keys.remove('content')
    
    for i,data_decoded in enumerate(datasets):
        # get messages of requests and count how many messages per request so that
        # you can add the request id for each message
        message_list = []
        [message_list.extend(request['messages']) for request in data_decoded['objects']]
        messages_per_request = [len(request['messages']) for request in\
                                data_decoded['objects']]
        
        # load id's of requests
        rlist = data_decoded['objects']
        df_request_ids = pd.DataFrame(rlist,columns =  ['id'])
        
        # load messages into dataframe and add column with request id's
        if i == 0:
            dataframe = pd.DataFrame(message_list,columns = keys)
            request_ids = df_request_ids['id'].repeat(messages_per_request)
            dataframe['request_id'] = request_ids.values
        else:
            tempDf = pd.DataFrame(message_list,columns = keys)
            request_ids = df_request_ids['id'].repeat(messages_per_request)
            tempDf['request_id'] = request_ids.values
            dataframe = dataframe.append(tempDf, ignore_index = True)
            
    return dataframe
