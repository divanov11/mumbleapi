from rest_framework import serializers
from .models import UserMessage , Thread
from users.serializers import UserProfileSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender = UserProfileSerializer(read_only=True)
    class Meta:
        model = UserMessage
        fields = '__all__'

class ThreadSerializer(serializers.ModelSerializer):
    chat_messages = serializers.SerializerMethodField(read_only=True)
    last_message = serializers.SerializerMethodField(read_only=True)
    un_read_count = serializers.SerializerMethodField(read_only=True)
    sender = UserProfileSerializer(read_only=True)
    reciever = UserProfileSerializer(read_only=True)
    class Meta:
        model = Thread
        fields = ['id','updated','timestamp','sender','reciever','chat_messages','last_message','un_read_count']

    def get_chat_messages(self,obj):
        messages = MessageSerializer(obj.messages.order_by('timestamp'),many=True)
        return messages.data

    def get_last_message(self,obj):
        serializer = MessageSerializer(obj.messages.order_by('timestamp').last(),many=False)
        return serializer.data

    def get_un_read_count(self,obj):
        messages = obj.messages.filter(is_read=False).count()
        return messages
