import pytest
from rest_framework import status

from news.factories import NewsFactory
from news.models import News
from users.factories import AdminUserFactory, UserFactory
from users.models import User

class TestNews:
    url_news = '/api/v1/news/'
    url_one_news = '/api/v1/news/%s/'


    @pytest.mark.django_db()
    def test_list_news(self, api_client_factory, unauthorized_client):
        NEWS_COUNT = 20

        author = UserFactory.create()
        user = UserFactory.create()

        NewsFactory.create_batch(NEWS_COUNT, author=author)

        author_client = api_client_factory(author)
        user_client = api_client_factory(user)

        for client in (user_client, author_client, unauthorized_client,):
            response = client.get(self.url_news)

            assert response.status_code == status.HTTP_200_OK
            assert response.json()['count'] == NEWS_COUNT

    @pytest.mark.django_db()
    def test_get_one_news(self, api_client_factory, unauthorized_client):
        author = UserFactory.create()
        user = UserFactory.create()

        simple_news = NewsFactory.create(author=author)

        author_client = api_client_factory(author)
        user_client = api_client_factory(user)

        for client in (user_client, author_client, unauthorized_client,):
            response = client.get(self.url_one_news % simple_news.id)

            assert response.status_code == status.HTTP_200_OK
            assert response.json()['id'] == str(simple_news.id)
            assert response.json()['author'] == author.username
            assert response.json()['title'] == simple_news.title
            assert response.json()['text'] == simple_news.text
            assert response.json()['comments_count'] == 0
            assert response.json()['likes_count'] == 0
            assert response.json()['last_comments'] == []

    @pytest.mark.django_db()
    def test_create_news(self, api_client_factory, unauthorized_client):
        user = UserFactory.create()

        user_client = api_client_factory(user)

        simple_news = NewsFactory.build()

        news_data = {
            key: simple_news.__dict__[key] for key in simple_news.__dict__ if key not in ('created_at',)
        }

        response = unauthorized_client.post(self.url_news, data=news_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = user_client.post(self.url_news, data=news_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'id' in response.json()
        assert response.json()['author'] == user.username
        assert response.json()['title'] == simple_news.title
        assert response.json()['text'] == simple_news.text
        assert response.json()['comments_count'] == 0
        assert response.json()['likes_count'] == 0
        assert response.json()['last_comments'] == []

    @pytest.mark.django_db()
    def test_update_news(self):
        pass

    @pytest.mark.parametrize(
        'type_client, status_code, count_news_after_response', [
            ('admin', status.HTTP_204_NO_CONTENT, 0),
            ('author', status.HTTP_204_NO_CONTENT, 0),
            ('other_user', status.HTTP_403_FORBIDDEN, 1),
            ('anonymous', status.HTTP_401_UNAUTHORIZED, 1),

        ]
    )
    @pytest.mark.django_db()
    def test_delete_news(self, api_client_factory, type_client, status_code, count_news_after_response):
        author = UserFactory.create()
        simple_news = NewsFactory.create(author=author)

        if type_client == 'admin':
            user = AdminUserFactory.create()
        elif type_client == 'author':
            user = author
        elif type_client == 'other_user':
            user = UserFactory.create()
        elif type_client == 'anonymous':
            user = None
        else:
            raise KeyError('Тестирование такого типа клиента не предусмотрено.')
        
        client = api_client_factory(user)
        response = client.delete(self.url_one_news % simple_news.id)

        assert response.status_code == status_code
        assert News.objects.count() == count_news_after_response
