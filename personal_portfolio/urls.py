"""personal_portfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers

from blog.api import *
from personal_portfolio import settings
from projects.api import *

router = routers.DefaultRouter()
router.register('posts', PostViewSet, 'posts')
router.register('categories', CategoryViewSet, 'categories')
router.register('comments', CommentViewSet, 'comments')
router.register('profiles', ProfileViewSet, 'profiles')
router.register('projects', ProjectViewSet, 'projects')
router.register('users', UserViewSet, 'users')

schema_view = get_schema_view(
    openapi.Info(
        title='Blog and projects API',
        default_version='v1',
        description='description of app',
        terms_of_service='https://www.google.com/polices/terms/',
        contact=openapi.Contact(email='admin@company.local'),
        license=openapi.License(name=''),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
                  path('admin/doc/', include('django.contrib.admindocs.urls')),
                  path('admin/', admin.site.urls),
                  path("projects/", include("projects.urls")),
                  path("blog/", include('blog.urls')),
                  path('i18n', include('django.conf.urls.i18n')),
                  path('api/', include(router.urls)),
                  path('api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                  path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
