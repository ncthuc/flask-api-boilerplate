# coding=utf-8
import logging

from flask import request
from flask_restx import Resource, fields

from src.extensions.namespace import Namespace
from src.extensions.response_wrapper import wrap_response
from src.helpers import login_manager
from src.helpers.request_helper import RequestHelper
from src.helpers.response_helper import pagination
from src.model.user import User, UserSchema

__author__ = 'ThucNC'
_logger = logging.getLogger(__name__)

ns = Namespace('users', description='User operations')

_user = ns.model('user', UserSchema.user)
_user_post = ns.model('user_post', UserSchema.user_post)
_user_put = ns.model('user_put', UserSchema.user_put)
_metadata = ns.model('metadata', {
    'current_page': fields.Integer(),
    'page_size': fields.Integer(),
    'total_items': fields.Integer(),
    'next_page': fields.Integer(),
    'previous_page': fields.Integer(),
    'total_pages': fields.Integer()
})


@ns.route('/', methods=['GET', 'POST'])
@ns.route('/<string:username>', methods=['DELETE', 'PUT'])
class Users(Resource):
    @ns.expect(RequestHelper.add_pagination_params(), validate=True)
    @ns.marshal_with(_user, True, metadata=_metadata)
    @login_manager.required_roles('admin')
    @ns.doc(security='access-token')
    def get(self):
        """
            Get list of user
        """
        args = RequestHelper.add_pagination_params().parse_args()
        page = args['page']
        if page < 1:
            page = 1
        page_size = args['pageSize']
        _pagination = User.q().paginate(page=page, per_page=page_size, error_out=False)
        # print(get_debug_queries())
        print("_pagination:", _pagination)
        return {'data': _pagination.items,
                'metadata': pagination(page, page_size, _pagination.total)}

    @ns.marshal_with(_user)
    @ns.expect(_user_post, validate=True)
    @login_manager.required_roles('admin')
    @ns.doc(security='access-token')
    def post(self):
        """
            Create new user
        """
        data = request.json
        # user: User = flask_login.current_user
        return User.create(data)


@ns.route('/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
class UserSingle(Resource):
    """
    Manipulations with a specific user.
    """

    @ns.marshal_with(_user)
    @login_manager.required_roles('admin')
    @ns.doc(security='access-token')
    def get(self, user_id):
        """
        Get user details by ID.
        """
        user = User.get(user_id, error_out=True)
        return user

    @ns.marshal_with(_user)
    @ns.expect(_user_put, validate=True)
    @login_manager.required_roles('admin')
    @ns.doc(security='access-token')
    def put(self, user_id):
        """
            Update existed user
        """
        data = request.json
        user = User.get(user_id, error_out=True)
        user.update(data)
        return user

    @staticmethod
    @login_manager.required_roles('admin')
    @ns.doc(security='access-token')
    def delete(self, user_id):
        """
            Update existed user
        """
        user = User.get(user_id, error_out=True)
        user.delete()
        return wrap_response(None, 'ok', 200)
