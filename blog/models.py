from datetime import datetime

from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def profile_directory_path(instance, filename):
    now = datetime.now().strftime('%d_%m_%y-%H : %M : %S')
    return f'profile\\{now}_{filename}'


def comment_directory_path(instance, filename):
    now = datetime.now().strftime('%d_%m_%y-%H : %M : %S')
    return f'comment\\{now}_{filename}'


def post_directory_path(instance, filename):
    now = datetime.now().strftime('%d_%m_%y-%H : %M : %S')
    return f'post\\{now}_{filename}'


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=25)
    body = models.TextField()
    image = models.ImageField(blank=True, upload_to=post_directory_path)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField('Category', related_name='posts', blank=True)
    profile = models.ForeignKey('Profile', verbose_name='User',
                                on_delete=models.CASCADE,
                                related_name='profile')

    def __str__(self):
        return self.title


@receiver(post_save, sender=Post, dispatch_uid="clear_cache_post")
def update_post(sender, **kwargs):
    key = make_template_fragment_key('post', [kwargs['instance'].profile.id])
    cache.delete(key)


class Comment(models.Model):
    author = models.CharField(max_length=60, blank=True)
    body = models.TextField()
    image = models.ImageField(upload_to=comment_directory_path, blank=True)
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
    avatar = models.ImageField(upload_to=profile_directory_path, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        permissions = (('deleteanotherscomment', "can delete another's comment"),)


@receiver(post_save, sender=Profile, dispatch_uid="clear_cache_profile")
def update_post(sender, **kwargs):
    key = make_template_fragment_key('account', [kwargs['instance'].user.id])
    cache.delete(key)
