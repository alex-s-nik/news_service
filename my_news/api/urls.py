from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter

from .views import auth, news

router = SimpleRouter()

router.register('news', news.NewsViewSet, basename='news')
router.register('news/(?P<news_id>[^/.]+)/comments', news.CommentViewSet, basename='comments')

urlpatterns = [
    path('auth/login/', views.obtain_auth_token, name='login'),
    path('auth/logout/', auth.logout, name='logout'),
    path('', include(router.urls))
]