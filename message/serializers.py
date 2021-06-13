from rest_framework import serializers
from .models import Message

from users.serializers import UserProfileSerializer

class MessageSerializer(serializers.ModelSerializer):
    to_user = serializers.SerializerMethodField(read_only=True)
    created_by = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Message
        fields = '__all__'

    def get_created_by(self, obj):
        return UserProfileSerializer(obj.created_by.userprofile, many=False).data

    def get_to_user(self, obj):
        return UserProfileSerializer(obj.to_user.userprofile, many=False).data
