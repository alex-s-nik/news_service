import uuid

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseModel(models.Model):
    """Базовая модель с uuid в роли id, текстом, датой создания и автором."""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    author = models.ForeignKey(
        verbose_name='Автор',
        to=User,
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        abstract = True


class News(BaseModel):
    """Модель новости.
    У новости есть дата создания новости, заголовок, текст и автор.
    Также новость может лайкнуть другой пользователь.
    """
    title = models.CharField(
        verbose_name='Заголовок новости',
        max_length=100,

    )
    likes = models.ManyToManyField(
        verbose_name='Пользователи, лайкнувшие новость',
        to=User,
        related_name='all_news',
    )

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
    
    def __str__(self) -> str:
        return self.title


class Comment(BaseModel):
    """Модель комментария к новости."""
    news = models.ForeignKey(
        to=News,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        CUT_CHAR_OF_TEXT = 15
        CUT_CHAR_OF_TITLE = 15
        return (f'{self.author} написал "{self.text[:CUT_CHAR_OF_TEXT]}" '
                f'о новости "{self.news.title[:CUT_CHAR_OF_TITLE]}".')
