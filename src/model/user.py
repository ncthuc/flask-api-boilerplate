import datetime

from src.model import db, ma


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(191), nullable=False, unique=True)
    username = db.Column(db.String(191), nullable=False, unique=True)
    fullname = db.Column(db.String(191), nullable=False)
    status = db.Column(db.Integer, default=1)
    id_token = db.Column(db.String(512), nullable=True)
    image = db.Column(db.Text(), nullable=True)
    role = db.Column(db.Enum('admin', 'moderator', 'viewer'),
                     nullable=False, default='viewer')
    last_login = db.Column(db.DateTime(), default=datetime.datetime.now)
    created_at = db.Column(db.DateTime(), default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime(), default=datetime.datetime.now)

    def __init__(self, username, email, status=None, image=None):
        self.name = username
        self.email = email
        self.status = status
        self.image = image

    def get_id(self):
        return self.id

    @property
    def is_authenticated(self):
        return True


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'image', 'last_login')