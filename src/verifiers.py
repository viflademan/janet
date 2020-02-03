import logging


def integer(word: str, maximum: int = None):
    try:
        word_int = int(word)
    except ValueError as e:
        logging.info(e)
        return False
    if maximum is not None:
        if word_int not in range(0, maximum):
            logging.info(f'Supplied int not in range. ({word_int} in range 0-{maximum})')
            return False

    return True
