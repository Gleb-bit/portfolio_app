from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    technology = models.CharField(max_length=255)
    image = models.FilePathField(path="/img")
    github_link = models.CharField(max_length=255)

    def __str__(self):
        return self.title
