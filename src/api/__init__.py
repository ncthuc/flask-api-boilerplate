# coding=utf-8
import logging
from flask_restx import Api
from flask import Blueprint

from src.extensions.exceptions import global_error_handler
from .api_user import ns as user_ns
from .api_hello import ns as hello_ns

__author__ = 'ThucNC'
_logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__, url_prefix=None)

api = Api(
    app=api_bp,
    version='1.0',
    title='Boilerplate API',
    validate=False,
    # doc='' # disable Swagger UI
)

api.add_namespace(user_ns)
api.add_namespace(hello_ns, path='/hello')  # path default to namespace's name

api.error_handlers[Exception] = global_error_handler


def init_api(app, **kwargs):
    """
    :param flask.Flask app: the app
    :param kwargs:
    :return:
    """
    app.register_blueprint(api_bp)
