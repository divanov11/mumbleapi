from rest_framework import serializers
from .models import Notification

from users.serializers import UserProfileSerializer
from feed.serializers import MumbleSerializer
from article.serializers import ArticleSerializer
from discussion.serializers import DiscussionSerializer

class NotificationSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField(read_only=True)
    followed_by = serializers.SerializerMethodField(read_only=True)
    mumble = serializers.SerializerMethodField(read_only=True)
    article = serializers.SerializerMethodField(read_only=True)
    discussion = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Notification
        fields = '__all__'

    def get_created_by(self, obj):
        return UserProfileSerializer(obj.created_by.userprofile, many=False).data

    def get_followed_by(self, obj):
        if obj.notification_type == 'follow':
            return UserProfileSerializer(obj.followed_by.userprofile, many=False).data
        return None

    def get_mumble(self, obj):
        if obj.notification_type == 'mumble':
            return MumbleSerializer(obj.mumble, many=False).data
        return None

    def get_article(self, obj):
        if obj.notification_type == 'article':
            return ArticleSerializer(obj.article, many=False).data
        return None

    def get_discussion(self, obj):
        if obj.notification_type == 'discussion':
            return DiscussionSerializer(obj.discussion, many=False).data
        return None
