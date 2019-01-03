# coding=utf-8
import logging
from werkzeug.exceptions import Unauthorized

from src.api import api
from src.api.api_base import BaseApi
from flask_restplus import Resource, fields

__author__ = 'ThucNC'
_logger = logging.getLogger(__name__)


@api.route('/hello', methods=['GET'])
class HelloApi(Resource, BaseApi):
    """
    Hello world api
    """
    def get(self):
        _logger.info('Hello world API')
        return BaseApi.api_response('Hello world', 'ok', 200)


@api.route('/ex0', methods=['GET'])
class Exception0Api(Resource, BaseApi):
    """
    Exception api
    """
    def get(self):
        1/0


@api.route('/ex1', methods=['GET'])
class Exception1Api(Resource, BaseApi):
    """
    Exception api
    """
    def get(self):
        raise ValueError('Value error exception!')


@api.route('/ex2', methods=['GET'])
class Exception2Api(Resource, BaseApi):
    """
    Exception api
    """
    def get(self):
        raise Unauthorized("Login required!")




