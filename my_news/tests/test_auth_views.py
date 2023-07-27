import pytest
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def username_n_password():
    return {
            'username': 'test',
            'password': 'test_password'
        }

@pytest.fixture
def test_user(django_user_model, username_n_password):
    user = django_user_model.objects.create_user(**username_n_password)
    return user

@pytest.fixture
def test_user_token(test_user):
    token, _ = Token.objects.get_or_create(user=test_user)
    return token


class TestAuth:
    login_url = '/api/v1/auth/login/'
    logout_url = '/api/v1/auth/logout/'

    @pytest.mark.parametrize(
        'status_code,credential_data,content_part', [
            (
                status.HTTP_200_OK,
                {
                    'username': 'test',
                    'password': 'test_password'
                },
                'token'),
            (
                status.HTTP_400_BAD_REQUEST,
                {
                    'username': 'wrong_username',
                    'password': 'test_password'
                },
                'non_field_errors'
            ),
            (
                status.HTTP_400_BAD_REQUEST,
                {
                    'username': 'test',
                    'password': 'wrong_password'
                },
                'non_field_errors'
            ),
            (
                status.HTTP_400_BAD_REQUEST,
                {
                    'username': 'wrong_username',
                    'password': 'wrong_password'
                },
                'non_field_errors'
            )
        ]
    )
    @pytest.mark.django_db()
    def test_login(self, api_client, test_user, status_code, credential_data, content_part):
        response = api_client.post(self.login_url, data=credential_data)
        assert response.status_code == status_code
        assert content_part in response.json()

    @pytest.mark.django_db()
    def test_logout(self, api_client, test_user, test_user_token):
        # проверка logout без токена
        response = api_client.post(self.logout_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # проверка logout с неправильным токеном
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {test_user_token}1')
        response = api_client.post(self.logout_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # проверка logout с правильным токеном
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {test_user_token}')
        response = api_client.post(self.logout_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
