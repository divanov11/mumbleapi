from django.db import models
from users.models import UserProfile
import uuid

class Thread(models.Model):
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    users = models.ManyToManyField(UserProfile, blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        participants = []
        for i in self.users.all():
            participants.append(str(i.name))
        return str(participants)

    def latestMessage(self):
        message = self.message_set.last()
        print('Latest message:', message)
        if message:
            return message
        else:
            return None


class Message(models.Model):
    thread = models.ForeignKey(
        Thread, null=True, blank=True, on_delete=models.SET_NULL)
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.body)