from django.db.models.signals import post_save, pre_save, post_delete
from django.contrib.auth.models import User
from users.models import UserProfile
from .models import Mumble, MumbleVote
from .utils import update_comment_counts, update_remumble_counts

def update_mumble(sender, instance, created, **kwargs):
    #If a post is created & is a comment, them update the parent

    if created and instance.parent:
        update_comment_counts(instance.parent, 'add')

    if instance.remumble:
        parent = instance.remumble
        update_remumble_counts(parent, 'add')


def delete_mumble_comments(sender, instance, **kwargs):
    #If a post is created & is a comment, them update the parent

    try:
        if instance.parent:
            update_comment_counts(instance.parent, 'delete')
    except Exception as e:
        print('mumble associated with comment was deleted')

    try:
        if instance.remumble:
            update_remumble_counts(instance.remumble, 'delete')
    except Exception as e:
        print('remumble associated with comment was deleted')

post_save.connect(update_mumble, sender=Mumble)
post_delete.connect(delete_mumble_comments, sender=Mumble)


def vote_updated(sender, instance, **kwargs):
    try:
        mumble = instance.mumble
        up_votes =  len(mumble.votes.through.objects.filter(mumble=mumble, value='upvote'))
        down_votes =  len(mumble.votes.through.objects.filter(mumble=mumble, value='downvote'))
        mumble.vote_rank = (up_votes - down_votes)
        mumble.save()
    except Exception as e:
        print('mumble the vote was associated with was already deleted')



post_save.connect(vote_updated, sender=MumbleVote)
post_delete.connect(vote_updated,  sender=MumbleVote)
