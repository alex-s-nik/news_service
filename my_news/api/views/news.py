from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import CommentSerializer, NewsSerializer
from news.models import Comment, News

from api.permissions import ReadAnonCreateAuthUpdateAdminOrAuthor


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
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
        curr_news = get_object_or_404(News, id=pk)
        liker = request.user
        if liker in curr_news.likes.all():
            return Response(
                'You have already likdes this news!',
                status=status.HTTP_400_BAD_REQUEST
            )
        curr_news.likes.add(liker)
        return Response(
            'You liked this news successfully',
            status=status.HTTP_201_CREATED
        )

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        news_id = self.kwargs.get('news_id')
        return get_object_or_404(News, pk=news_id).comments
    
    def perform_create(self, serializer):
        news_id = self.kwargs.get('news_id')
        curr_news = get_object_or_404(News, pk=news_id)
        serializer.save(author=self.request.user, news=curr_news)
