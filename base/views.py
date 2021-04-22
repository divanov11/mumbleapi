from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password
from rest_framework import status

from .models import Post, PostVote
from .serializers import PostSerializer, UserSerializer, UserSerializerWithToken



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['name'] = user.userprofile.name
        token['profile_pic'] = 'static' + user.userprofile.profile_pic.url
        token['is_staff'] = user.is_staff
        token['id'] = user.id

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def registerUser(request):
    data = request.data
    #try:
    user = User.objects.create(
        username=data['username'],
        email=data['email'],
        password=make_password(data['password'])
    )

    serializer = UserSerializerWithToken(user, many=False)
    return Response(serializer.data)
    # except:
    #     message = {'detail': 'User with this email already exists'}
    #     return Response(message, status=status.HTTP_400_BAD_REQUEST)


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

    user = request.user
    following = user.following.select_related('user')

    following = user.following.all()

    ids = [user.id]
    for i in following:
        ids.append(i.user.id)

    #Make sure parent==None is always on
    posts = Post.objects.filter(parent=None, user__id__in=ids)
    posts = posts.filter(Q(user__userprofile__name__icontains=query) | Q(content__icontains=query))
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createPost(request):
    user = request.user
    data = request.data

    isComment = data['isComment']

    if isComment:
        print('Creating a comment')
        parent = Post.objects.get(id=data['postId'])
        post = Post.objects.create(
            parent=parent,
            user=user,
            content=data['content'],
            )
        print('PARENT:', parent)
    else:
        print('Creating a standard post')
        post = Post.objects.create(
            user=user,
            content=data['content']
            )

    serializer = PostSerializer(post, many=False)
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

    users = User.objects.filter(Q(userprofile__name__icontains=query) | Q(userprofile__username__icontains=query))
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def usersRecommended(request):
    user = request.user
    following = user.following.select_related('user')

    following = user.following.all()

    ids = []
    for i in following:
        pass
        #ids.append(i.user.id)

    #Exlude logged in users and user i am already following from recommendations
    users = User.objects.filter(~Q(id=user.id), ~Q(id__in=ids))[0:5]

    user = request.user
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


@api_view(['POST'])
def followUser(request, username):
    user = request.user
    otherUser = User.objects.get(username=username).userprofile
    if user in otherUser.followers.all():
        otherUser.followers.remove(user)
        otherUser.followers_count =  len(otherUser.followers.all())
        otherUser.save()
        return Response('User unfollowed')
    else:
        otherUser.followers.add(user)
        otherUser.followers_count =  len(otherUser.followers.all())
        otherUser.save()
        return Response('User followed')

@api_view(['POST'])
def remumble(request):
    user = request.user
    data = request.data
    origionalPost = Post.objects.get(id=data['id'])

    post = Post.objects.create(
        remumble=origionalPost,
        user=user,
    )
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def updateVote(request):
    user = request.user 
    data = request.data

    post = Post.objects.get(id=data['post_id'])
    #What if user is trying to remove their vote?
    vote, created = PostVote.objects.get_or_create(post=post, user=user)
    if vote.value == data['value']:
        #If same value is sent, user is clicking on vote to remove it
        vote.delete() 
    else:

        vote.value=data['value']
        vote.save()

    #We re-query the vote to get the latest vote rank value
    post = Post.objects.get(id=data['post_id'])
    serializer = PostSerializer(post, many=False)

    return Response(serializer.data)


# @api_view(['GET'])
# def userTags(request, pk):
#     user = User.objects.get(id=pk)
#     tags = user._set.filter(parent=None)
#     serializer = PostSerializer(posts, many=True)
#     return Response(serializer.data)

