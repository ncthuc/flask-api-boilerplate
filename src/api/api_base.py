# coding=utf-8
import logging

from flask_restplus import fields

from src.api import api
from werkzeug.exceptions import HTTPException

__author__ = 'ThucNC'
_logger = logging.getLogger(__name__)


@api.errorhandler(Exception)
def default_error_handler(e):
    # traceback.print_exc()
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return {'success': False, 'message': str(e), 'code': code}, code


class BaseApi():
    GENERAL_RESP = api.model('GENERAL_RESP', {
        'code': fields.String(),
        'message': fields.String()
    })
    AUTHORIZATION = 'access-token'

    @staticmethod
    def api_response(data=None, message="", http_code=200):
        """ Return general HTTP response
        :param int http_code:
        :param str message: detail info
        :param data:
        :return:
        """
        return {
                   'code': http_code,
                   'success': http_code // 100 == 2,
                   'message': message,
                   'data': data
               }, http_code
