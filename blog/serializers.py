from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Post, Category, Comment, Profile


class PostSerializer(serializers.HyperlinkedModelSerializer):
    profile = serializers.ReadOnlyField(source='profile.name')
    comments = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='comments-detail')
    categories = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='categories-detail')

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'image', 'profile', 'comments', 'categories']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='posts-detail')

    class Meta:
        model = Category
        fields = ['id', 'name', 'posts']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    post = serializers.ReadOnlyField(source='post.title')
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'author', 'body', 'image', 'post', 'user']


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='posts-detail')
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Profile
        fields = ['id', 'name', 'surname', 'about_me', 'avatar', 'posts', 'user']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    comments = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='comments-detail')

    class Meta:
        model = User
        fields = ['id', 'username', 'last_login', 'is_staff', 'is_superuser', 'is_active', 'comments']
