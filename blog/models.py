from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


def user_directory_path(instance, filename):
    now = datetime.now().strftime('%d_%m_%y-%H:%M:%S')
    return f'{now}_{filename}'


class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name='название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'


class Post(models.Model):
    title = models.CharField(max_length=25, verbose_name='название')
    body = models.TextField(verbose_name='тело')
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    last_modified = models.DateTimeField(auto_now=True, verbose_name='редактирован')
    categories = models.ManyToManyField('Category', related_name='posts', blank=True, )
    user = models.ForeignKey('Profile', verbose_name='User',
                             on_delete=models.CASCADE,
                             related_name='profile')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'


class Comment(models.Model):
    author = models.CharField(max_length=60, blank=True, verbose_name='автор')
    body = models.TextField(verbose_name='тело')
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=None, null=True, verbose_name='Пользователь', on_delete=models.CASCADE,
                             related_name='comments')

    def __str__(self):
        return self.author

    class Meta:
        verbose_name = 'Комментарий'


class Profile(models.Model):
    user = models.OneToOneField(User, max_length=25, on_delete=models.CASCADE)
    name = models.CharField(max_length=25, verbose_name='имя')
    surname = models.CharField(max_length=25, verbose_name='фамилия')
    about_me = models.TextField(blank=True, verbose_name='обо мне')
    avatar = models.ImageField(upload_to=user_directory_path, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        permissions = (('deleteanotherscomment', "can delete another's comment"),)
        verbose_name = "Профиль"
