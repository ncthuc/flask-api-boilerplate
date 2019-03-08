# coding=utf-8
import logging
import faker.providers
from tests.faker.user_provider import UserProvider

__author__ = 'Dan'
_logger = logging.getLogger(__name__)

fake = faker.Faker()
fake.add_provider(UserProvider)
