import datetime

from flask_restplus import fields

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


class UserSchema:
    user = {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password_hash': fields.String(required=False, description='user password hash'),
    }

    user_post = user.copy()
    user_post.update({
        'password': fields.String(required=True, description='user password'),
        'fullname': fields.String(required=False, description='user full name'),
        'image': fields.String(required=False, description='user avatar'),
        'role': fields.String(required=False, description='user role (admin | moderator | viewer)'),
    })
