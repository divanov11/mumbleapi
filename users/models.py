from django.contrib.auth.models import User
from django.db import models
import uuid


# A topic tag is added to by the user so they can content on their feed with the 
# related tags that
# They have selected
class TopicTag(models.Model):
    name = models.CharField(primary_key=True, max_length=150, null=False, blank=False)

    def __str__(self):
        return self.name


# Skills are added by teh user to indicate topics they are proficient in
class SkillTag(models.Model):
    name = models.CharField(primary_key=True, max_length=150, null=False, blank=False)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(blank=True, null=True, default='default.png')
    bio = models.TextField(null=True)
    vote_ratio = models.IntegerField(blank=True, null=True, default=0)
    followers_count = models.IntegerField(blank=True, null=True, default=0)
    skills = models.ManyToManyField(SkillTag, related_name='personal_skills', blank=True)
    interests = models.ManyToManyField(TopicTag, related_name='topic_interests', blank=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    email_verified = models.BooleanField(default=False)
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    """
    profile = UserProfile.objects.first()
    profile.followers.all() -> All users following this profile
    user.following.all() -> All user profiles I follow
    """

    def __str__(self):
        return str(self.user.username)
