import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('logger.log', mode='a', encoding='utf-8' )
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
