# pylint: disable=too-few-public-methods
"""Module for initializing global logger object"""
import logging

class InitLogger:
    """InitLogger defines singleton for setting/retrieving global logger
       usage:
       # Initial initialization on startup
       InitLogger.instance(slack, development)
       # Follow up retrieving
       InitLogger.instance()
    """
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls, name="", app_env="production") -> logging.Logger:
        """Set/Get instance of logger"""
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            log_level = logging.WARNING if app_env == 'production' else logging.DEBUG
            # create logger
            logger = logging.getLogger(name)
            logger.setLevel(log_level)
            # create console handler and set level based on APP_ENV
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(log_level)
            # create formatter
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            # add formatter to stream_handler
            stream_handler.setFormatter(formatter)
            # add stream_handler to logger
            logger.addHandler(stream_handler)
            cls._instance = logger
            return cls._instance
        return cls._instance
