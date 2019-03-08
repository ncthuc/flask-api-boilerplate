# coding=utf-8
import logging
import faker.providers
from src import model
from faker import Faker
import random

__author__ = 'Dan'
_logger = logging.getLogger(__name__)
fake = Faker()


class UserProvider(faker.providers.BaseProvider):
    @staticmethod
    def user(name=None, fullname=None, email=None, password=None, role=None,
             commit=False):
        """
        Fake an user in db for testing
        :return: user model object
        """
        user = model.User.create_user(
            {'username': name or fake.phone_number(),
             'fullname': fullname or fake.name(),
             'email': email or fake.email(),
             'password': password or fake.password(),
             'role': role or random.choice(['admin', 'moderator', 'viewer'])},
            commit=commit
        )
        return user

    @staticmethod
    def users(data=None, number=None):
        """
        Fake list of users
        :param list[dict] data:
        :param int number:
        :return: list user object
        """
        number = number or random.randint(2, 10)
        if not data:
            users = [UserProvider.user() for i in range(number)]
        else:
            users = [UserProvider.user(user_info) for user_info in data]
        model.db.session.commit()
        return users

