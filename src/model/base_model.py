import datetime

from flask_restx import fields
from sqlalchemy import func
from werkzeug.exceptions import NotFound

from src.model import db


metadata_scheme = {
    'current_page': fields.Integer(),
    'page_size': fields.Integer(),
    'total_items': fields.Integer(),
    'next_page': fields.Integer(),
    'previous_page': fields.Integer(),
    'total_pages': fields.Integer()
}


class BareBaseModel(db.Model):
    __abstract__ = True

    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

    @classmethod
    def max(cls, field):
        """
        Sample: User.max(User.id)
        :param field:
        :return: int, None if no records
        """
        return cls.scalar('max', field)

    @classmethod
    def scalar(cls, _func, field):
        """
        Sample: User.scalar('max', User.id)
        :param field:
        :return: int, None if no records
        """
        func_to_call = getattr(func, _func)
        return db.session.query(func_to_call(field)).scalar()

    @classmethod
    def q(cls, *criterion):
        """
        Filter by criterion, ex: User.q(User.name=='Thuc', User.status==1)
        :param criterion:
        :return:
        """
        if criterion:
            return cls.query.filter(*criterion)
        return cls.query

    @classmethod
    def q_by(cls, **kwargs):
        """
        Filter by named params, ex: User.q(name='Thuc', status=1)
        :param kwargs:
        :return:
        """
        return cls.query.filter_by(**kwargs)

    @classmethod
    def first(cls, *criterion):
        """
        Get first by list of criterion, ex: user1 = User.first(User.name=='Thuc1')
        :param criterion:
        :return:
        """
        res = cls.q(*criterion).first()
        return res

    @classmethod
    def first_or_error(cls, *criterion):
        res = cls.first(*criterion)
        if not res:
            raise NotFound("Obj {} is not found".format(cls.__name__))
        return res

    @classmethod
    def first_by(cls, **kwargs):
        """
        Get first by named params, ex: user1 = User.first_by(name='Thuc1')
        :return:
        """
        res = cls.q_by(**kwargs).first()
        return res

    @classmethod
    def first_by_or_error(cls, **kwargs):
        res = cls.first_by(**kwargs)
        if not res:
            raise NotFound("Obj {} is not found".format(cls.__name__))
        return res

    @classmethod
    def get(cls, _id, error_out=False):
        """
        Find model object by id
        :param int _id:
        :param error_out:
        :return:
        :rtype: cls
        """
        obj = cls.query.get(_id)
        if not obj and error_out:
            raise NotFound("{} id `{}` is not found".format(cls.__name__, _id))
        return obj

    @classmethod
    def get_or_error(cls, _id):
        return cls.get(_id, True)

    @classmethod
    def create(cls, data, commit=False):
        """
        Create new model object with given dict `data`
        :param dict data:
        :param commit:
        :return:
        """
        new_obj = cls(**data)
        db.session.add(new_obj)
        if commit:
            db.session.commit()
        else:
            db.session.flush()
        return new_obj

    def update(self, data, commit=False, exclude=None):
        """
        Update current model object with given dict `data`
        :param data: dict
        :param commit:
        :param exclude: list of key to exclude from `data` dict
        :return:
        """
        for key, value in data.items():
            if not exclude or key not in exclude:
                setattr(self, key, value)

        if commit:
            db.session.commit()
        else:
            db.session.flush()

        return self

    def delete(self, commit=False):
        db.session.delete(self)
        if commit:
            db.session.commit()
        else:
            db.session.flush()


class BaseModel(BareBaseModel):
    """Adds `created_at` and `updated_at` columns to a derived declarative model.

    The `created_at` column is handled through a default and the `updated_at`
    column is handled through a `before_update` event that propagates
    for all derived declarative models.
    """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

