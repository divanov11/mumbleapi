from django.db import models
from django.contrib.auth.models import User
import uuid

class Message(models.Model):
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    to_user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    content = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.id)
