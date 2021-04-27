from django.shortcuts import render
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from django.db.models import Q
from .models import UserProfile
from .serializers import UserProfileSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password
from rest_framework import status


from .serializers import UserSerializerWithToken, UserSerializer
from feed.serializers import MumbleSerializer
import datetime
# Create your views here.

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        data = request.data
        user = User.objects.create(
            username=data['username'],
            email=data['email'],
            password=make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)

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

    users = User.objects.filter(~Q(id=user.id))[0:5]

    user = request.user
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def user(request, username):
    user = User.objects.get(username=username)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def userMumbles(request, username):
    user = User.objects.get(username=username)
    mumbles = user.mumble_set.filter(parent=None)
    serializer = MumbleSerializer(mumbles, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def followUser(request, username):
    user = request.user
    otherUser = User.objects.get(username=username).userprofile
    if user in otherUser.followers.all():
        otherUser.followers.remove(user)
        otherUser.followers_count =  otherUser.followers.count()
        otherUser.save()

        return Response('User unfollowed')
    else:
        otherUser.followers.add(user)
        otherUser.followers_count =  otherUser.followers.count()
        otherUser.save()
        
        return Response('User followed')
    
    

class UserProfileUpdate(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    #http_method_names = ['patch', 'head']


    def patch(self, *args, **kwargs):
        profile = self.request.user.userprofile
        serializer = self.serializer_class(
            profile, data=self.request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save().user
            
            response = {'success': True, 'message': 'successfully updated your info',
                        'user': UserSerializer(user).data}
            return Response(response, status=200)
        else:
            response = serializer.errors
            return Response(response, status=401)
        

class ProfilePictureUpdate(APIView):
    permission_classes=[IsAuthenticated]
    serializer_class=UserProfileSerializer
    parser_class=(FileUploadParser,)

    def patch(self, *args, **kwargs):
    
        profile_pic=self.request.FILES['profile_pic']
        profile_pic.name='{}.png'.format(self.request.user.id)
        serializer=self.serializer_class(
            self.request.user.profile, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.profile_pic.name=datetime.datetime.now()
            user=serializer.save().user
            response={'type': 'Success', 'message': 'successfully updated your info',
                        'user': UserSerializer(user).data}
        else:
            response=serializer.errors
        return Response(response)
    
