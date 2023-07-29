
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from api.serializers import NewsSerializer
from news.models import News

from api.permissions import ReadAnonCreateAuthUpdateAdminOrAuthor

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = (ReadAnonCreateAuthUpdateAdminOrAuthor,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
