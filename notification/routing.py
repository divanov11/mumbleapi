from django.urls import re_path,path

from . import consumers

websocket_urlpatterns = [
    path('', consumers.NotificationConsumer.as_asgi()),
]