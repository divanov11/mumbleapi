from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


from .models import Post
from .serializers import PostSerializer, UserSerializer, UserSerializerWithToken



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['name'] = user.userprofile.name
        token['profile_pic'] = 'static' + user.userprofile.profile_pic.url
        token['is_staff'] = user.is_staff

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def routes(request):
    urls = [
        '/api',
        '/posts',
        '/posts/:id'
        '/posts/:id/comments'

        '/users',
        '/users/:id'
        '/users/posts'
    ]
    return Response(urls)

@api_view(['GET'])
def posts(request):
    query = request.query_params.get('q')
    if query == None:
        query = ''

    #Make sure parent==None is always on
    posts = Post.objects.filter(parent=None)
    posts = posts.filter(Q(user__userprofile__name__icontains=query) | Q(content__icontains=query))
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def postComments(request, pk):
    post = Post.objects.get(id=pk)
    comments = post.post_set.all()
    serializer = PostSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def users(request):

    query = request.query_params.get('q')
    if query == None:
        query = ''

    #users = User.objects.filter(username__icontains=query)
    users = User.objects.filter(Q(userprofile__name__icontains=query) | Q(userprofile__username__icontains=query))
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def usersRecommended(request):
    users = User.objects.all()[0:5]
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def user(request, username):
    user = User.objects.get(username=username)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def userPosts(request, username):
    user = User.objects.get(username=username)
    posts = user.post_set.filter(parent=None)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

# @api_view(['GET'])
# def userTags(request, pk):
#     user = User.objects.get(id=pk)
#     tags = user._set.filter(parent=None)
#     serializer = PostSerializer(posts, many=True)
#     return Response(serializer.data)

