import datetime

from src.model import db


class Timestamp:
    """Adds `created_at` and `updated_at` columns to a derived declarative model.

    The `created_at` column is handled through a default and the `updated_at`
    column is handled through a `before_update` event that propagates
    for all derived declarative models.
    """
    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.DateTime(), default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime(), default=datetime.datetime.now, nullable=False)
