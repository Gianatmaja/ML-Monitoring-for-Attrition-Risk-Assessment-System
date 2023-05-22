'''
This file sets up the API using Flask, and connects it with functions defined throughout the project.

Author: Gian Atmaja
Date Created: 20 May 2023
'''


# Import required libraries
import numpy as np
import pandas as pd
import json
import os
from flask import Flask, request
from diagnostics import model_predictions, dataframe_summary, missing_data, execution_time, outdated_packages_list
from scoring import score_model
import pickle


# Set up variables for use in our script
app = Flask(__name__)
app.secret_key = '1652d576-484a-49fd-913a-6879acfa6ba4'


# Default endpoint
@app.route('/')
def index():

    # Returns "Hello {user_name}"
    user = request.args.get("user")

    return "Hello " + user + "\n"


# Prediction endpoint
@app.route("/prediction", methods=['POST', 'OPTIONS'])
def predict():
    
    # Returns prediction on posted dataset, using prod model
    with open('config.json', 'r') as json_file:
        config = json.load(json_file)
    json_file.close()

    # Define paths
    data_file = request.get_json()['dataset_path']
    test_data_path = os.path.join(config['test_data_path'])

    # Read data
    df_test = pd.read_csv('{}/{}'.format(test_data_path, data_file))

    # Obtain predictions
    y_preds = model_predictions(df_test)

    return str(y_preds)


# Model scoring endpoint
@app.route("/scoring", methods=['GET', 'OPTIONS'])
def scoring():
    
    # Returns model scores
    with open('config.json', 'r') as json_file:
        config = json.load(json_file)
    json_file.close()

    # Define paths
    prod_deployment_path = os.path.join(config['prod_deployment_path']) 
    test_data_path = os.path.join(config['test_data_path']) 

    # Load model and data, then test model
    model = pickle.load(open('{}/trainedmodel.pkl'.format(prod_deployment_path), 'rb'))
    df_test = pd.read_csv('{}/testdata.csv'.format(test_data_path))
    score = score_model(df_test, model)

    return str(score)


# Dataset summary endpoint
@app.route("/summarystats", methods=['GET', 'OPTIONS'])
def stats():
    
    # Returns summary statistics on dataset
    statistics = dataframe_summary()

    return str(statistics)


# Diagnostics endpoint
@app.route("/diagnostics", methods=['GET', 'OPTIONS'])
def diagnostics():

    # Checks NA proportion, script execution time, and outdated dependencies
    na_data = str(missing_data())
    exec_time = str(execution_time())
    outd_packages_list = str(outdated_packages_list())

    return na_data + "\n\n" + exec_time + "\n\n" + outd_packages_list


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
