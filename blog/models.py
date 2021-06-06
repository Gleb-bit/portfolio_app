from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


def user_directory_path(instance, filename):
    now = datetime.now().strftime('%d_%m_%y-%H:%M:%S')
    return f'{now}_{filename}'


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField('Category', related_name='posts')

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.CharField(max_length=60, blank=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=None, null=True, verbose_name='Пользователь', on_delete=models.CASCADE,
                             related_name='comments')

    def __str__(self):
        return self.author


class Profile(models.Model):
    user = models.OneToOneField(User, max_length=25, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    surname = models.CharField(max_length=25)
    about_me = models.TextField(blank=True)
    avatar = models.ImageField(upload_to=user_directory_path, blank=True)

    def __str__(self):
        return self.name
