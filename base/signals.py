from django.db.models.signals import post_save, pre_save, post_delete
from django.contrib.auth.models import User
from .models import UserProfile, Post, PostVote


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
        parentPost = instance.remumble 
        parentPost.share_count = len(parentPost.shares)
        parentPost.save()

def voteUpdate(sender, instance, **kwargs):
    vote = instance
    print('VOTE IN POST DELETE', vote)
    post = instance.post

    upvotes =  len(post.postvote_set.filter(value="upvote"))
    downvotes =  len(post.postvote_set.filter(value="downvote"))
    print('UPVOTES COUNT:', upvotes)
    print("upvotes -downvotes:", (upvotes - downvotes))


    post.vote_rank = (upvotes - downvotes)
    print('post.vote_rank:', post.vote_rank)
    post.save()
    print('post.vote_rank:', post.vote_rank)


pre_save.connect(updatePost, sender=Post)
post_save.connect(voteUpdate, sender=PostVote)
post_delete.connect(voteUpdate,  sender=PostVote)

