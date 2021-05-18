import datetime
import uuid
import random
import os.path

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
#email verification imports
from django.contrib.auth.tokens import default_token_generator
from django.core.files.storage import default_storage
# from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Q , Count
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from article.serializers import ArticleSerializer
from feed.serializers import MumbleSerializer
from notification.models import Notification
from notification.serializers import NotificationSerializer

from .models import UserProfile
from .serializers import (UserProfileSerializer, UserSerializer,
                          UserSerializerWithToken, CurrentUserSerializer)

# Create your views here.

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        data = request.data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        messages = {'errors':[]}
        if username == None:
            messages['errors'].append('username can\'t be empty')
        if email == None:
            messages['errors'].append('Email can\'t be empty')
        if password == None:
            messages['errors'].append('Password can\'t be empty')
        if User.objects.filter(email=email).exists():
            messages['errors'].append("Account already exists with this email id.")    
        if User.objects.filter(username__iexact=username).exists():
            messages['errors'].append("Account already exists with this username.") 
        if len(messages['errors']) > 0:
            return Response({"detail":messages['errors']},status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password)
            )
            serializer = UserSerializerWithToken(user, many=False)
        except Exception as e:
            print(e)
            return Response({'detail':f'{e}'},status=status.HTTP_400_BAD_REQUEST)
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


@api_view(['GET'])
def users(request):
    query = request.query_params.get('q')
    if query == None:
        query = ''
    users = User.objects.filter(Q(userprofile__name__icontains=query) | Q(userprofile__username__icontains=query)).order_by('userprofile__followers')
    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(users,request)
    serializer = UserSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def usersRecommended(request):
    user = request.user
    users = User.objects.annotate(followers_count=Count('userprofile__followers')).order_by('followers_count').reverse().exclude(id=user.id)[0:5]
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def user(request, username):
    user = User.objects.get(username=username)

    if(request.user.username == username):
        serializer = CurrentUserSerializer(user, many=False)
        return Response(serializer.data)

    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def userMumbles(request, username):
    user = User.objects.get(username=username)
    mumbles = user.mumble_set.filter(parent=None)
    serializer = MumbleSerializer(mumbles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def userArticles(request, username):
    user = User.objects.get(username=username)
    articles = user.article_set
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def followUser(request, username):
    userWantingToFollowSomeone = request.user
    try:
        userToFollow = User.objects.get(username=username)
        userToFollowProfile = userToFollow.userprofile

        if userWantingToFollowSomeone == userToFollow: 
            return Response('You can not follow yourself')
            
        if userWantingToFollowSomeone in userToFollowProfile.followers.all():
            userToFollowProfile.followers.remove(userWantingToFollowSomeone)
            userToFollowProfile.followers_count =  userToFollowProfile.followers.count()
            userToFollowProfile.save()
            return Response('User unfollowed')
        else:
            userToFollowProfile.followers.add(userWantingToFollowSomeone)
            userToFollowProfile.followers_count = userToFollowProfile.followers.count()
            userToFollowProfile.save()
            # doing this as a signal is much more difficult and hacky
            Notification.objects.create(
                to_user=userToFollow,
                created_by=userWantingToFollowSomeone,
                notification_type='follow',
                followed_by=userWantingToFollowSomeone,
                content=f"{userWantingToFollowSomeone.userprofile.name} started following you."
            )
            return Response('User followed')
    except Exception as e:
        message = {'detail':f'{e}'}
        return Response(message,status=status.HTTP_204_NO_CONTENT)


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
        rd = random.Random()
        profile_pic=self.request.FILES['profile_pic']
        extension = os.path.splitext(profile_pic.name)[1]
        profile_pic.name='{}{}'.format(uuid.UUID(int=rd.getrandbits(128)), extension)
        filename = default_storage.save(profile_pic.name, profile_pic)
        setattr(self.request.user.userprofile, 'profile_pic', filename)
        serializer=self.serializer_class(
            self.request.user.userprofile, data={}, partial=True)
        if serializer.is_valid():
            user=serializer.save().user
            response={'type': 'Success', 'message': 'successfully updated your info',
                        'user': UserSerializer(user).data}
        else:
            response=serializer.errors
        return Response(response)

# THIS EMAIL VERIFICATION SYSTEM IS ONLY VALID FOR LOCAL TESTING
# IN PRODUCTION WE NEED A REAL EMAIL , TILL NOW WE ARE USING DEFAULT EMAIL BACKEND
# THIS DEFAULT BACKEND WILL PRINT THE VERIFICATION EMAIL IN THE CONSOLE 
# LATER WE CAN SETUP SMTP FOR REAL EMAIL SENDING TO USER

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def sendActivationEmail(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    try:
        mail_subject = 'Verify your Mumble account.'
        message = render_to_string('verify-email.html', {
            'user': user_profile,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        to_email = user.email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return Response('Mail sent Successfully',status=status.HTTP_200_OK)
    except Exception as e:
        return Response('Something went wrong , please try again',status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user_profile = UserProfile.objects.get(user=user)
        user_profile.email_verified = True
        user_profile.save()
        return Response("Email Verified")
    else:
        return Response('Something went wrong , please try again',status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def passwordChange(request):
    user = request.user
    data = request.data
    new_password = data.get('new_password')
    new_password_confirm = data.get('new_password_confirm')
    if new_password_confirm and new_password is not None:
        if new_password == new_password_confirm:
            user.set_password(new_password)
            user.save()
            return Response({'detail':'Password changed successfully'},status=status.HTTP_200_OK)
        else:
            return Response({"detail":'Password doesn\'t match'})
    elif new_password is None:
        return Response({'detail':'New password field required'})
    elif new_password_confirm is None:
        return Response({'detail':'New password confirm field required'})
