import uuid

from django.shortcuts import get_object_or_404

from news.exceptions import AlreadyLikedException
from news.models import News
from users.models import User


def get_news_by_id(news_id: uuid.uuid4):
    """Вернуть новость по id."""
    return get_object_or_404(News, id=news_id)


def like_news_by_liker(curr_news_id: uuid.uuid4, liker: User):
    """Лайкнуть новость пользователем."""
    curr_news = get_news_by_id(curr_news_id)

    if liker in curr_news.likes.all():
        raise AlreadyLikedException

    curr_news.likes.add(liker)


def get_all_comments_by_news_id(news_id: uuid.uuid4):
    """Вернуть все комментарии новости по ее id."""
    curr_news = get_news_by_id(news_id)
    return curr_news.comments
