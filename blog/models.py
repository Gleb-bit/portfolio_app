from datetime import datetime

from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


def profile_directory_path(instance, filename):
    now = datetime.now().strftime('%d_%m_%y-%H : %M : %S')
    return f'profile/{now}_{filename}'


def comment_directory_path(instance, filename):
    now = datetime.now().strftime('%d_%m_%y-%H : %M : %S')
    return f'comment/{now}_{filename}'


def post_directory_path(instance, filename):
    now = datetime.now().strftime('%d_%m_%y-%H : %M : %S')
    return f'post/{now}_{filename}'


class Category(models.Model):
    """
    Return a category
    """
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'


class Post(models.Model):
    """
    Return a post with certain fields. Profile can have multiple posts.
    One post can have multiple categories, such as one category can have multiple posts
    """
    title = models.CharField(max_length=25)
    body = models.TextField()
    image = models.ImageField(blank=True, upload_to=post_directory_path, null=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category, related_name='posts', blank=True)
    profile = models.ForeignKey('Profile', verbose_name='User',
                                on_delete=models.CASCADE,
                                related_name='posts')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


@receiver(post_save, sender=Post, dispatch_uid="clear_cache_post")
def update_post(sender, instance, **kwargs):
    user_key = instance.profile.user.id
    for language in ('en', 'ru'):
        key = make_template_fragment_key('post', [user_key, instance.pk, language])
        cache.delete(key)


class Comment(models.Model):
    """
    Return a comment with certain fields. Post can have multiple comments, and so can the user
    """
    author = models.CharField(max_length=60, blank=True)
    body = models.TextField()
    image = models.ImageField(upload_to=comment_directory_path, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, default=None, null=True, verbose_name='Пользователь', on_delete=models.CASCADE,
                             related_name='comments')

    def __str__(self):
        return self.author

    class Meta:
        ordering = ['author']


@receiver(post_save, sender=Comment, dispatch_uid="clear_cache_comment")
def update_comment(sender, instance, **kwargs):
    user_key = instance.user.id if instance.user else None
    for language in ('en', 'ru'):
        key = make_template_fragment_key('post', [user_key, instance.post.pk, language])
        cache.delete(key)


@receiver(post_delete, sender=Comment, dispatch_uid="clear_cache_comment")
def delete_comment(sender, instance, **kwargs):
    user_key = instance.user.id if instance.user else None
    for language in ('en', 'ru'):
        key = make_template_fragment_key('post', [user_key, instance.post.pk, language])
        cache.delete(key)


class Profile(models.Model):
    """
    Return a profile with certain fields. One profile corresponds to one profile
    """
    user = models.OneToOneField(User, max_length=25, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    surname = models.CharField(max_length=25)
    about_me = models.TextField(blank=True)
    avatar = models.ImageField(upload_to=profile_directory_path, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        permissions = (('deleteanotherscomment', "can delete another's comment"),)


@receiver(post_save, sender=Profile, dispatch_uid="clear_cache_profile")
def update_profile(sender, instance, **kwargs):
    for language in ('en', 'ru'):
        key = make_template_fragment_key('account', [instance.user.id, language])
        cache.delete(key)
