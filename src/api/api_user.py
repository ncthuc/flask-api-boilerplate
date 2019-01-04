# coding=utf-8
import logging

from flask import request
from flask_restplus import Resource

from src.extensions.namespace import Namespace
from src.extensions.response_wrapper import wrap_response
from src.helpers.request_helper import RequestHelper
from src.model.user import User, UserSchema

__author__ = 'ThucNC'
_logger = logging.getLogger(__name__)

ns = Namespace('user', description='User operations')

_user = ns.model('user', UserSchema.user)
_user_post = ns.model('user_post', UserSchema.user_post)


@ns.route('', methods=['GET', 'POST'])
class UserApi(Resource):
    """
    Hello world api
    """
    @ns.expect(RequestHelper.pagination_params, validate=True)
    def get(self):
        _logger.warn('User API: {}')
        args = RequestHelper.pagination_params.parse_args()
        # args = request.args
        return wrap_response(args, 'ok', 200)

    @ns.doc(description='Create an user')
    @ns.expect(_user_post, validate=True)
    @ns.marshal_list_with(_user)
    def post(self):
        data = request.json
        user = User(**data)
        # user.password = data['password']
        # return user
        return [user]

