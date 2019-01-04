from flask_restplus._http import HTTPStatus as BaseHTTPStatus
from werkzeug.exceptions import HTTPException as BaseHTTPException


class HTTPException(BaseHTTPException):
    def __init__(self, code=400, message=None, response=None, errors=None):
        super().__init__(description=message, response=response)
        self.code = code
        self.errors = errors


def global_error_handler(e):
    # traceback.print_exc()
    code = 500
    errors = None
    if isinstance(e, BaseHTTPException):
        code = e.code
    if isinstance(e, HTTPException):
        errors = e.errors
    return {'success': False, 'message': str(e), 'code': code, 'errors': errors}, code