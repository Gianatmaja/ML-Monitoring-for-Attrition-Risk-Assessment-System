'''
This file performs deployment process by copying the model pickle file, the ingestion records as well as
the latest test f1-score of the trained model.

Author: Gian Atmaja
Date Created: 18 May 2023
'''


# Import required libraries
from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import os
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import json
import shutil


# Load config.json and correct path variable
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
prod_deployment_path = os.path.join(config['prod_deployment_path']) 
model_path = os.path.join(config['output_model_path']) 


# function for deployment
def store_model_into_pickle():

    # Copy model pickle file
    source = '{}/trainedmodel.pkl'.format(model_path)
    dest = '{}/trainedmodel.pkl'.format(prod_deployment_path)

    shutil.copyfile(source, dest)

    # Copy latest f1-score txt file
    source = '{}/latestscore.txt'.format(model_path)
    dest = '{}/latestscore.txt'.format(prod_deployment_path)

    shutil.copyfile(source, dest)

    # Copy latest list of ingested data files
    source = '{}/ingestedfiles.txt'.format(dataset_csv_path)
    dest = '{}/ingestedfiles.txt'.format(prod_deployment_path)

    shutil.copyfile(source, dest)
    
    status = "Process done"

    return status


if __name__ == '__main__':
    store_model_into_pickle()
