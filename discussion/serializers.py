from rest_framework import serializers
from .models import (
    Discussion,
    DiscussionComment,
    DiscussionVote
)
from users.serializers import UserProfileSerializer, TopicTagSerializer



class DiscussionSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    tags = TopicTagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Discussion
        fields = '__all__'

    def get_user(self, obj):
        user = obj.user.userprofile
        serializer = UserProfileSerializer(user, many=False)
        return serializer.data

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
