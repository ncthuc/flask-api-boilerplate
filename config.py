import os

import dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

dotenv.load_dotenv(os.path.join(basedir, '../../.env'))
# print('###########')
# print(os.environ)

ETC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'etc'))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    LOGGING_CONFIG_FILE = os.path.join(ETC_DIR, 'logging.ini')
    DEBUG = False
    BABEL_TRANSLATION_DIRECTORIES = '../translations'
    LANGUAGES = ['en', 'vi']


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_main.db')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_test.db')
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
