from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import logging
from app import app as application

__author__ = 'ThucNC'
_logger = logging.getLogger(__name__)

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000)
