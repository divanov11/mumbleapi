from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from .models import UserProfile, Post


def create_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(
			user=instance,
			name=instance.username,
            username=instance.username,
			#email=instance.email,
			)
            
		print('Profile Created!')


def update_profile(sender, instance, created, **kwargs):
    if created == False:
        instance.userprofile.username = instance.username

        #instance.userprofile.email = instance.email
        instance.userprofile.save()
        print('Profile updated!')

post_save.connect(create_profile, sender=User)
post_save.connect(update_profile, sender=User)


def updatePost(sender, instance, **kwargs):
    if instance.parent:
        parent = instance.parent 
        parent.comment_count += 1
    
        parent.save()

    if instance.remumble:
        print('THis is a remumble')
        parentPost = instance.remumble 
        parentPost.share_count = len(parentPost.shares)
        parentPost.save()


pre_save.connect(updatePost, sender=Post)
