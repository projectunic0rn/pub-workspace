import logging
import time 

class InitLogger:
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls, name="", app_env="production") -> logging.Logger:
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            # Put any initialization here.
            log_level = logging.WARNING if app_env == 'production' else logging.DEBUG
            # create logger
            logger = logging.getLogger(name)
            logger.setLevel(log_level)
            # create console handler and set level to debug
            ch = logging.StreamHandler()
            ch.setLevel(log_level)
            # create formatter
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            # add formatter to ch
            ch.setFormatter(formatter)
            # add ch to logger
            logger.addHandler(ch)
            cls._instance = logger
            return cls._instance
        return cls._instance

