from django.db.models.signals import post_save, pre_save, post_delete
from django.contrib.auth.models import User
from .models import UserProfile, Post, PostVote


#Updates comment count for parent posts
def updateCommentCounts(parent, action):
    if parent:
        if action == 'add':
            parent.comment_count += 1
        if action == 'delete':
            parent.comment_count -= 1
        parent.save()
        return updateCommentCounts(parent.parent, action)

#Gets triggered on post created and updates remumble count if shared or deleted
def updateRemumbleCounts(parent, action):

    if action == 'add':

        parent.share_count += 1

    if action == 'delete':
        parent.share_count -= 1

    parent.save()

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





def updatePost(sender, instance, created, **kwargs):
    #If a post is created & is a comment, them update the parent

    if created and instance.parent:
        updateCommentCounts(instance.parent, 'add')

    if instance.remumble:
        parent = instance.remumble
        updateRemumbleCounts(parent, 'add')


def deletePostComments(sender, instance, **kwargs):
    #If a post is created & is a comment, them update the parent

    if instance.parent:
        updateCommentCounts(instance.parent, 'delete')


    if instance.remumble:
        parent = instance.remumble
        updateRemumbleCounts(parent, 'delete')

post_save.connect(updatePost, sender=Post)
post_delete.connect(deletePostComments, sender=Post)



def voteUpdate(sender, instance, **kwargs):
    vote = instance
    post = instance.post

    upvotes =  len(post.votes.through.objects.filter(post=post, value='upvote'))
    downvotes =  len(post.votes.through.objects.filter(post=post, value='downvote'))

    post.vote_rank = (upvotes - downvotes)
    post.save()



post_save.connect(voteUpdate, sender=PostVote)
post_delete.connect(voteUpdate,  sender=PostVote)

