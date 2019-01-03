# coding=utf-8
import logging
from flask_restplus import Api
from flask import Blueprint

__author__ = 'ThucNC'
_logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__, url_prefix='/api')

api = Api(
    app=api_bp,
    version='1.0',
    title='Boilerplate API',
    validate=False,
    default_label='Boilerplate API'
)


def init_api(app, **kwargs):
    """
    :param flask.Flask app: the app
    :param kwargs:
    :return:
    """
    app.register_blueprint(api_bp)


from . import api_hello
