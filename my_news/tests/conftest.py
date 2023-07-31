import pytest

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from users.models import User


@pytest.fixture
def api_client_factory():
    def _wrapper(user: User|None=None):
        client = APIClient()
        if not user:
            return client
        token_user, _ = Token.objects.get_or_create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token_user}')
        return client
    return _wrapper

@pytest.fixture
def unauthorized_client():
    return APIClient()
