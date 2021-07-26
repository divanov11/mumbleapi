from django.db import models
from users.models import UserProfile
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True
class Thread(BaseModel):
    sender = models.ForeignKey(UserProfile,on_delete=models.SET_NULL,null=True,related_name="sender")
    reciever = models.ForeignKey(UserProfile,on_delete=models.SET_NULL,null=True,related_name="reciever")
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.sender.username + " and " + self.reciever.username)


class UserMessage(BaseModel):
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE,related_name="messages")
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    body = models.TextField(null=True,blank=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return str(self.body)