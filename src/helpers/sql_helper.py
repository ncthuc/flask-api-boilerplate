import flask_sqlalchemy


def get_debug_queries():
    return flask_sqlalchemy.get_debug_queries()