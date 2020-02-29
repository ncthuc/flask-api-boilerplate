import logging
from functools import wraps

import flask_login
from werkzeug.exceptions import Forbidden, Unauthorized

from src.model import User

__author__ = 'ThucNC'
_logger = logging.getLogger(__name__)

login_manager = flask_login.LoginManager()


def init_login_manager(app):
    login_manager.init_app(app)


@login_manager.request_loader
def load_user_from_request(request):
    """ Load User from request
    :param flask.Request request: the request
    :rtype: sso.models.User
    """
    return User.get_logged_in_user(request, False)


def required_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            current_user = flask_login.current_user
            if not current_user.is_authenticated:
                raise Unauthorized()
            if current_user.role not in roles:
                raise Forbidden(f"User '{current_user.email}' does not have the required permission")
            return f(*args, **kwargs)

        return wrapped

    return wrapper

