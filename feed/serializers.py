from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Mumble
from users.serializers import UserProfileSerializer, UserSerializer


class MumbleSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    origional_mumble = serializers.SerializerMethodField(read_only=True)
    upVoters = serializers.SerializerMethodField(read_only=True)
    downVoters = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Mumble
        fields = '__all__'

    def get_user(self, obj):
        user = obj.user.userprofile
        serializer = UserProfileSerializer(user, many=False)
        return serializer.data


    def get_origional_mumble(self, obj):
        origional = obj.remumble
        if origional != None:
            serializer = MumbleSerializer(origional, many=False)
            return serializer.data
        else:
            return None

    def get_upVoters(self, obj):
        # Returns list of users that upvoted post
        voters = obj.votes.through.objects.filter(mumble=obj, value='upvote').values_list('user', flat=True)

        voter_objects = obj.votes.filter(id__in=voters)
        serializer = UserSerializer(voter_objects, many=True)
        return serializer.data

    def get_downVoters(self, obj):
        # Returns list of users that upvoted post
        voters = obj.votes.through.objects.filter(mumble=obj, value='downvote').values_list('user', flat=True)

        voter_objects = obj.votes.filter(id__in=voters)
        serializer = UserSerializer(voter_objects, many=True)
        return serializer.data
