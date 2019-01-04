from flask_restplus._http import HTTPStatus as BaseHTTPStatus
from werkzeug.exceptions import HTTPException as BaseHTTPException


class HTTPException(BaseHTTPException):
    def __init__(self, code=400, message=None, response=None, errors=None):
        super().__init__(description=message, response=response)
        self.code = code
        self.errors = errors