from rest_framework import serializers

from .models import Post, Category, Comment, Profile


class PostSerializer(serializers.HyperlinkedModelSerializer):
    profile = serializers.ReadOnlyField(source='profile.name')

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'image', 'profile')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    post = serializers.ReadOnlyField(source='post.title')

    class Meta:
        model = Comment
        fields = ['id', 'author', 'body', 'image', 'post']


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'name', 'surname', 'about_me', 'avatar']
