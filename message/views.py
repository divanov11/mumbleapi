from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import MessageSerializer
from .models import Message


# @api_view(['PUT'])
# @permission_classes((IsAuthenticated,))
# def read_notification(request, pk):
#     try:
#         notification = Notification.objects.get(id=pk)
#         if notification.to_user == request.user:
#             notification.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response(status=status.HTTP_401_UNAUTHORIZED)
#     except Exception as e:
#         return Response({'details': f"{e}"},status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_messages(request):
    messages = request.user.messages.all().order_by('-created')
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_message(request):
    user = request.user
    data = request.data
    to_user = User.objects.get(id=data['to_user'])

    message = Message.objects.create(
        to_user=to_user,
        created_by=user,
        content=data['content']
    )
    serializer = MessageSerializer(message, many=False)
    return Response(serializer.data)