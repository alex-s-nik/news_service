import pytest

from users.factories import AdminUserFactory, UserFactory
from users.models import User

class TestModelRole:
    @pytest.mark.parametrize('user_factory, data, expected_role', [
        (
            UserFactory,
            {},
            User.USER_ROLE
        ),
        (
            UserFactory,
            {'role': User.ADMIN_ROLE},
            User.ADMIN_ROLE
        ),
        (
            AdminUserFactory,
            {},
            User.ADMIN_ROLE
        )
    ]
            
    )
    @pytest.mark.django_db()
    def test_role(self, user_factory,data, expected_role):
        user = user_factory.create(**data)
        assert user.role == expected_role
