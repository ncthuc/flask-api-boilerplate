# coding=utf-8
import logging
from flask_restx import Api
from flask import Blueprint

from src.extensions.exceptions import global_error_handler

from .api_admin_user import ns as admin_user_ns

__author__ = 'ThucNC'
_logger = logging.getLogger(__name__)

api_bp = Blueprint('api_admin', __name__, url_prefix="/admin")

api = Api(
    app=api_bp,
    version='1.0',
    title='Admin API',
    validate=False,
    authorizations= {
        'access-token': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'access-token'
        }
    }
    # doc='' # disable Swagger UI
)

api.add_namespace(admin_user_ns)

api.error_handlers[Exception] = global_error_handler


def init_admin_api(app, **kwargs):
    """
    :param flask.Flask app: the app
    :param kwargs:
    :return:
    """
    app.register_blueprint(api_bp)
