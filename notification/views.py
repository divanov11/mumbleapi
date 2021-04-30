from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q
from .models import Notification
from .serializers import NotificationSerializer

@api_view(['GET'])
def getNotification(request, pk):
    try:
        notification = Notification.objects.get(id=pk)
        serializer = NotificationSerializer(notification, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def readNotification(request,pk):
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
