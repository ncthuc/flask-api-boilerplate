# coding=utf-8
import logging

__author__ = 'ThucNC'
_logger = logging.getLogger(__name__)


def wrap_response(data=None, message="", http_code=200, metadata=None):
    """ Return general HTTP response
    :param data:
    :param metadata:
    :param str message: detail info
    :param int http_code:
    :return:
    """
    res = {
        'code': http_code,
        'success': http_code // 100 == 2,
        'message': message,
    }

    if data is not None:
        res['data'] = data
    if metadata:
        res['metadata'] = metadata
    return res
