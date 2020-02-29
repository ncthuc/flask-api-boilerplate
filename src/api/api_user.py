# coding=utf-8
import logging

import flask_login
from flask import request
from flask_restx import Resource, fields
from werkzeug.exceptions import BadRequest, Forbidden

from src.extensions import reqparse
from src.extensions.namespace import Namespace
from src.extensions.response_wrapper import wrap_response
from src.helpers import login_manager
from src.model import db
from src.model.user import User, UserSchema

__author__ = 'ThucNC'
_logger = logging.getLogger(__name__)

ns = Namespace('user', description='User operations')

_user = ns.model('user', UserSchema.user)
_user_post = ns.model('user_post', UserSchema.user_post)
_user_put = ns.model('user_put', UserSchema.user_put)


@ns.route('/me', methods=['GET', 'PUT'])
class UserResource(Resource):
    """
    Manipulations with a specific user.
    """

    @ns.doc(security='access-token')
    @ns.marshal_with(_user)
    @flask_login.login_required
    def get(self):
        """
            Get current user info
        """
        # return User.get_logged_in_user()
        return flask_login.current_user

    @ns.doc(security='access-token')
    @ns.marshal_with(_user)
    @ns.expect(_user_put, validate=False)
    @flask_login.login_required
    def put(self):
        """
            Update current user info
        """
        data = request.json
        user: User = flask_login.current_user
        user.update(data, exclude=['email', 'role'])
        return user


@ns.route('/login')
class LoginApi(Resource):
    LOGIN_INFO = ns.model('LOGIN_INFO', {
        'email': fields.String(),
        'password': fields.String()
    })

    @ns.expect(LOGIN_INFO)
    def post(self):
        """
        Login with username and password
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, location='json')
        parser.add_argument('password', type=str, location='json')
        params = parser.parse_args()

        email = params['email']
        password = params['password']
        if email and password:
            access_token = User.login_with_email_or_username(email, password)
            return wrap_response(http_code=200, message='OK', data=access_token)
        raise BadRequest("Invalid params")


@ns.route('/login-google')
class LoginGoogleApi(Resource):
    """
    Api for user user management
    """
    LOGIN_GOOGLE_INFO = ns.model('LOGIN_GOOGLE_INFO', {
        'google_token': fields.String()
    })

    @ns.expect(LOGIN_GOOGLE_INFO)
    def post(self):
        """
        Login with Google id_token

        For testing:
        1. Access https://developers.google.com/oauthplayground/
        2. Scroll to Google+ API, choose https://www.googleapis.com/auth/userinfo.email and other scope if needed
        3. Click `Authorize APIs`
        4. Click  `Exchange authorization code for tokens`
        5. Copy id_token
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument('google_token', type=str, location='json')
        params = parser.parse_args()

        google_token = params['google_token']
        if google_token:
            access_token = User.login_with_google_token(google_token)
            return wrap_response(http_code=200, message='OK', data=access_token)
        raise BadRequest("Invalid params")


@ns.route('/password')
class SetPassword(Resource):
    PASSWORD = ns.model('PASSWORD', {
        'current_password': fields.String(required=False),
        'new_password': fields.String(required=True)
    })

    @ns.doc(security='access-token')
    @flask_login.login_required
    @ns.expect(PASSWORD)
    def put(self):
        """
        set or update password
        """
        user = flask_login.current_user
        data = request.json
        old_password = data.get('current_password', "")
        new_password = data.get('new_password')

        if user.password_hash and not user.check_password(old_password):
            raise Forbidden("Invalid current password")

        user.password = new_password
        db.session.commit()
        return wrap_response(data=None, http_code=200, message='success')

    @ns.doc(security='access-token')
    @login_manager.required_roles('moderator', 'admin', 'viewer', 'customer-care')
    @flask_login.login_required
    def get(self):
        """
        check user had password
        :param:
        :return:
        """
        # user = User.get_logged_in_user()
        user = flask_login.current_user
        return wrap_response(http_code=200, message='OK', data={'has_password': user.password_hash is not None})


@ns.route('/logout')
class Logout(Resource):

    @ns.doc(security='access-token')
    # @login_manager.required_roles('moderator', 'admin', 'viewer')
    @flask_login.login_required
    def post(self):
        """
            logout
        """
        User.logout()
        return wrap_response(data=None, http_code=200, message='success')
