from django.urls import path, include

from .views import BlogIndexView, BlogDetailView, BlogCategoryView, RegisterView, OurLoginView, OurLogoutView

urlpatterns = [
    path('', BlogIndexView.as_view(), name="blog_index"),
    path('<int:pk>/', BlogDetailView.as_view(), name="blog_detail"),
    path('<category>/', BlogCategoryView.as_view(), name="blog_category"),
    path('user/register/', RegisterView.as_view(), name='register'),
    path('user/login/', OurLoginView.as_view(), name='login'),
    path('user/logout/', OurLogoutView.as_view(), name='logout'),
]
