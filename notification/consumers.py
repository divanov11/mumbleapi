import asyncio
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from notification.exceptions import ClientError
from .serializers import NotificationSerializer
import json
from django.db.models.signals import post_save
from .models import  Notification
from django.dispatch import receiver

class NotificationConsumer(AsyncJsonWebsocketConsumer):
    """ Notification Consumer """
    async def connect(self):
        print("new connection request ")
        await self.accept()
        while True:
            await asyncio.sleep(3)
            payload = await get_latest_notifications(self, self.scope["user"])
            if payload == None:
                pass
            else:
                await self.get_notifications(payload)

    async def disconnect(self, close_code):
        print(close_code)

    async def receive_json(self, content):
        command = content.get("command", None)
        print('command recived----',command)
        try:
            if command == "get_notifications":
                print("get_notificaitons ran")
                print(self.scope["user"])
                payload = await get_latest_notifications(self,self.scope["user"])
                if payload == None:
                    pass
                else:
                    await self.get_notifications(payload)
        except ClientError as e:
            pass
    @receiver(post_save,sender=Notification)
    async def get_continuous_notifications(instance,**kwargs):
        """Called by the postSave Signal """
        print(instance)
        print(**kwargs)
        # payload = await get_latest_notifications(self, self.scope["user"])
        # if payload == None:
        #     pass
        # else:
        #     await self.get_notifications(payload)

    async def get_notifications(self,notifications,**kwargs):
        await self.send(json.dumps({
            "notificaitons":notifications
        }))


# post_save.connect(get_continuous_notifications(self),sender=Notification)
@database_sync_to_async
def get_latest_notifications(self,user):
    notifications = user.notifications.order_by('-created')
    serialized_data = NotificationSerializer(notifications,many=True)
    return  serialized_data.data



