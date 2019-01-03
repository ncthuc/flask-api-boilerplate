# coding=utf-8
import logging

from flask_restplus import Resource, Namespace

from src.helpers.response_helper import api_response

__author__ = 'ThucNC'
_logger = logging.getLogger(__name__)

ns = Namespace('user', description='User operations')


@ns.route('', methods=['GET'])
class UserApi(Resource):
    """
    Hello world api
    """
    def get(self):
        _logger.info('User API')
        return api_response('Hello user', 'ok', 200)

