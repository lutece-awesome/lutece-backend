from django.test import RequestFactory
from graphene.test import Client

from Lutece.schema import schema
from user.attachinfo.models import AttachInfo
from user.models import User


def create_mock_user(username: str, password: str) -> User:
    attach_info = AttachInfo.objects.create()
    return User.objects.create(
        username=username,
        password=password,
        attach_info=attach_info
    )


def get_test_graphql_client() -> Client:
    return Client(schema)


def get_query_context() -> RequestFactory:
    return RequestFactory()
