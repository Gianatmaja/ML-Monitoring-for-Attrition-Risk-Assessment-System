'''
This file performs calls on the API, testing endpoints defined on app.py.

Author: Gian Atmaja
Date Created: 21 May 2023
'''


# Import required libraries
import os
import json
import time
import requests


# API URL
URL = "http://127.0.0.1:8000"


# Define API calls
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
response1 = requests.post(
    "%s/prediction" %
    URL,
    json={
        "dataset_path": "testdata.csv"},
    headers=headers).text
response2 = requests.get("%s/scoring" % URL, headers=headers).text
response3 = requests.get("%s/summarystats" % URL, headers=headers).text
response4 = requests.get("%s/diagnostics" % URL, headers=headers).text


# Compile responses
report = response1 + "\n\n" + response2 + \
    "\n\n" + response3 + "\n\n" + response4


# Define path to store results of API calls
with open('config.json', 'r') as json_file:
    config = json.load(json_file)
json_file.close()

output_model_path = os.path.join(config['output_model_path']) 


# Write results to a .txt file
with open(('{}/apireturns.txt'.format(output_model_path)), "w") as apireturn_file:
    apireturn_file.write(report)
apireturn_file.close()
