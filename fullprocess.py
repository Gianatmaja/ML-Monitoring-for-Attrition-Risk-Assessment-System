'''
This file orchestrates the entire process, starting from checking for new data, performing data ingestion
in the presence of new data, checking for model drift, performing model retraining & redeployment in the
presence of model drift, as well as re-running the reporting & API calls script post redeployment.

Author: Gian Atmaja
Date Created: 21 May 2023
'''


# Import required libraries
import pandas as pd
import numpy as np
import os
import json
import sys
from sklearn.metrics import f1_score
import pickle
import glob

import ingestion
import training
import scoring
import deployment
import diagnostics
import reporting


# Get config
with open('config.json', 'r') as json_file:
    config = json.load(json_file)
json_file.close()


# Define paths
input_folder_path = config['input_folder_path']
output_folder_path = config['output_folder_path']
model_path = os.path.join(config['output_model_path']) 
prod_deployment_path = os.path.join(config['prod_deployment_path']) 


# Main function
def main():

    # Read ingestedfiles.txt
    with open(os.path.join(os.path.join(config['prod_deployment_path']), "ingestedfiles.txt")) as ingested_file:
        ingested_files = ingested_file.read().splitlines()
    ingested_file.close()

    # Determine whether the source data folder has files that aren't listed in ingestedfiles.txt
    dataset_files = []
    for file in glob.glob("{}/*.csv".format(input_folder_path)):
        dataset_files.append(file.split("/")[1])

    # Exit if no new data is identified
    if (ingested_files == dataset_files):
        sys.exit()

    # Ingest if new data is available
    df_ingested = ingestion.merge_multiple_dataframe()
    filename = output_folder_path + "/" + "finaldata.csv"
    df_ingested.to_csv(filename, index = False)
    
    # Check for model drift based on scores
    with open("{}/latestscore.txt".format(prod_deployment_path)) as score_file:
        latest_score = float(score_file.read().splitlines()[0])
    score_file.close()
    
    # Score existing model on new dataset
    df_new = pd.read_csv('{}/finaldata.csv'.format(output_folder_path))
    model = pickle.load(open('{}/trainedmodel.pkl'.format(prod_deployment_path), 'rb'))
    f1_new = scoring.score_model(df_new, model)

    # exit if lastest_score smaller or equal
    if (latest_score >= f1_new):
        sys.exit()
    
    # Re-train model if model drift is detected
    model = training.train_model(df_new)
    pickle.dump(model, open('{}/trainedmodel.pkl'.format(model_path), 'wb'))

    # Perform re-deployment
    deployment.store_model_into_pickle()

    # Re-run reporting script
    reporting.score_model()

    # Re-run API calls
    os.system("python apicalls.py")


if __name__ == '__main__':
    main()

