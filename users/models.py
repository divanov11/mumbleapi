from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser
import uuid

# Create your models here.
class User(AbstractBaseUser):
    email = models.EmailField(unique=True,max_length=200)
    username = models.CharField(unique=True,max_length=200)
    full_name = models.CharField(max_length=155)
    birth_date = models.DateField(null=True,blank=True)
    is_active = models.BooleanField(default=True) 
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True 

    @property
    def is_staff(self):
        return self.is_admin

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(blank=True, null=True, default='default.png')
    bio = models.TextField(null=True)
    vote_ratio = models.IntegerField(blank=True, null=True, default=0)
    followers_count = models.IntegerField(blank=True, null=True, default=0)
    #skills = 
    #interests = 
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
