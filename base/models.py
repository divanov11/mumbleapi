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
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    """
    profile = UserProfile.objects.first()
    profile.followers.all() -> All users following this profile
    user.following.all() -> All user profiles I follow
    """

    def __str__(self):
        return self.name


#This needs to be shareable
class Post(models.Model):
    parent =models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    #For re-mumble (Share) functionality
    remumble = models.ForeignKey("self", on_delete=models.SET_NULL, related_name='remumbles', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True)
    #ups = models.IntegerField(default=0)
    #downs = models.IntegerField(default=0)
    vote_rank = models.IntegerField(blank=True, null=True, default=0)
    comment_count = models.IntegerField(blank=True, null=True, default=0)
    share_count = models.IntegerField(blank=True, null=True, default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.content[0:80]

    @property
    def shares(self):
        queryset = self.remumbles.all()
        return queryset

    

class PostVote(models.Model):
    
    CHOICES = (
        ('upvote', 'upvote'),
        ('downvote', 'downvote'),
        )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    value = models.CharField(max_length=20, choices=CHOICES)

    def __str__(self):
        return str(self.user) + ' ' +  str(self.value) + 'd ' + '"' + str(self.post) + '"'



#https://github.com/nikolak/django_reddit/blob/master/reddit/models.py
# class Vote(models.Model):
#     user = models.ForeignKey('users.RedditUser')
#     submission = models.ForeignKey(Submission)
#     vote_object_type = models.ForeignKey(ContentType)
#     vote_object_id = models.PositiveIntegerField()
#     vote_object = GenericForeignKey('vote_object_type', 'vote_object_id')
#     value = models.IntegerField(default=0)



#https://github.com/SteinOveHelset/oinkoink
# class Notification(models.Model):
#     MESSAGE = 'message'
#     FOLLOWER = 'follower'
#     LIKE = 'like'
#     MENTION = 'mention'

#     CHOICES = (
#         (MESSAGE, 'Message'),
#         (FOLLOWER, 'Follower'),
#         (LIKE, 'Like'),
#         (MENTION, 'Mention')
#     )

#     to_user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)

#     notification_type = models.CharField(max_length=20, choices=CHOICES)
#     is_read = models.BooleanField(default=False)

#     created_at = models.DateTimeField(auto_now_add=True)
#     created_by = models.ForeignKey(User, related_name='creatednotifications', on_delete=models.CASCADE)

#     class Meta:
#         ordering = ['-created_at']
