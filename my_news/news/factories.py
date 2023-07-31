import factory
from factory import fuzzy

from users.factories import UserFactory
from users.models import User
from .models import Comment, News


class NewsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = News
    
    title = factory.Faker('sentence', locale='ru_RU', nb_words=2)
    text = factory.Faker('paragraph', locale='ru_RU', nb_sentences=3, variable_nb_sentences=False)
    author = fuzzy.FuzzyChoice(User.objects.all())


class CommentsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    text = factory.Faker('paragraph', locale='ru_RU', nb_sentences=3, variable_nb_sentences=False)
    news = fuzzy.FuzzyChoice(News.objects.all())
    author = fuzzy.FuzzyChoice(User.objects.all())
