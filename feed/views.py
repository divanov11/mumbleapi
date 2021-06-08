from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Mumble, MumbleVote
from .serializers import MumbleSerializer

# Create your views here.


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def mumbles(request):
    query = request.query_params.get('q')
    if query == None:
        query = ''

    user = request.user
    following = user.following.select_related('user')

    following = user.following.all()

    ids = []
    ids = [i.user.id for i in following]
    ids.append(user.id)
    print('IDS:', ids)
    
    #Make sure parent==None is always on
    #Query 5 mumbles form users you follow | TOP PRIORITY
    
    mumbles = list(Mumble.objects.filter(parent=None, user__id__in=ids).order_by("-created"))[0:5]
    #mumbles = list(mumbles.filter(Q(user__userprofile__name__icontains=query) | Q(content__icontains=query)))

    recentMumbles = Mumble.objects.filter(Q(parent=None) & Q(vote_rank__gte=0) & Q(remumble=None)).order_by("-created")[0:5]

    #Query top ranked mumbles and attach to end of original queryset
    topMumbles = Mumble.objects.filter(Q(parent=None)).order_by("-vote_rank", "-created")

    #Add top ranked mumbles to feed after prioritizing follow list 
    index = 0
    for mumble in recentMumbles:
        if mumble not in mumbles:
            mumbles.insert(index, mumble) 
            index += 1


    #Add top ranked mumbles to feed after prioritizing follow list 
    for mumble in topMumbles:
        if mumble not in mumbles:
            mumbles.append(mumble)


    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(mumbles, request)
    serializer = MumbleSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def mumble_details(request,pk):
    try:
        mumble = Mumble.objects.get(id=pk)
        serializer = MumbleSerializer(mumble, many=False)
        return Response(serializer.data)
    except:
        message = {
            'detail':'Mumble doesn\'t exist'
        }
        return Response(message, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_mumble(request):
    user = request.user
    data = request.data

    is_comment = data.get('isComment')
    if is_comment:
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

@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def edit_mumble(request,pk):
    user = request.user
    data = request.data

    try:
        mumble = Mumble.objects.get(id=pk)
        if user != mumble.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = MumbleSerializer(mumble,data = data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    except Exception as e:
        return Response(status=status.HTTP_204_NO_CONTENT)    

@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_mumble(request, pk):
    user = request.user
    try:
        mumble = Mumble.objects.get(id=pk)
        if user != mumble.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            mumble.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'details': f"{e}"},status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def mumble_comments(request, pk):
    mumble = Mumble.objects.get(id=pk)
    comments = mumble.mumble_set.all()
    serializer = MumbleSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def remumble(request):
    user = request.user
    data = request.data
    original_mumble = Mumble.objects.get(id=data['id'])
    if original_mumble.user == user:
        return Response({'detail':'You can not remumble your own mumble.'},status=status.HTTP_403_FORBIDDEN)
    try:
        mumble = Mumble.objects.filter(
            remumble=original_mumble,
            user=user,
        )
        if mumble.exists():
            return Response({'detail':'Already Mumbled'},status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            mumble = Mumble.objects.create(
            remumble=original_mumble,
            user=user,
        )
        serializer = MumbleSerializer(mumble, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response({'detail':f'{e}'},status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def update_vote(request):
    user = request.user 
    data = request.data

    mumble = Mumble.objects.get(id=data['post_id'])
    #What if user is trying to remove their vote?
    vote, created = MumbleVote.objects.get_or_create(mumble=mumble, user=user)

    if vote.value == data.get('value'):
        #If same value is sent, user is clicking on vote to remove it
        vote.delete() 
    else:

        vote.value=data['value']
        vote.save()

    #We re-query the vote to get the latest vote rank value
    mumble = Mumble.objects.get(id=data['post_id'])
    serializer = MumbleSerializer(mumble, many=False)

    return Response(serializer.data)
