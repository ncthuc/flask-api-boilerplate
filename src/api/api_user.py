# coding=utf-8
import logging

from flask import request
from flask_restplus import Resource, fields

from src.extensions.namespace import Namespace
from src.extensions.response_wrapper import wrap_response
from src.helpers.request_helper import RequestHelper
from src.model.user import User, UserSchema
from werkzeug.exceptions import Conflict

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
@ns.route('/<int:username>', methods=['DELETE', 'PUT'])
class Users(Resource):
    @ns.expect(RequestHelper.get_list_user_arguments(), validate=True)
    @ns.marshal_with(_user, True, metadata=_metadata)
    def get(self):
        """
            Get list of user
        """
        args = RequestHelper.get_list_user_arguments().parse_args()
        page = args['page']
        page_size = args['pageSize']
        res = User.query.offset((page - 1) * page_size).limit(page_size).all()
        # print(flask_sqlalchemy.get_debug_queries())
        return {'data': res,
                'metadata': Users.pagination(page, page_size, len(res))}

    @ns.expect(_user_post, validate=True)
    @ns.marshal_with(_user)
    def post(self):
        """
            Create a new user
        """
        data = request.json
        user = User.query.filter(User.username == data['username']).first()
        if user:
            raise Conflict('Username %s is existed' % data['username'])
        user = User.create_user(data)
        return user

    @staticmethod
    def pagination(page, page_size, total_items):
        """
        Pagination for creating metadata
        """
        total_pages = total_items // page_size if total_items % page_size == 0 \
            else (total_items // page_size) + 1
        next_page = page + 1 if page < total_pages - 1 else None
        previous_page = page - 1 if page > 1 else None
        return {
            'current_page': page,
            'page_size': page_size,
            'total_items': total_items,
            'next_page': next_page,
            'previous_page': previous_page,
            'total_pages': total_pages
        }


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


@ns.route('/<string:username>', methods=['GET', 'PUT', 'DELETE'])
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

    @ns.marshal_with(_user)
    @ns.expect(_user_put, validate=True)
    def put(self, username):
        """
            Update existed user
        """
        data = request.json
        user = User.update_user(username, data)
        return user

    @staticmethod
    def delete(username):
        """
            Update existed user
        """
        User.delete_user(username)
        return wrap_response(None, 'ok', 200)
