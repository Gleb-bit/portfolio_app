from django.urls import path

from .views import BlogIndexView, BlogDetailView, BlogCategoryView

urlpatterns = [
    path("", BlogIndexView.as_view(), name="blog_index"),
    path("<int:pk>/", BlogDetailView.as_view(), name="blog_detail"),
    path("<category>/", BlogCategoryView.as_view(), name="blog_category"),
]
