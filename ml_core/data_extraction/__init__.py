import pymongo
import pandas as pd
import wandb
import random
import string

def fetch_data(collection: pymongo.collection.Collection):
    list_json = []
    for i in collection.find():
        list_json.append(i)

    # Convert jsonl to dataframe
    df = pd.json_normalize(list_json)
    print("Size of dataset: ",len(df))
    return df

def extract_data(project: str, collection: pymongo.collection.Collection):
    run = wandb.init(project=project, job_type="data-extraction")

    # Create a sample dataset to log as an artifact
    df = fetch_data(collection=collection)

    # log data artifacts
    dataset_artifact = wandb.Artifact('raw-dataset', type='dataset')
    dataset_table = wandb.Table(data=df, columns=df.columns)
    dataset_artifact.add(dataset_table, 'raw-dataset')
    run.log_artifact(dataset_artifact)

    wandb.finish()