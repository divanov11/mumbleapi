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
    print('DATA:', data)

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
    print('HEADERS:', request.headers)
    user = request.user
    otherUser = User.objects.get(username=username).userprofile
    if user in otherUser.followers.all():
        otherUser.followers.remove(user)
        return Response('User unfollowed')
    else:
        otherUser.followers.add(user)
        return Response('User followed')


# @api_view(['GET'])
# def userTags(request, pk):
#     user = User.objects.get(id=pk)
#     tags = user._set.filter(parent=None)
#     serializer = PostSerializer(posts, many=True)
#     return Response(serializer.data)

