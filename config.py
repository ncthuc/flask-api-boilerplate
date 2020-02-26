import os
# import dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
# dotenv.load_dotenv(os.path.join(basedir, '../../.env'))
ETC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'etc'))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    LOGGING_CONFIG_FILE = os.path.join(ETC_DIR, 'logging.ini')
    DEBUG = False
    BABEL_TRANSLATION_DIRECTORIES = '../translations'
    LANGUAGES = ['en', 'vi']
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # PRESERVE_CONTEXT_ON_EXCEPTION = False
