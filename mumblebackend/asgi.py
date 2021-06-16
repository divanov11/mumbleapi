"""
ASGI config for mumblebackend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import notification.routing
from channels.security.websocket import AllowedHostsOriginValidator
from .channelsmiddleware import JwtAuthMiddlewareStack
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mumblebackend.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(JwtAuthMiddlewareStack(
            URLRouter(notification.routing.websocket_urlpatterns))
        ),
    }
)
