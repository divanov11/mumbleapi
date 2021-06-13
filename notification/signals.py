from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save, pre_save

from article.models import Article
from discussion.models import Discussion
from feed.models import Mumble
from users.models import UserProfile

from .models import Notification


def article_created(sender, instance, created, **kwargs):
    if not created: return
    followers = instance.user.userprofile.followers.all()
    for follower in followers:
        notification = Notification.objects.create(
            to_user=follower,
            created_by=instance.user,
            notification_type='article',
            article=instance,
            content=f"An article {instance.title} recently posted by {instance.user.userprofile.name}."
        )


def mumble_created(sender, instance, created, **kwargs):
    if not created: return
    followers = instance.user.userprofile.followers.all()
    for follower in followers:
        notification = Notification.objects.create(
            to_user=follower,
            created_by=instance.user,
            notification_type='mumble',
            mumble=instance,
            content=f"{instance.user.userprofile.name} posted a new Mumble."
        )



def discussion_created(sender, instance, created, **kwargs):
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

post_save.connect(article_created, sender=Article)
post_save.connect(mumble_created, sender=Mumble)
post_save.connect(discussion_created, sender=Discussion)