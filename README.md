# ML Monitoring for an Attrition Risk Assessment System
A simple framework for machine learning models post deployment, which in this project, is applied to an attrition risk assessment system.


## Project Structure
This repository follows the following structure:

    .
    ├── sourcedata/                       # Directory storing data for model development
    ├── practicedata/                     # Directory storing data for practice
    ├── testdata/                         # Directory storing data for testing
    ├── ingesteddata/                     # Directory storing clean data
    ├── practicemodels/                   # Directory storing trial models
    ├── models/                           # Directory storing models build with sourcedata
    ├── productiondeployment/             # Directory soring deployed model
    ├── images/                           # Directory soring images  
    ├── ingestion.py   
    ├── training.py                     
    ├── scoring.py         
    ├── deployment.py
    ├── reporting.py    
    ├── diagnostics.py   
    ├── app.py    
    ├── apicalls.py  
    ├── fullprocess.py
    ├── wsgi.py                             
    ├── config.json
    ├── slice_output.txt
    ├── cronjob.txt
    └── README.md


## Running the Project
To install the requirements, run the following command:

    pip install -r requirements.txt

To run the app locally, run the following command:

    python app.py

To run the API calls, open a new CL/terminal tab, then run the following command:

    python apicalls.py

To run other scripts individually, run the following command:

    python {SCRIPT_NAME}.py


## The ML Monitoring Process
The entire monitoring process, which is orchestrated by the `fullprocess.py` script, follows the diagram below:

![process_flow](https://github.com/Gianatmaja/ML-Monitoring-for-Attrition-Risk-Assessment-System/blob/main/images/process_flow.png)

This process can be setup to run automatically at specific intervals using `cron`. The shell command used to do this can be found in `cronjob.txt`. This command tells the `fullprocess.py` script to run every 10 minutes.

For more information on cron expressions, check out their [documentation](https://docs.oracle.com/cd/E12058_01/doc/doc.1014/e12030/cron_expressions.htm).


### Data Ingestion
First, the script will check for new data under the `input_folder_path`, defined in `config.json`. If new data is present, the ingestion process, defined by the `ingestion.py` script, will run and produce a new dataset, stored under `output_folder_path`, again defined in config.json.

In this example, the paths are just subdirectories. However, the same concept can be extended to other data storage options.


### Model Retraining & Redeployment
Using the new data produced in the step above, the script will proceed to test the existing model, stored in `prod_deployment_path`, against this new data. The model scores are recorded, and if model drift is detected, the script will initiate the retraining and redeployment steps (defined in the `training.py` and `deployment.py` scripts), before finally initiating the reporting and diagnostics steps (defined in the `reporting.py` and `diagnostics.py` scripts).

Other than model drift, data drift will also be assessed and reported using EvidentlyAI.

![data_drift_dashboard](https://github.com/Gianatmaja/ML-Monitoring-for-Attrition-Risk-Assessment-System/blob/main/images/drift_report.png)

For more information on EvidentlyAI, check out their [documentation](https://docs.evidentlyai.com/).


### Flask API
The codes for the Flask API are defined in the `app.py` script, which can be run via the command line or terminal. As models are retrained and redeployed, the app will continuously update as well. To test the endpoints defined in the `app.py` script, run `apicalls.py` in a separate CL/terminal tab.

For more information on Flask, check out their [documentation](https://flask.palletsprojects.com/en/2.3.x/).
