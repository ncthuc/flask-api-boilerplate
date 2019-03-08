# coding=utf-8
import logging
import pytest
from tests.faker import fake

__author__ = 'Dan'
_logger = logging.getLogger(__name__)


def get_users_pagination(page, page_size, users):
    def get_subset_dict(a_dict):
        return {k: a_dict[k]
                for k in ['id', 'username', 'fullname', 'role', 'image', 'email']}

    users_info = [get_subset_dict(user.to_dict) for user in users]
    return users_info[(page - 1) * page_size: page * page_size]


@pytest.mark.parametrize('number_users', [7, 15])
def test_api_get_list_user_without_params(number_users, app):
    """
    Assume: database has N users, call api without params page, pagesize
    Expect: get list users with default page=1, pagesize=10
    :return:
    """
    users = fake.users(number=number_users)
    client = app.test_client()
    resp = client.get('/users/').json
    assert resp['success']
    assert get_users_pagination(1, 10, users) == resp['data']


def test_api_get_list_user_with_invalid_params(app):
    """
    Assume: call api with invalid params page = -1
    Expect: response success = false
    :return:
    """
    client = app.test_client()
    resp = client.get('/users/?page=-1&pagesize=2').json
    assert not resp['success']


@pytest.mark.parametrize('number_users, page, page_size',
                         [(7, 1, 10), (7, 2, 10), (15, 1, 10), (15, 2, 10)])
def test_api_get_list_user_with_valid_params(app, number_users, page, page_size):
    """
   Assume: database has N users, call api with params page, pagesize
   Expect: list returned users are correct with corresponding page, pagesize
   :return:
   """
    users = fake.users(number=number_users)
    client = app.test_client()
    resp = client.get('/users/?page=%s&pagesize=%s' % (page, page_size)).json
    assert resp['success']
    assert get_users_pagination(page, page_size, users) == resp['data']


# def test_api_create_user_with_invalid_params():
#     pass
#
#
# def test_api_create_user_success():
#     pass
#
#
# def test_api_get_user_detail_by_correct_id():
#     pass
#
#
# def test_api_get_user_detail_by_id_not_found():
#     pass
#
#
# def test_api_find_user_by_username_email_not_found():
#     pass
#
#
# def test_api_find_user_by_correct_username_email():
#     pass
