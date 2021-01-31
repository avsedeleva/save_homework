from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField('Текст публикации', help_text='Введите текст публикации')
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts')
    group = models.ForeignKey(Group, verbose_name='Группа',
                              blank=True, null=True,
                              on_delete=models.SET_NULL,
                              related_name='posts', help_text='Выберете группу')

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering = ['-pub_date']
