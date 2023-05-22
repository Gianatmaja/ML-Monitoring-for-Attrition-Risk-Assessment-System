'''
This file performs diagnostics on the data, models, and dependencies used in the project.

Author: Gian Atmaja
Date Created: 19 May 2023
'''


# Import required libraries
import pandas as pd
import numpy as np
import timeit
import os
import json
import pickle
import subprocess
import sys


# Load config.json and get environment variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
test_data_path = os.path.join(config['test_data_path']) 
prod_deployment_path = os.path.join(config['prod_deployment_path']) 


# Function to get model predictions
def model_predictions(df):

    #read the deployed model and a test dataset, calculate predictions
    filename = prod_deployment_path + "/" + "trainedmodel.pkl"

    with open(filename, 'rb') as pickle_file:
        model = pickle.load(pickle_file)

    X = df[['lastmonth_activity', 'lastyear_activity', 'number_of_employees']]
    y = df['exited']

    # Predict on test X features
    y_preds = model.predict(X)

    return y_preds


# Function to get summary statistics
def dataframe_summary():

    # Read in data and select columns
    df = pd.read_csv("{}/finaldata.csv".format(dataset_csv_path))
    df = df[['lastmonth_activity', 'lastyear_activity', 'number_of_employees']]

    # Get summary
    col_stats = []
    for column in df.columns:
        col_stats.append([column + " (mean):", df[column].mean()])
        col_stats.append([column + " (median):", df[column].median()])
        col_stats.append(
            [column + " (standard deviation):", df[column].std()])

    return col_stats


# Function to obtain missing data proportion
def missing_data():

    # Read in data
    df = pd.read_csv("{}/finaldata.csv".format(dataset_csv_path))
    
    # Calculate proportion of null values
    na_prop = []
    for column in df.columns:
        na_prop.append(
            [column + " (%):", int(df[column].isna().sum() / df[column].shape[0] * 100)])

    return na_prop


# Function to get timings of data ingestion and model training scripts
def execution_time():
    
    # Select scripts to time
    scripts_to_time = ['ingestion.py', 'training.py']
    time_records = []

    #calculate timing of ingestion.py and training.py
    for script in scripts_to_time:
        starttime = timeit.default_timer()
        _ = subprocess.run(['python', script], capture_output=True)
        timing = timeit.default_timer() - starttime
        time_records.append([script + ": ", timing])

    return time_records


# Function to check dependencies
def outdated_packages_list():

    # Get list of packages, used and current versions
    outdated_packages = subprocess.check_output(
        ['pip', 'list', '--outdated']).decode(sys.stdout.encoding)

    return outdated_packages


if __name__ == '__main__':
    df_test = pd.read_csv('{}/testdata.csv'.format(test_data_path))
    print(model_predictions(df_test), '\n')
    print(dataframe_summary(), '\n')
    print(missing_data(), '\n')
    print(execution_time(), '\n')
    print(outdated_packages_list())

