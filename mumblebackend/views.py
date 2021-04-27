from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse, reverse_lazy


@api_view(['GET'])
def api_root(request):

    ''' Single entry point to mumble API (Does not include dynamic urls)'''

    return Response({
        # users endpoints
        'users': reverse('users-api:users', request=request),
        'users-recommended': reverse('users-api:users-recommended', request=request),
        'register': reverse('users-api:register', request=request),
        'login': reverse('users-api:login', request=request),
        'profile_update': reverse('users-api:profile_update', request=request),

        # mumbles endpoints
        'mumbles': reverse('mumbles-api:mumbles', request=request),
        'mumble-create': reverse('mumbles-api:mumble-create', request=request),
        'mumble-remumble': reverse('mumbles-api:mumble-remumble', request=request),
        'posts-vote': reverse('mumbles-api:posts-vote', request=request),
    })