from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.signals import request_started
from django.db import models
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

    class Meta:
        ordering = ['title']


@receiver(request_started, sender=Project, dispatch_uid="clear_cache_project")
def update_project(sender, instance, **kwargs):
    key = make_template_fragment_key('project', [instance.id])
    cache.delete(key)
