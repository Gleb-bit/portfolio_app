from django.urls import path, include

from .views import *

urlpatterns = [
    path('', BlogIndexView.as_view(), name="blog_index"),
    path('<int:pk>/', BlogDetailView.as_view(), name="blog_detail"),
    path('<category>/', BlogCategoryView.as_view(), name="blog_category"),
    path('create/post', CreatePostView.as_view(), name='create_post'),
    path('user/register/', RegisterView.as_view(), name='register'),
    path("oauth/", include('social_django.urls')),
    path('user/login/', OurLoginView.as_view(), name='login'),
    path('user/logout/', OurLogoutView.as_view(), name='logout'),
    path('user/<int:pk>', DetailAccountView.as_view(), name='detail_account'),
    path('user/<int:pk>/edit', EditAccountView.as_view(), name='edit_account')
]
