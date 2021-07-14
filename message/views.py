from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models import UserProfile
from .serializers import MessageSerializer , ThreadSerializer
from .models import UserMessage , Thread
from django.db.models import Q

@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def read_message(request, pk):
    try:
        message = UserMessage.objects.get(id=pk)
        if message.sender == request.user.userprofile:
            message.is_read = True
            message.save()
            serializer = MessageSerializer(message, many=False)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'details': f"{e}"},status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_messages(request):
    user = request.user.userprofile
    threads = Thread.objects.filter(users__in=[user])
    serializer = ThreadSerializer(threads, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_message(request):
    sender = request.user.userprofile
    data = request.data
    reciever_id = data.get('reciever_id')
    if reciever_id:
        message = data.get('message')
        reciever = UserProfile.objects.get(id=reciever_id)
        threads = Thread.objects.filter(users__in=[sender.id])
        if threads.count() > 0:
            chat_box = threads.first()
            if message is not None:
                message = UserMessage.objects.create(thread=chat_box,sender=sender,body=message)
            else:
                return Response({'details':'Content for message required'})
        else:
            chat_box = Thread()
            chat_box.save()
            chat_box.users.set([sender,reciever])
        serializer = ThreadSerializer(chat_box,many=False)
        return Response(serializer.data)
    else:
        return Response({'details':'Please provide other user id'})