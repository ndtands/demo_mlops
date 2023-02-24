from ml_core import data_extraction
from decouple import config
from configs.config import logger
from pymongo import MongoClient


if __name__ == '__main__':
    MONGODB_USER = config('MONGODB_USER')
    MONGODB_PASSWORD = config('MONGODB_PASSWORD')
    DATASOURCE = config('DATASOURCE')
    PROJECT_NAME = config('PROJECT_NAME')
    MONGODB_URL = f'mongodb+srv://{MONGODB_USER}:{MONGODB_PASSWORD}@cluster0.k0hrmbm.mongodb.net/test'
    client = MongoClient(MONGODB_URL)
    db=client[DATASOURCE]
    collection_post = db.data
    df = data_extraction.extract_data(project=PROJECT_NAME, collection=collection_post)
    print(len(df))
    logger.info("Data extract Done")