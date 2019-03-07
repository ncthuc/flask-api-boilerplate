import datetime

from flask_restplus import fields
from sqlalchemy import or_
from werkzeug.exceptions import NotFound, Conflict

from src.model import db, bcrypt
from src.model.base_model import Timestamp


class User(db.Model, Timestamp):
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
    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in
                self.__table__.columns}

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
        user = db.session.query(User).filter(User.username == username).first_or_404()
        db.session.delete(user)
        db.session.flush()

    @staticmethod
    def find(user_id):
        """
        Args:
            user_id (int)

        Returns:
            user (User) - if there is a user with a specified username and
            password, None otherwise.
        """
        user = User.query.get(user_id)
        if not user:
            raise NotFound("User id not found: {}".format(user_id))
        return user

    @staticmethod
    def find_by_username_or_email(username):
        """
        Args:
            user_id (int)

        Returns:
            user (User) - if there is a user with a specified username and
            password, None otherwise.
        """
        user = User.query.filter(or_(User.username==username, User.email==username)).first_or_404()
        return user

    @staticmethod
    def find_by_email(email):
        """
        Args:
            user_id (int)

        Returns:
            user (User) - if there is a user with a specified username and
            password, None otherwise.
        """
        user = User.query.filter_by(email=email).first()
        if not user:
            return None
        return user


class UserSchema:
    user = {
        'id': fields.Integer(required=True, description='user id'),
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'fullname': fields.String(required=False, description='user full name'),
        'image': fields.String(required=False, description='user avatar'),
        'role': fields.String(required=False, description='user role (admin | moderator | viewer)'),
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
