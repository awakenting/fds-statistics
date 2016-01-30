# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 13:06:58 2015

@author: andrej
"""
import urllib
import json
import numpy as np

def download_from_url(url):
    """Download url and return the content."""
    r = urllib.request.urlopen(url)
    data = r.read()
    data = data.decode(encoding='UTF-8')

    return data

#%% load request data
### THIS TAKES QUITE A WHILE BECAUSE YOU CAN ONLY REQUEST SMALL BATCHES WITH ONE REQUEST

url_all = 'https://fragdenstaat.de/api/v1/request/?limit=1'
data_all = download_from_url(url_all)
data_all_decoded = [json.loads(data_all)]
max_requests = data_all_decoded[0]['meta']['total_count']


url = 'https://fragdenstaat.de/api/v1/request/?'
limit = 200 # bigger batches don't seem to work
#print(data_decoded['objects'][0].keys())
print('load requests\n')
datasets = []
for offset in np.arange(0,max_requests,limit):
    complete_url = url + 'limit=' + str(int(limit)) + '&offset=' + str(int(offset))
    data = download_from_url(complete_url)
    datasets.extend(json.loads(data)['objects'])
    #time.sleep(5) # delays for 5 seconds
    print('Loading part ' + str(int(offset/limit+1)) + ' of ' + str(int(max_requests/limit)) + '...', end='\r')
print('loading done')

np.save('./data/request_data',datasets)

#%% load jurisdiction list

url_juri = 'https://fragdenstaat.de/api/v1/jurisdiction/'

data_juri = download_from_url(url_juri)
data_juri_decoded = [json.loads(data_juri)]
np.save('./data/jurisdictions', data_juri_decoded)

#%% load all public bodies

url_public = 'https://fragdenstaat.de/api/v1/publicbody/?'

url_all = 'https://fragdenstaat.de/api/v1/publicbody/?limit=1'
data_all = download_from_url(url_all)
data_all_decoded = [json.loads(data_all)]
max_requests = data_all_decoded[0]['meta']['total_count']
#max_requests = 100

limit = 100 # bigger batches don't seem to work
#print(data_decoded['objects'][0].keys())
print('load requests\n')
datasets_pb = []
for offset in np.arange(0,max_requests,limit):
    complete_url = url_public + 'limit=' + str(int(limit)) + '&offset=' + str(int(offset))
    data = download_from_url(complete_url)
    raw_data = json.loads(data)
    save_data = []
    for pbody in raw_data['objects']:
        pbody.pop('laws')
        pbody.pop('default_law')
        save_data.append(pbody)
    datasets_pb.extend(save_data)
    #time.sleep(5) # delays for 5 seconds
    print('Loading part ' + str(int(offset/limit+1)) + ' of ' + str(int(max_requests/limit)) + '...', end='\r')
print('loading done')

np.save('./data/public_bodies',datasets_pb)


