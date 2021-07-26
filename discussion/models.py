from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from users.models import TopicTag
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        abstract = True


class Discussion(BaseModel):
    headline = models.CharField(max_length=500, default="no headline")
    content = RichTextField(max_length=10000)
    # discussion tags from user model
    tags = models.ManyToManyField(TopicTag, related_name='discussion_tags', blank=True)

    def __str__(self):
        return str(self.headline)


class DiscussionComment(BaseModel):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)

    def __str__(self):
        return str(self.user.username)


class DiscussionVote(BaseModel):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    comment = models.ForeignKey(DiscussionComment, on_delete=models.SET_NULL, null=True, blank=True)
    value = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return f"{self.discussion} - count - {self.value}"