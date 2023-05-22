'''
This file plots a confusion matrix on the production model & test dataset.

Author: Gian Atmaja
Date Created: 20 May 2023
'''


# Import required libraries
import numpy as np
import pandas as pd
import json
import os
import time
import matplotlib.pyplot as plt
from sklearn.metrics import plot_confusion_matrix
from diagnostics import model_predictions
import pickle


# Load config.json and get path variables
with open('config.json', 'r') as json_file:
    config = json.load(json_file)
json_file.close()


# Get paths
test_data_path = os.path.join(config['test_data_path'])
prod_deployment_path = os.path.join(config['prod_deployment_path'])
output_model_path = os.path.join(config['output_model_path']) 
confusionmatrix_pth = output_model_path + '/' + 'confusionmatrix.png'


# Function to plot confusion matrix
def score_model():
    
    # Read data
    df = pd.read_csv('{}/testdata.csv'.format(test_data_path))

    # Obtain model
    filename = prod_deployment_path + "/" + "trainedmodel.pkl"

    with open(filename, 'rb') as pickle_file:
        model = pickle.load(pickle_file)
    
    # Define X & y variables
    X = df[['lastmonth_activity', 'lastyear_activity', 'number_of_employees']]
    y = df['exited']

    # Plot confusion matrix & save as .png file
    plot_confusion_matrix(model, X, y)
    plt.savefig(confusionmatrix_pth)

    status = "Confusion matrix plot saved"

    return status
    

if __name__ == '__main__':
    score_model()
