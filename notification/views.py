from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import UserProfile

from .models import Notification
from .serializers import NotificationSerializer


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def readNotification(request, pk):
    try:
        notification= Notification.objects.get(id=pk)
        if notification.to_user == request.user:
            notification.is_read = True
            notification.save()
            serializer = NotificationSerializer(notification, many=False)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def getNotifications(request):
    notifications = request.user.notifications
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)
