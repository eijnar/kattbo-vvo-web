from os import environ

class Config(object):

    # Logging setup:
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
    LOG_FILE_PATH = environ.get('LOG_FILE_PATH')
    LOG_FILE_BACKUP_COUNT = 5
    LOG_FILE_MAX_SIZE = 10240

    # Environment setup, might be decrepid
    api_environment = environ.get('API_ENVIRONMENT')

class ProductionConfig(Config):
    LOG_LEVEL = 'INFO'
    SQLALCHEMY_DATABASE_URL = environ.get('SQLALCHEMY_DATABASE_URL_PROD')

class DevelopmentConfig(Config):
    LOG_LEVEL = 'DEBUG'
    SQLALCHEMY_DATABASE_URL = environ.get('SQLALCHEMY_DATABASE_URL_DEV')

class TestConfig(Config):
    LOG_LEVEL = 'DEBUG'
    SQLALCHEMY_DATABASE_URL = environ.get('SQLALCHEMY_DATABASE_URL_PROD')