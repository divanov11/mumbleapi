from rest_framework import serializers

from users.serializers import UserProfileSerializer

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Notification
        fields = '__all__'

    def get_created_by(self, obj):
        created_by = obj.created_by.userprofile
        serializer = UserProfileSerializer(created_by, many=False)
        return serializer.data
