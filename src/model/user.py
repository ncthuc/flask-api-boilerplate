import datetime
import secrets

import requests
from flask import request
from flask_restx import fields
from sqlalchemy import or_
from werkzeug.exceptions import Conflict, Unauthorized, BadRequest

from src.helpers.datetime_helper import now_plus_30_days
from src.helpers.request_helper import RequestHelper
from src.model import db, bcrypt
from src.model.base_model import BaseModel


GG_OAUTH2_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token="


class User(BaseModel):
    email = db.Column(db.String(191), nullable=False, unique=True)
    username = db.Column(db.String(191), nullable=False, unique=True)
    fullname = db.Column(db.String(191), nullable=False)
    status = db.Column(db.Integer, default=1)
    password_hash = db.Column(db.String(100))
    id_token = db.Column(db.String(512), nullable=True)
    image = db.Column(db.Text(), nullable=True)
    role = db.Column(db.Enum('admin', 'moderator', 'viewer'),
                     nullable=False, default='viewer')
    last_login = db.Column(db.DateTime(), default=datetime.datetime.now)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.id

    @property
    def is_authenticated(self):
        return True

    @staticmethod
    def get_logged_in_user(req=None, raise_on_error=True):
        if not req:
            req = request
        access_token = req.headers.get('access-token')
        if access_token:
            token = UserToken.first(UserToken.token == access_token)
            if token:
                return User.get(token.user_id)
        if raise_on_error:
            raise Unauthorized("Unauthorized")
        return None

    @staticmethod
    def login_with_email_or_username(email, password):
        access_token = secrets.token_hex(16)
        user: User = User.find_by_username_or_email(email)
        if not user:
            raise Unauthorized('Bad username and/or password')
        if not user.password_hash:
            raise BadRequest("Account haven't set password")
        if user.check_password(password):
            # user.update_user(email, {'token': token, 'email': email})
            # UserToken.delete_token_by_user_id(user.id)
            UserToken.create(data={'token': access_token, 'user_id': user.id})
            return access_token
        raise Unauthorized('Email or Password not correct')

    @staticmethod
    def login_with_google_token(google_token):
        verify_token = requests.get(GG_OAUTH2_USER_INFO_URL + google_token)
        user_info = verify_token.json()
        print(user_info)
        hd = user_info.get('hd')
        # if not hd or hd not in ['studyland.edu.vn', 'ucode.vn']:
        #     raise Unauthorized('Unauthorized email domain')

        email = user_info.get('email')
        name = user_info.get('name')

        user = User.find_by_username_or_email(email, raise_error=False)
        access_token = secrets.token_hex(16)
        if not user:
            data = {
                'email': email,
                'username': email,
                'fullname': name,
                'image':user_info.get('picture')
            }
            user = User.create(data)
        UserToken.create({'token': access_token, 'user_id': user.id})
        return access_token

    @staticmethod
    def logout():
        access_token = request.headers.get('access-token')
        UserToken.delete_token(access_token)

    @staticmethod
    def create_user(data, commit=False):
        new_user = User(**data)
        db.session.add(new_user)
        if commit:
            db.session.commit()
        else:
            db.session.flush()
        return new_user

    @staticmethod
    def update_user(username, data):
        user = db.session.query(User).filter(User.username == username).first_or_404()
        if data['email'] != user.email:
            conflict = User.query.filter(User.email == data['email']).first()
            if conflict:
                raise Conflict('Email %s is existed' % data['email'])
        for key, value in data.items():
            setattr(user, key, value)
        db.session.flush()
        return user

    @staticmethod
    def delete_user(username):
        user: User = db.session.query(User).filter(User.username == username).first_or_404()
        user.delete()
        db.session.flush()

    @staticmethod
    def find_by_username_or_email(username, raise_error=True):
        """
        Args:
            username (str)

        Returns:
            user (User) - if there is a user with a specified username and
            password, None otherwise.
        """
        user_query = User.query.filter(or_(User.username==username, User.email==username))
        if raise_error:
            return user_query.first_or_404()
        return user_query.first()

    @staticmethod
    def find_by_email(email):
        """
        Args:
            email (str)

        Returns:
            user (User) - if there is a user with a specified username and
            password, None otherwise.
        """
        user = User.query.filter_by(email=email).first()
        if not user:
            return None
        return user


class UserToken(BaseModel):
    token = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    expired_at = db.Column(db.DateTime, default=now_plus_30_days)
    ip_address = db.Column(db.String(64), default=RequestHelper.get_remote_ip)
    user_agent = db.Column(db.String(1024), default=RequestHelper.get_user_agent)

    @staticmethod
    def delete_token(token):
        obj_token = UserToken.first(UserToken.token == token)
        if obj_token:
            obj_token.delete()

    @staticmethod
    def delete_token_by_user_id(user_id):
        UserToken.q(UserToken.user_id == user_id).delete()


class UserSchema:
    user = {
        'id': fields.Integer(required=True, description='user _id'),
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'fullname': fields.String(required=False, description='user full name'),
        'image': fields.String(required=False, description='user avatar'),
        'role': fields.String(required=False, description='user role (admin | moderator | viewer)',
                              enum=['admin', 'moderator', 'viewer']),
        # 'password_hash': fields.String(required=False, description='user password hash'),
    }

    user_post = user.copy()
    user_post.pop('id', None)
    user_post.update({
        'password': fields.String(required=True, description='user password'),
    })

    user_put = user_post.copy()
    user_put.pop('username', None)
    user_put.pop('password', None)
