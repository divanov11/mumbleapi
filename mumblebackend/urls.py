from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.api_root),
    path('api/users/', include('users.urls')),
    path('api/articles/', include('article.urls')),
    path('api/discussions/', include('discussion.urls')),
    path('api/notifications/', include('notification.urls')),
    path('api/mumbles/', include('feed.urls')),
]
