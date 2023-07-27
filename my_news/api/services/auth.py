from rest_framework.authtoken.models import Token

from news.models import User

def logout_user(user: User) -> None:
    Token.objects.filter(user=user).delete()
