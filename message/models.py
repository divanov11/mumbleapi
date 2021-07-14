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
            participants.append(str(i.username))
        return str(participants)


class UserMessage(models.Model):
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    thread = models.ForeignKey(
        Thread, null=True, blank=True, on_delete=models.SET_NULL,related_name="messages")
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    body = models.TextField(null=True,blank=True)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.body)