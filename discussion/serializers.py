from rest_framework import serializers
from .models import (
    Discussion,
    DiscussionComment,
    DiscussionVote
)
from users.serializers import UserProfileSerializer



class DiscussionSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Discussion
        fields = '__all__'

    def get_user(self, obj):
        user = obj.user.userprofile
        serializer = UserProfileSerializer(user, many=False)
        return serializer.data

    def get_tags(self, obj):
        return ['Python', 'Django', 'Postman', 'API']

class DiscussionCommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = DiscussionComment
        fields = '__all__'

    def get_user(self, obj):
        user = obj.user.userprofile
        serializer = UserProfileSerializer(user, many=False)
        return serializer.data

class DiscussionVoteSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = DiscussionVote
        field = '__all__'
    
    def get_user(self, obj):
        user = obj.user.userprofile
        serializer = UserProfileSerializer(user, many=False)
        return serializer.data
