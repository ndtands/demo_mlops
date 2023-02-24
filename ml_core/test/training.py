from ml_core import training
from configs.config import logger
from decouple import config

if __name__ == '__main__':
    PROJECT_NAME = config('PROJECT_NAME')
    training.train(project=PROJECT_NAME, is_test = True)
    logger.info('Training + Tuning Done')