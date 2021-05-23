from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from users.models import TopicTag
import uuid


class Discussion(models.Model):
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    headline = models.CharField(max_length=500, default="no headline")
    content = RichTextField(max_length=10000)
    # discussion tags from user model
    tags = models.ManyToManyField(TopicTag, related_name='discussion_tags', blank=True) 
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.headline)


class DiscussionComment(models.Model):
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    discussion = models.ForeignKey(Discussion,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)


class DiscussionVote(models.Model):
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    comment = models.ForeignKey(DiscussionComment, on_delete=models.SET_NULL,null=True, blank=True)
    value = models.IntegerField(blank=True, null=True, default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.discussion} - count - {self.value}"
