'''
This file performs model scoring on the model trained in the training process. The output of this step
will be a .txt file containing the test F1 score of the model.

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
from sklearn.metrics import f1_score
import json


# Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 


test_data_path = os.path.join(config['test_data_path']) 
model_path = os.path.join(config['output_model_path']) 


# Function for model scoring
def score_model(df, model_file):
    
    # Get X & y features
    X = df[['lastmonth_activity', 'lastyear_activity', 'number_of_employees']]
    y = df['exited']

    # Predict on test X features
    y_preds = model_file.predict(X)

    # Get f1 score (test)
    f1 = f1_score(y, y_preds)

    # Write f1 score to .txt file
    with open(model_path + "/latestscore.txt", "w") as record:
        record.write(str(f1))
    record.close()

    return f1


if __name__ == '__main__':
    model = pickle.load(open('{}/trainedmodel.pkl'.format(model_path), 'rb'))
    df_test = pd.read_csv('{}/testdata.csv'.format(test_data_path))
    score_model(df_test, model)



