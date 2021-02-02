import pytest
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


@pytest.fixture(scope="function")
def api_client():
    api_client = APIClient()
    return api_client


@pytest.fixture(scope="function")
def add_admin_token(django_user_model):
    def _add_admin_token():
        user = django_user_model.objects.create(
            username="superuser", password="123", is_staff=True
        )
        token = Token.objects.create(user=user)
        return token

    return _add_admin_token


@pytest.fixture(scope="function")
def add_user_token(django_user_model):
    def _add_user_token():
        user = django_user_model.objects.create(username="user", password="123")
        token = Token.objects.create(user=user)
        return token

    return _add_user_token
