import pytest

from rest_framework import status

from news.factories import CommentsFactory, NewsFactory
from news.models import Comment, News
from users.factories import AdminUserFactory, UserFactory

class Test_like:
    url_one_news = '/api/v1/news/%s/'
    url_news_for_like = '/api/v1/news/%s/like/'

    @pytest.mark.django_db()
    def test_to_like_news(self, api_client_factory):
        user = UserFactory.create()
        author = UserFactory.create()

        news = NewsFactory.create(author=author)

        user_client = api_client_factory(user)
        response = user_client.post(self.url_news_for_like % news.id)
        assert response.status_code == status.HTTP_201_CREATED

        response = user_client.get(self.url_one_news % news.id)
        assert response.json()['likes_count'] == 1, (
            'количество лайков у новости должно увеличиться'
        )

        response = user_client.post(self.url_news_for_like % news.id)
        assert response.status_code == status.HTTP_400_BAD_REQUEST, (
            'повторный лайк должен возвращать 400-й код'
        )
        response = user_client.get(self.url_one_news % news.id)
        assert response.json()['likes_count'] == 1, (
            'количество лайков у новости не должно измениться'
        )

        # анонимный запрос должен вох
        anonymous_client = api_client_factory()
        response = anonymous_client.post(self.url_news_for_like % news.id)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, (
            'лайк от неавторизованного пользователя должен возвращать 401-й код'
        )
        response = user_client.get(self.url_one_news % news.id)
        assert response.json()['likes_count'] == 1, (
            'количество лайков у новости не должно измениться'
        )




