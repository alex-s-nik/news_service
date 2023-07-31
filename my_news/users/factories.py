import factory

from .models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('email')
    username = factory.Faker('user_name')
    password = factory.PostGenerationMethodCall('set_password', 'adm1n')
    is_staff = factory.Faker('pybool')
    is_active = True


class AdminUserFactory(UserFactory):
    is_superuser = False
    role = User.ADMIN_ROLE
