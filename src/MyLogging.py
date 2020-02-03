import logging
from logging.handlers import RotatingFileHandler


def init_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler('log.txt', mode='a', maxBytes=2 * 1024 * 1024,
                                       backupCount=1, encoding='utf-8', delay=0)

    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.debug('Logger initialized')
