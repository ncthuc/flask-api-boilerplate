import datetime

from werkzeug.exceptions import NotFound

from src.model import db


class BaseModel(db.Model):
    """Adds `created_at` and `updated_at` columns to a derived declarative model.

    The `created_at` column is handled through a default and the `updated_at`
    column is handled through a `before_update` event that propagates
    for all derived declarative models.
    """

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.DateTime(), default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime(), default=datetime.datetime.now, nullable=False)

    @property
    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in
                self.__table__.columns}

    @classmethod
    def get(cls, _id, raise_not_found=False):
        """
        Find model object by id
        :param int _id:
        :param raise_not_found:
        :return:
        """
        obj = cls.query.get(_id)
        if not obj and raise_not_found:
            raise NotFound("{} id `{}` is not found".format(cls.__name__, _id))
        return obj

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

    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.commit()
        else:
            db.session.flush()
