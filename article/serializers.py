from rest_framework import serializers
from .models import (
    Article,
    ArticleComment,
    ArticleVote
)
from users.serializers import UserProfileSerializer , UserSerializer



class ArticleSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Article
        fields = '__all__'

    def get_user(self, obj):
        user = obj.user.userprofile
        serializer = UserProfileSerializer(user, many=False)
        return serializer.data