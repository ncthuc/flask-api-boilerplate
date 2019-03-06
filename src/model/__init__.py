# coding=utf-8
import logging

from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

__author__ = 'ThucNC'
_logger = logging.getLogger(__name__)

db = SQLAlchemy()
migrate = Migrate(db=db)
bcrypt = Bcrypt()


def init_model(app, **kwargs):
    """
    :param flask.Flask app: the app
    :param kwargs:
    :return:
    """
    db.app = app
    db.init_app(app)
    migrate.init_app(app)
    bcrypt.init_app(app)


from src.model.user import User

