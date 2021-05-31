from django.urls import path

from .views import ListProjectView, DetailProjectView

urlpatterns = [
    path("", ListProjectView.as_view(), name="project_index"),
    path("<int:pk>/", DetailProjectView.as_view(), name="project_detail"),
]
