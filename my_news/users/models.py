from typing import Iterable, Optional
from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    """У каждого пользователя может быть две роли – пользователь и админ, админ может зайти в админ-панель, пользователь – нет.
    Каждый пользователь может создать новость. Все пользователи могут получать списки всех новостей с пагинацией. 
    Пользователи могут удалять и изменять свои новости. Админ может удалять и изменять любую новость.
    Лайкать и комментировать может любой пользователь, автор может удалять комментарии к своим новостям, админ может удалять любые комментарии.
    """
    USER_ROLE = 'user'
    ADMIN_ROLE = 'admin'

    ROLE_CHOICES = (
        (USER_ROLE, 'Пользователь'),
        (ADMIN_ROLE, 'Администратор')
    )

    role = models.CharField(
        verbose_name='Роль пользователя',
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER_ROLE
    )

    def save(self, *args, **kwargs) -> None:
        if self.is_superuser:
            self.role = User.ADMIN_ROLE
        return super().save(*args, **kwargs)

    @property
    def is_admin(self) -> bool:
        return self.is_superuser or self.role == User.ADMIN_ROLE