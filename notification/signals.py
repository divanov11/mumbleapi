from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save, pre_save

from article.models import Article
from discussion.models import Discussion
from feed.models import Mumble
from users.models import UserProfile

from .models import Notification


def articleCreated(sender, instance, created, **kwargs):
    if not created: return
    followers = instance.user.userprofile.followers.all()
    for follower in followers:
        notification = Notification.objects.create(
            to_user=follower,
            created_by=instance.user,
            notification_type='article',
            article=instance,
            content=f"An article named {instance.title} was created by {instance.user.userprofile.name}."
        )


def mumbleCreated(sender, instance, created, **kwargs):
    if not created: return
    followers = instance.user.userprofile.followers.all()
    for follower in followers:
        notification = Notification.objects.create(
            to_user=follower,
            created_by=instance.user,
            notification_type='mumble',
            mumble=instance,
            content=f"A mumble mentioning {instance.user.userprofile.name} was created."
        )



def discussionCreated(sender, instance, created, **kwargs):
    if not created: return
    followers = instance.user.userprofile.followers.all()
    for follower in followers:
        notification = Notification.objects.create(
            to_user=follower,
            created_by=instance.user,
            notification_type='discussion',
            discussion=instance,
            content=f"A discussion was started by {instance.user.userprofile.name}."
        )

post_save.connect(articleCreated, sender=Article)
post_save.connect(mumbleCreated, sender=Mumble)
post_save.connect(discussionCreated, sender=Discussion)