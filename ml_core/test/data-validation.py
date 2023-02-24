from ml_core import data_validation
from configs.config import logger
from decouple import config
if __name__ == '__main__':
    PROJECT_NAME = config('PROJECT_NAME')
    data_validation.validate_data(project=PROJECT_NAME)
    logger.info('Validation Done')
