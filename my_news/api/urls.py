from django.urls import path
from rest_framework.authtoken import views

from .views import auth

urlpatterns = [
    path('auth/login/', views.obtain_auth_token, name='login'),
    path('auth/logout/', auth.logout, name='logout')
]