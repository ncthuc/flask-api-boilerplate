from werkzeug.exceptions import HTTPException as BaseHTTPException

from src.extensions.response_wrapper import wrap_response
from src.model import db


class HTTPException(BaseHTTPException):
    def __init__(self, code=400, message=None, errors=None):
        super().__init__(description=message, response=None)
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
    res = wrap_response(None, str(e), code)
    db.session.rollback()
    if errors:
        res[0]['errors'] = errors
    return res
