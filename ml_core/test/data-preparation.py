from ml_core import data_preparation
from configs.config import logger
from decouple import config

if __name__ == '__main__':
    PROJECT_NAME = config('PROJECT_NAME')
    data_preparation.preparation_data(project=PROJECT_NAME)
    logger.info('Data Preparation Done')