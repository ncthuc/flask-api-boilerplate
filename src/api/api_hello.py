# coding=utf-8
import logging
from werkzeug.exceptions import Unauthorized

from flask_restplus import Resource
from src.extensions.namespace import Namespace

from src.helpers.response_helper import api_response

__author__ = 'ThucNC'
_logger = logging.getLogger(__name__)

ns = Namespace('hello', description='Hello operations')


@ns.route('', methods=['GET'])
class HelloApi(Resource):
    """
    Hello world api
    """
    def get(self):
        _logger.info('Hello world API')
        return api_response('Hello world', 'ok', 200)


@ns.route('/ex0', methods=['GET'])
class Exception0Api(Resource):
    """
    Exception api
    """
    def get(self):
        1/0


@ns.route('/ex1', methods=['GET'])
class Exception1Api(Resource):
    """
    Exception api
    """
    def get(self):
        raise ValueError('Value error exception!')


@ns.route('/ex2', methods=['GET'])
class Exception2Api(Resource):
    """
    Exception api
    """
    def get(self):
        raise Unauthorized("Login required!")




