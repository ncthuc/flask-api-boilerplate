# coding=utf-8
import logging

import flask_sqlalchemy
from flask import request
from flask_restplus import Resource

from src.extensions.namespace import Namespace
from src.extensions.response_wrapper import wrap_response
from src.helpers.request_helper import RequestHelper
from src.model.user import User, UserSchema

__author__ = 'ThucNC'
_logger = logging.getLogger(__name__)

ns = Namespace('users', description='User operations')

_user = ns.model('user', UserSchema.user)
_user_post = ns.model('user_post', UserSchema.user_post)


@ns.route('/', methods=['GET', 'POST'])
class Users(Resource):
    @ns.expect(RequestHelper.pagination_params, validate=True)
    @ns.marshal_list_with(_user)
    def get(self):
        """
            Get list of user
        """
        _logger.warn('User API: {}')
        args = RequestHelper.pagination_params.parse_args()
        # return wrap_response(args, 'ok', 200)
        res = User.query.offset((args['page']-1) * args['pageSize']).limit(args['pageSize']).all()
        # print(flask_sqlalchemy.get_debug_queries())
        return res

    @ns.expect(_user_post, validate=True)
    @ns.marshal_with(_user)
    def post(self):
        """
            Create a new user
        """
        data = request.json
        user = User.create_user(data)
        # user.password = data['password']
        # return user
        return user


@ns.route('/<int:user_id>', methods=['GET', 'PUT'])
class UserByID(Resource):
    """
    Manipulations with a specific user.
    """

    @ns.marshal_with(_user)
    def get(self, user_id):
        """
        Get user details by ID.
        """
        return User.find(user_id)


@ns.route('/<string:username>', methods=['GET', 'PUT'])
class UserByUsernameOrEmail(Resource):
    """
    Manipulations with a specific user.
    """

    @ns.marshal_with(_user)
    def get(self, username):
        """
        Get user details by username or email
        """
        return User.find_by_username_or_email(username)