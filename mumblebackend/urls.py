"""mumblebackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # commenting this because docs is added for better endpoint view
    # path('', views.api_root),
    path('api/users/', include('users.urls')),
    path('api/articles/', include('article.urls')),
    path('api/discussions/', include('discussion.urls')),
    path('api/messages/', include('message.urls')),
    path('api/notifications/', include('notification.urls')),
    path('api/mumbles/', include('feed.urls')),
    path('schema/', get_schema_view(
        title="MumbleAPI",
        description="API for the Mumble.dev",
        version="1.0.0"
    ), name="mumble-schema"),
    path('', include_docs_urls(
        title="MumbleAPI",
        description="API for the Mumble.dev",
    ), name="mumble-docs")
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)