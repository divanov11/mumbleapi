from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Post, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField(read_only=True)
    interests = serializers.SerializerMethodField(read_only=True)
    skills = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = UserProfile
        fields = '__all__'

    def get_profile_pic(self, obj):
        try:
            pic = 'static' + obj.profile_pic.url
        except:
            pic = None
        return pic

    def get_interests(self, obj):
        return ['Python', 'C#', 'D3 Charts', 'Flutter']

    def get_skills(self, obj):
        return ['Python', 'C#', 'D3 Charts', 'Flutter']

class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'profile', 'username', 'is_superuser', 'is_staff']

    def get_profile(self, obj):
        profile = obj.userprofile
        serializer = UserProfileSerializer(profile, many=False)
        return serializer.data


class UserSerializerWithToken(UserSerializer):
    access = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def get_access(self, obj):
        token = RefreshToken.for_user(obj)

        token['username'] = obj.username
        token['name'] = obj.userprofile.name
        token['profile_pic'] = 'static' + obj.userprofile.profile_pic.url
        token['is_staff'] = obj.is_staff
        token['id'] = obj.id
        return str(token.access_token)

    #Add route to return refresh token



class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    origional_mumble = serializers.SerializerMethodField(read_only=True)
    upVoters = serializers.SerializerMethodField(read_only=True)
    downVoters = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Post
        fields = '__all__'

    def get_user(self, obj):
        user = obj.user.userprofile
        serializer = UserProfileSerializer(user, many=False)
        return serializer.data


    def get_origional_mumble(self, obj):
        origional = obj.remumble
        if origional != None:
            serializer = PostSerializer(origional, many=False)
            return serializer.data
        else:
            return None

    def get_upVoters(self, obj):
        # Returns list of users that upvoted post
        voters = obj.votes.through.objects.filter(post=obj, value='upvote').values_list('user', flat=True)

        voter_objects = obj.votes.filter(id__in=voters)
        serializer = UserSerializer(voter_objects, many=True)
        return serializer.data

    def get_downVoters(self, obj):
        # Returns list of users that upvoted post
        voters = obj.votes.through.objects.filter(post=obj, value='downvote').values_list('user', flat=True)

        voter_objects = obj.votes.filter(id__in=voters)
        serializer = UserSerializer(voter_objects, many=True)
        return serializer.data
