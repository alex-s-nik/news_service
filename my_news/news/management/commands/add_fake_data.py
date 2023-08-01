from django.core.management.base import BaseCommand

from news.factories import CommentsFactory, NewsFactory
from users.factories import UserFactory

class Command(BaseCommand):
    help = "Adds a fake data into database."

    def handle(self, *args, **options):
        USERS_COUNT = 10
        NEWS_COUNT = 50
        COMMENTS_COUNT = 300

        UserFactory.create_batch(USERS_COUNT)
        NewsFactory.create_batch(NEWS_COUNT)
        CommentsFactory.create_batch(COMMENTS_COUNT)
