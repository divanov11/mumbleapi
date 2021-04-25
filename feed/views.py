from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from django.db.models import Q
from rest_framework import status

from .models import Mumble, MumbleVote

from .serializers import MumbleSerializer

# Create your views here.


@api_view(['GET'])
def mumbles(request):
    query = request.query_params.get('q')
    if query == None:
        query = ''

    user = request.user
    following = user.following.select_related('user')

    following = user.following.all()

    ids = [user.id]
    for i in following:
        ids.append(i.user.id)

    #Make sure parent==None is always on
    mumbles = Mumble.objects.filter(parent=None, user__id__in=ids)
    mumbles = mumbles.filter(Q(user__userprofile__name__icontains=query) | Q(content__icontains=query))
    serializer = MumbleSerializer(mumbles, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def createMumble(request):
    user = request.user
    data = request.data

    isComment = data['isComment']
    if isComment:
        parent = Mumble.objects.get(id=data['postId'])
        mumble = Mumble.objects.create(
            parent=parent,
            user=user,
            content=data['content'],
            )
    else:
        mumble = Mumble.objects.create(
            user=user,
            content=data['content']
            )

    serializer = MumbleSerializer(mumble, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def mumbleComments(request, pk):
    mumble = Mumble.objects.get(id=pk)
    comments = mumble.mumble_set.all()
    serializer = MumbleSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def remumble(request):
    user = request.user
    data = request.data
    originalMumble = Mumble.objects.get(id=data['id'])

    mumble = Mumble.objects.create(
        remumble=originalMumble,
        user=user,
    )
    serializer = MumbleSerializer(mumble, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def updateVote(request):
    user = request.user 
    data = request.data

    mumble = Mumble.objects.get(id=data['post_id'])
    #What if user is trying to remove their vote?
    vote, created = MumbleVote.objects.get_or_create(mumble=mumble, user=user)

    if vote.value == data['value']:
        #If same value is sent, user is clicking on vote to remove it
        vote.delete() 
    else:

        vote.value=data['value']
        vote.save()

    #We re-query the vote to get the latest vote rank value
    mumble = Mumble.objects.get(id=data['post_id'])
    serializer = MumbleSerializer(mumble, many=False)

    return Response(serializer.data)
