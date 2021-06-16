"""General web socket middlewares
written by github.com/nasir733
"""

from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.state import User
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack
from django.db import close_old_connections
from urllib.parse import parse_qs
from jwt import decode as jwt_decode
from django.conf import settings


@database_sync_to_async
def get_user(validated_token):
    try:
        user = get_user_model().objects.get(id=validated_token["user_id"])
        # return get_user_model().objects.get(id=toke_id)
        print(f"{user}")
        return user

    except User.DoesNotExist:
        return AnonymousUser()


class JwtAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # Close old database connections to prevent usage of timed out connections
        close_old_connections()

        # Get the token
        token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]

        # Try to authenticate the user
        try:
            # This will automatically validate the token and raise an error if token is invalid
            UntypedToken(token)
        except (InvalidToken, TokenError) as e:
            # Token is invalid
            print(e)
            return None
        else:
            #  Then token is valid, decode it
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            print(decoded_data)
            # Will return a dictionary like -
            # {
            #     "token_type": "access",
            #     "exp": 1568770772,
            #     "jti": "5c15e80d65b04c20ad34d77b6703251b",
            #     "user_id": 6
            # }

            # Get the user using ID
            scope["user"] = await get_user(validated_token=decoded_data)
        return await super().__call__(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    return JwtAuthMiddleware(AuthMiddlewareStack(inner))