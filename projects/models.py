from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Project(models.Model):
    '''
    Return a project with certain fields
    '''
    title = models.CharField(max_length=100)
    description = models.TextField()
    technology = models.CharField(max_length=255)
    image = models.FilePathField(path="projects/static/img")
    github_link = models.CharField(max_length=255)

    def __str__(self):
        return self.title


@receiver(post_save, sender=Project, dispatch_uid="clear_cache_project")
def update_project(sender, **kwargs):
    key = make_template_fragment_key('project', [kwargs['instance'].user.id])
    cache.delete(key)
