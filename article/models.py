from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class Article(models.Model):
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=500, default="untitled")
    content = models.TextField(max_length=10000)
    tags = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)


class ArticleComment(models.Model):
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)


class ArticleVote(models.Model):
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment = models.ForeignKey(ArticleComment, on_delete=models.SET_NULL,null=True, blank=True)
    value = models.IntegerField(blank=True, null=True, default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.article} - count - {self.value}"
