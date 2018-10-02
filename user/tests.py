from graphene.test import Client
from django.test import TestCase


TEST_USER_USERNAME = '123456a'
TEST_USER_PASSWORD = '66666aaaa'
TEST_USER_EMAIL = '1@q.com'

def generate_test_user_form():
    return {
        'username' : TEST_USER_USERNAME,
        'password' : TEST_USER_PASSWORD,
        'email': TEST_USER_EMAIL
    }


# TODO(KeShen): Add unit tests for user model
class UserTestCase( TestCase ):
    pass
