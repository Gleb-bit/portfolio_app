from django.urls import path

from .views import ListProjectView, DetailProjectView

urlpatterns = [
    path('', ListProjectView.as_view(), name="list_project"),
    path('<int:pk>/', DetailProjectView.as_view(), name="detail_project"),
]
