from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, mixins
from rest_framework.viewsets import GenericViewSet

from .models import Post, Category, Comment, Profile
from .permissions import IsPostOwnerOrReadOnly, IsUserOwnerOrReadOnly, IsProfileOwnerOrReadOnly, \
    IsCommentOwnerOrReadOnly
from .serializers import PostSerializer, CategorySerializer, CommentSerializer, ProfileSerializer, UserSerializer


class PostViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    '''Information about post'''
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsPostOwnerOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    '''Information about categories'''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CommentViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    '''Information about comments'''
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCommentOwnerOrReadOnly]


class ProfileViewSet(viewsets.ModelViewSet):
    '''Information about profile'''
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsProfileOwnerOrReadOnly]


class UserViewSet(viewsets.ModelViewSet):
    '''Information about user'''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsUserOwnerOrReadOnly]
