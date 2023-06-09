'''
This file performs the model training process using the cleaned data obtained from the data
ingestion process. The output of this step will be the trained model pickle file, which will
be saved in the practicemodels/ directory.

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

# Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
model_path = os.path.join(config['output_model_path']) 


# Function for training the model
def train_model(df):

    # Get X & y features
    X = df[['lastmonth_activity', 'lastyear_activity', 'number_of_employees']]
    y = df['exited']

    # Fit logistic regression model
    log_model = LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
                    intercept_scaling=1, l1_ratio=None, max_iter=100,
                    multi_class='auto', n_jobs=None, penalty='l2',
                    random_state=0, solver='liblinear', tol=0.0001, verbose=0,
                    warm_start=False).fit(X, y)
    
    return log_model


if __name__ == '__main__':
    data = pd.read_csv('{}/finaldata.csv'.format(dataset_csv_path))
    model = train_model(data)
    pickle.dump(model, open('{}/trainedmodel.pkl'.format(model_path), 'wb'))