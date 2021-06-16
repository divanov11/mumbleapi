import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from notification.exceptions import ClientError
from .serializers import NotificationSerializer

class NotificationConsumer(AsyncWebsocketConsumer):
    """ Notification Consumer """
    async def connect(self):
        print("new connection request ")
        await self.accept()

    async def disconnect(self, close_code):
        print(close_code)

    async def receive_json(self, content):
        command = content.get("command", None)
        print('command recived----',command)
        try:
            if command == "get_notifications":
                print("get_notificaitons ran")
                payload = await get_latest_notifications(self.scope["user"])
                if payload == None:
                    pass
                else:
                    await self.get_notifications(payload)






        except ClientError as e:
            pass

    async def get_notifications(self,notifications):
        await self.send({
            "notificaitons":notifications
        })

@database_sync_to_async
def get_latest_notifications(self,user):
    notifications = user.notifications.order_by('-created')
    serialized_data = NotificationSerializer(notifications,many=True)
    return  serialized_data.data



