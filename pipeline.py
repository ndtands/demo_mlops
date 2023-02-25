from ml_core import data_extraction
from ml_core import data_validation
from ml_core import data_preparation
from ml_core import training
from decouple import config
from pymongo import MongoClient

if __name__ =='__main__':
    PROJECT_NAME = config('PROJECT_NAME')
    MONGODB_USER = config('MONGODB_USER')
    MONGODB_PASSWORD = config('MONGODB_PASSWORD')
    DATASOURCE = config('DATASOURCE')
    MONGODB_URL = f'mongodb+srv://{MONGODB_USER}:{MONGODB_PASSWORD}@cluster0.k0hrmbm.mongodb.net/test'
    client = MongoClient(MONGODB_URL)
    db=client[DATASOURCE]
    collection_post = db.post
    data_extraction.extract_data(project=PROJECT_NAME, collection= collection_post)
    data_validation.validate_data(project=PROJECT_NAME)
    data_preparation.preparation_data(project=PROJECT_NAME)
    training.train(project=PROJECT_NAME, is_test=False)