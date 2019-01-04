def wrap_response(data=None, message="", http_code=200):
    """ Return general HTTP response
    :param data:
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
    return res, http_code
