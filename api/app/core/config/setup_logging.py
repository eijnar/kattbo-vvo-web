import logging
from logging.handlers import RotatingFileHandler


def setup_logging(config_class):
    try:
        log_format_string = config_class.LOG_FORMAT
        formatter = logging.Formatter(log_format_string)

        file_handler = RotatingFileHandler(
            config_class.LOG_FILE_PATH, 
            maxBytes=config_class.LOG_FILE_MAX_SIZE, 
            backupCount=config_class.LOG_FILE_BACKUP_COUNT
            )
        
        file_handler.setFormatter(formatter)
        file_handler.setLevel(
            config_class.LOG_LEVEL
            )
        
        root_logger = logging.getLogger()
        root_logger.setLevel(config_class.LOG_LEVEL)
        root_logger.addHandler(file_handler)

    except Exception as e:
        print(f'Error setting up logging: {e}')


