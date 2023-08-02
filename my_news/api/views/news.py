from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.pagination import NewsPagination
from api.serializers import CommentSerializer, NewsSerializer
from api.services import news
from news.exceptions import AlreadyLikedException
from news.models import News

from api.permissions import ReadAnonCreateAuthUpdateAdminOrAuthor


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    pagination_class = NewsPagination
    permission_classes = (ReadAnonCreateAuthUpdateAdminOrAuthor,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


    @action(
        detail=True,
        methods=('post',),
        permission_classes=(IsAuthenticated,)
    )
    def like(self, request, pk=None):
        """Можно лайкать новость. Лайкать может любой залогиненный пользователь, в том числе и автор новости.
        При повторном лайке можно убирать уже поставленный лайк, но здесь, в этом случае реализовано
        уведомление об ошибке.
        """
        curr_news_id = pk
        liker = request.user
        try:
            news.like_news_by_liker(curr_news_id, liker)
        except AlreadyLikedException:
            return Response(
                'You have already liked this news!',
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            'You liked this news successfully',
            status=status.HTTP_201_CREATED
        )

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        news_id = self.kwargs.get('news_id')
        return news.get_all_comments_by_news_id(news_id)
    
    def perform_create(self, serializer):
        news_id = self.kwargs.get('news_id')
        curr_news = news.get_news_by_id(news_id)
        serializer.save(author=self.request.user, news=curr_news)
