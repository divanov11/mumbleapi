from django.contrib.auth.models import User
from rest_framework import serializers

from users.serializers import UserProfileSerializer, UserSerializer

from .models import Mumble


class MumbleSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    original_mumble = serializers.SerializerMethodField(read_only=True)
    upVoters = serializers.SerializerMethodField(read_only=True)
    downVoters = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Mumble
        fields = '__all__'

    def get_user(self, obj):
        user = obj.user.userprofile
        serializer = UserProfileSerializer(user, many=False)
        return serializer.data


    def get_original_mumble(self, obj):
        original = obj.remumble
        if original != None:
            serializer = MumbleSerializer(original, many=False)
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
