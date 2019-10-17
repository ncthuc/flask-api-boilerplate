# coding=utf-8
import logging
import pytest
from src import model

__author__ = 'Dan'
_logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def app(request):
    """
    Establish an application context before running the tests.
    Create app fixture for test, declare as function argument at any
    test case you want to use it
    :param request:
    :return: flask app
    """
    from app import app

    ctx = app.app_context()
    ctx.push()
    model.db.create_all()

    def teardown():
        model.db.session.remove()
        model.db.drop_all()
        ctx.pop()

    request.addfinalizer(teardown)
    return app
