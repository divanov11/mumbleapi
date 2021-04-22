from django.db.models.signals import post_save, pre_save, post_delete
from django.contrib.auth.models import User
from users.models import UserProfile
from .models import Mumble, MumbleVote
from .utils import updateCommentCounts, updateRemumbleCounts

def updateMumble(sender, instance, created, **kwargs):
    #If a post is created & is a comment, them update the parent

    if created and instance.parent:
        updateCommentCounts(instance.parent, 'add')

    if instance.remumble:
        parent = instance.remumble
        updateRemumbleCounts(parent, 'add')


def deleteMumbleComments(sender, instance, **kwargs):
    #If a post is created & is a comment, them update the parent

    if instance.parent:
        updateCommentCounts(instance.parent, 'delete')


    if instance.remumble:
        parent = instance.remumble
        updateRemumbleCounts(parent, 'delete')

post_save.connect(updateMumble, sender=Mumble)
post_delete.connect(deleteMumbleComments, sender=Mumble)



def voteUpdate(sender, instance, **kwargs):
    print('Update Vote Triggered')
    vote = instance
    mumble = instance.mumble

    upvotes =  len(mumble.votes.through.objects.filter(mumble=mumble, value='upvote'))
    downvotes =  len(mumble.votes.through.objects.filter(mumble=mumble, value='downvote'))

    mumble.vote_rank = (upvotes - downvotes)
    mumble.save()



post_save.connect(voteUpdate, sender=MumbleVote)
post_delete.connect(voteUpdate,  sender=MumbleVote)
