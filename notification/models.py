import uuid

from django.contrib.auth.models import User
from django.db import models


class Notification(models.Model):

    CHOICES = (
        ('article', 'article'),
        ('mumble', 'mumble'),
        ('discussion', 'discussion'),
        ('follow', 'follow'),
    )

    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    to_user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    content = models.CharField(max_length=255)
    content_id = models.UUIDField(editable=False, null=False)
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=20, choices=CHOICES)

    def __str__(self):
        return str(self.id)
