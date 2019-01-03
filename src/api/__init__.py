# coding=utf-8
import logging
from flask_restplus import Api
from flask import Blueprint
from werkzeug.exceptions import HTTPException

from .api_user import ns as user_ns
from .api_hello import ns as hello_ns

__author__ = 'ThucNC'
_logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__, url_prefix=None)

api = Api(
    app=api_bp,
    version='1.0',
    title='Boilerplate API',
    validate=False
)

api.add_namespace(user_ns, path='/users')
api.add_namespace(hello_ns, path='/hello')


@api.errorhandler(Exception)
def default_error_handler(e):
    # traceback.print_exc()
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return {'success': False, 'message': str(e), 'code': code}, code


def init_api(app, **kwargs):
    """
    :param flask.Flask app: the app
    :param kwargs:
    :return:
    """
    app.register_blueprint(api_bp)
