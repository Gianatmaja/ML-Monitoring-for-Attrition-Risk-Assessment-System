'''
This file performs the data ingestion process, which consists of reading the data, compiling them,
performing data cleaning, as well as writing the output data and updating the records with the
filenames (and timestamps) of the dataset being used.

Author: Gian Atmaja
Date Created: 17 May 2023
'''


# Import required libraries
import numpy as np
import pandas as pd
import os
import glob
import json


# Load config.json, and get input and output paths
with open('config.json','r') as f:
    config = json.load(f) 

input_folder_path = config['input_folder_path']
output_folder_path = config['output_folder_path']


# Specify output files of the data ingestion process
output_logs_file = "ingestedfiles.txt"
output_filename = "finaldata.csv"


# Function for data ingestion
def merge_multiple_dataframe():

    # Get list of filenames
    filename_list = []
    for file in glob.glob("{}/*.csv".format(input_folder_path)):
        filename_list.append(file)
    
    # Compile dataset, then record source files and read timestamp
    df_list = []
    for file in filename_list:
        df = pd.read_csv(file, index_col = None, header = 0)
        df_list.append(df)

    # Convert data to df format, then perform deduplication
    df_all = pd.concat(df_list, axis = 0, ignore_index = True)
    df_final = df_all.drop_duplicates()

    # Record source files and read timestamp to txt file
    with open(output_folder_path + "/" + output_logs_file, "w") as records:
        for i in range(len(filename_list)):
            records.write(filename_list[i].split("/")[1] + "\n")
    records.close()

    return df_final


if __name__ == '__main__':
    df_ingested = merge_multiple_dataframe()
    filename = output_folder_path + "/" + output_filename
    df_ingested.to_csv(filename, index = False)