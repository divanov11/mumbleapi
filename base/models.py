from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(blank=True, null=True, default='default.png')
    bio = models.TextField()
    vote_ratio = models.IntegerField(blank=True, null=True, default=0)
    followers_count = models.IntegerField(blank=True, null=True, default=0)
    #skills = 
    #interests = 
    #followers = 

    def __str__(self):
        return self.name


#This needs to be shareable
class Post(models.Model):
    parent =models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True)
    vote_rank = models.IntegerField(blank=True, null=True, default=0)
    comment_count = models.IntegerField(blank=True, null=True, default=0)
    share_count = models.IntegerField(blank=True, null=True, default=0)
    created = models.DateTimeField(auto_now_add=True)

    

    def __str__(self):
        return self.content[0:80]





# class PostComment(models.Model):
#     parent =models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     content = models.TextField()
#     image = models.ImageField(blank=True, null=True)
#     vote_rank = models.IntegerField(blank=True, null=True, default=0)
#     comment_count = models.IntegerField(blank=True, null=True, default=0)
#     share_count = models.IntegerField(blank=True, null=True, default=0)
#     created = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-created']

#     def __str__(self):
#         return self.content[0:80]
