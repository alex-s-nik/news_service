import pytest
from rest_framework import status

from api.serializers import LAST_COMMENTS_COUNT
from news.factories import CommentsFactory, NewsFactory
from news import models
from users.factories import AdminUserFactory, UserFactory
from users.models import User


class TestComments:
    url_one_news = '/api/v1/news/%s/'
    url_comments = '/api/v1/news/%s/comments/'
    url_one_comment = '/api/v1/news/%s/comments/%s/'

    @pytest.mark.django_db()
    def test_list_comments(self, api_client_factory):
        COMMENTS_COUNT = 15

        author = UserFactory.create()
        user = UserFactory.create()

        one_news = NewsFactory.create(author=author)

        CommentsFactory.create_batch(COMMENTS_COUNT, news=one_news)

        author_client = api_client_factory(author)
        user_client = api_client_factory(user)
        unauthorized_client = api_client_factory()

        for client in (user_client, author_client, unauthorized_client,):
            response = client.get(self.url_comments % one_news.id)

            assert response.status_code == status.HTTP_200_OK
            assert len(response.json()) == COMMENTS_COUNT

    @pytest.mark.django_db()
    def test_get_one_comment(self, api_client_factory):
        author = UserFactory.create()
        user = UserFactory.create()

        one_news = NewsFactory.create(author=author)

        comment = CommentsFactory.create(author=author, news=one_news)

        author_client = api_client_factory(author)
        user_client = api_client_factory(user)
        unauthorized_client = api_client_factory()

        for client in (user_client, author_client, unauthorized_client,):
            response = client.get(self.url_one_comment % (one_news.id, comment.id))

            assert response.status_code == status.HTTP_200_OK
            assert response.json()['id'] == str(comment.id)
            assert response.json()['author'] == author.username
            assert response.json()['text'] == comment.text
    
    @pytest.mark.django_db()
    def test_create_comment(self, api_client_factory):
        user = UserFactory.create()
        simple_news = NewsFactory.create(author=user)
        simple_comment = CommentsFactory.build()

        data = {
            'text': simple_comment.text
        }

        unauthorized_client = api_client_factory()
        response = unauthorized_client.post(self.url_comments % simple_news.id, data=data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_client = api_client_factory(user)
        response = user_client.post(self.url_comments % simple_news.id, data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'id' in response.json()
        assert 'created_at' in response.json()
        assert response.json()['author'] == user.username
        assert response.json()['text'] == simple_comment.text

    @pytest.mark.django_db()
    def test_news_with_comments(self, api_client_factory):
        COMMENTS_COUNT = 25
        user = UserFactory.create()
        simple_news = NewsFactory.create(author=user)

        user_client = api_client_factory(user)
        for i in range(COMMENTS_COUNT):
            comment = CommentsFactory.build()
            data = {
                'text': comment.text
            }

            user_client.post(self.url_comments % simple_news.id, data=data)
            
            response = user_client.get(self.url_one_news % simple_news.id)
            assert response.json()['comments_count'] == i + 1
            assert len(response.json()['last_comments']) == min(i + 1, LAST_COMMENTS_COUNT)

    def test_update():
        pass

    def test_delete():
        pass
