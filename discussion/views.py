from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q
from .models import Discussion, DiscussionComment , DiscussionVote
from .serializers import DiscussionSerializer , DiscussionCommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


@api_view(['GET'])
def getDiscussion(request, pk):
    try:
        discussion= Discussion.objects.get(id=pk)
        serializer = DiscussionSerializer(discussion, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def editDiscussion(request,pk):
    try:
        discussion= Discussion.objects.get(id=pk)
        if discussion.user == request.user:
            data = request.data
            discussion.headline = data.get('headline')
            discussion.content = data.get('content')
            # tags field will be included after issue 23 is resolved
            # discussion.tags = data.get('tags')
            discussion.save()
            serializer = DiscussionSerializer(discussion, many=False)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
def deleteDiscussion(request,pk):
    try:
        discussion= Discussion.objects.get(id=pk)
        if discussion.user == request.user:
            discussion.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def discussions(request):
    query = request.query_params.get('q')
    if query == None:
        query = ''
    # Q objects is used to make complex query to search in discussion content and headline
    discussions = Discussion.objects.filter(Q(content__icontains=query)|Q(headline__icontains=query))
    serializer = DiscussionSerializer(discussions, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
def editDiscussionComment(request,pk):
    try:
        comment = DiscussionComment.objects.get(id=pk)
        if comment.user == request.user:
            serializer = DiscussionCommentSerializer(comment,many=False)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
def deleteDiscussionComment(request,pk):
    try:
        comment = DiscussionComment.objects.get(id=pk)
        if comment.user == request.user:
            serializer = DiscussionCommentSerializer(comment,many=False)
            comment.delete()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def createDiscussion(request):
    user = request.user
    data = request.data
    isComment = data.get('isComment')
    if isComment:
        discussion= Discussion.objects.get(id=data.get('postId'))
        comment = DiscussionComment.objects.create(
            user=user,
            discussion=discussion,
            content=data.get('content'),
            )
        comment.save()
        serializer = DiscussionCommentSerializer(comment,many=False)
        return Response(serializer.data)
    else:
        content = data.get('content')
        # tags field will be included after issue 23 is resolved
        # tags = data.get('tags')
        headline = data.get('headline')
        discussion= Discussion.objects.create(
            user=user,
            content=content,
            headline=headline,
            # tags=tags
            )
        discussion.save()
    serializer = DiscussionSerializer(discussion, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def updateVote(request):
    user = request.user
    data = request.data
    # get the discussion id
    discussionId = data.get('postId')
    # get discussionComment if, if it doesn't exist it will be None
    commentId = data.get('commentId')

    discussion= Discussion.objects.get(id=discussionId)

    if commentId:
        comment = DiscussionComment.objects.get(id=commentId)
        vote, created = DiscussionVote.objects.get_or_create(discussion=discussion,comment=comment,user=user,value=1)
        if not created:
            vote.delete()
        else:
            vote.save()
    else:
        vote, created = DiscussionVote.objects.get_or_create(discussion=discussion,user=user,value=1)
        if not created:
            vote.delete()
        else:
            vote.save()

    serializer = DiscussionSerializer(discussion, many=False)
    return Response(serializer.data)
