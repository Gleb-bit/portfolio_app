from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    technology = serializers.ReadOnlyField(source='technology.name')

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'image', 'github_link', 'technology')
