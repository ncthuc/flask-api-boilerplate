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
