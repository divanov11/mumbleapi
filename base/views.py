from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from django.contrib.auth.models import User


from .models import Post
from .serializers import PostSerializer, UserSerializer

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
def posts(requests):
    posts = Post.objects.filter(parent=None)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def postComments(requests, pk):
    post = Post.objects.get(id=pk)
    comments = post.post_set.all()
    serializer = PostSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def users(requests):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def user(requests, username):
    user = User.objects.get(username=username)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def userPosts(requests, username):
    user = User.objects.get(username=username)
    posts = user.post_set.filter(parent=None)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

# @api_view(['GET'])
# def userTags(requests, pk):
#     user = User.objects.get(id=pk)
#     tags = user._set.filter(parent=None)
#     serializer = PostSerializer(posts, many=True)
#     return Response(serializer.data)

