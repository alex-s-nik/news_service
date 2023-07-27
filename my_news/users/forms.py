from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        #fields = super().meta.fields + ('role',)
        fields = ("username", "email",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        models = User
        # fields = super().meta.fields + ('role',)
        fields = ("username", "email",)
