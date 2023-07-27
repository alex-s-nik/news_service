import pytest

from users.models import User

class TestModelRole:
    @pytest.mark.parametrize('method,data,expected_role', [
        (
            User.objects.create_user,
            {
                'username': 'test_username',
                'email': 'test_mail@fake.com',
                'password': 'test_pass'
            },
            User.USER_ROLE
        ),
        (
            User.objects.create_user,
            {
                'username': 'test_username',
                'email': 'test_mail@fake.com',
                'password': 'test_pass',
                'role': User.ADMIN_ROLE
            },
            User.ADMIN_ROLE
        ),
        (User.objects.create_superuser, {
            'username': 'test_username',
            'email': 'test_mail@fake.com',
            'password': 'test_pass'
        }, User.ADMIN_ROLE)
    ])
    @pytest.mark.django_db()
    def test_role_while_created(self, method, data, expected_role):
        
        user = method(**data)
        assert user.role == expected_role
