from django.db.models.signals import post_save, pre_save, post_delete
from django.contrib.auth.models import User
from .models import UserProfile


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
    userProfile, isCreated = UserProfile.objects.get_or_create(user=instance)
    if created == False:
        
        userProfile.username = instance.username

        #instance.userprofile.email = instance.email
        userProfile.save()
        print('Profile updated!')

post_save.connect(create_profile, sender=User)
post_save.connect(update_profile, sender=User)
