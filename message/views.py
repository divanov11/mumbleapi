from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models import UserProfile
from .serializers import MessageSerializer , ThreadSerializer
from .models import UserMessage , Thread
from django.db.models import Q

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def read_message(request, pk):
    try:
        thread = Thread.objects.get(id=pk)
        messages = thread.messages.all()
        print(messages)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
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
    thread_id = data.get('thread_id')
    if thread_id:
        message = data.get('message')
        thread,created = Thread.objects.get_or_create(id=thread_id,users__in=[sender.id])
        if thread:
            chat_box = thread
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