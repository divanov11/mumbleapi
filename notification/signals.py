from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save, pre_save

from article.models import Article
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
            content_id=instance.id,
            content=f"An article named {instance.title} was created by {instance.user.userprofile.name}."
        )

post_save.connect(articleCreated, sender=Article)