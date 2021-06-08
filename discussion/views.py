from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q
from .models import Discussion, DiscussionComment , DiscussionVote
from .serializers import DiscussionSerializer , DiscussionCommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from users.models import TopicTag


@api_view(['GET'])
def get_discussion(request, pk):
    try:
        discussion= Discussion.objects.get(id=pk)
        serializer = DiscussionSerializer(discussion, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def edit_discussion(request,pk):
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
        return Response({'detail':f'{e}'},status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_discussion(request,pk):
    try:
        discussion= Discussion.objects.get(id=pk)
        if discussion.user == request.user:
            discussion.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'detail':f'{e}'},status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def discussions(request):
    query = request.query_params.get('q')
    if query == None:
        query = ''
    # Q objects is used to make complex query to search in discussion content and headline
    discussions = Discussion.objects.filter(Q(content__icontains=query)|Q(headline__icontains=query)).order_by("-created")
    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(discussions,request)
    serializer = DiscussionSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def edit_discussion_comment(request,pk):
    try:
        comment = DiscussionComment.objects.get(id=pk)
        if comment.user == request.user:
            serializer = DiscussionCommentSerializer(comment,many=False)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'detail':f'{e}'},status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_discussion_comment(request,pk):
    try:
        comment = DiscussionComment.objects.get(id=pk)
        if comment.user == request.user:
            serializer = DiscussionCommentSerializer(comment,many=False)
            comment.delete()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'detail':f'{e}'},status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_discussion(request):
    user = request.user
    data = request.data
    is_comment = data.get('isComment')
    if is_comment:
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
        tags = data.get('tags')
        headline = data.get('headline')
        discussion= Discussion.objects.create(
            user=user,
            content=content,
            headline=headline,
            )
        if tags is not None:
            for tag_name in tags:
                tag_instance = TopicTag.objects.filter(name=tag_name).first()
                if not tag_instance:
                    tag_instance = TopicTag.objects.create(name=tag_name)
                discussion.tags.add(tag_instance)
        discussion.save()
    serializer = DiscussionSerializer(discussion, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def update_vote(request):
    user = request.user
    data = request.data
    discussion_id = data.get('postId')
    comment_id = data.get('commentId')

    discussion= Discussion.objects.get(id=discussion_id)

    if comment_id:
        comment = DiscussionComment.objects.get(id=comment_id)
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
