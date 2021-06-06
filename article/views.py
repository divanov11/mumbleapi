from rest_framework.response import Response 
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.db.models import Q
from .models import Article , ArticleComment , ArticleVote
from .serializers import ArticleSerializer , ArticleCommentSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from users.models import TopicTag

@api_view(['GET'])
def get_article(request, pk):
    try:
        article = Article.objects.get(id=pk)
        serializer = ArticleSerializer(article, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response({'details': f"{e}"},status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def edit_article(request,pk):
    try:
        article = Article.objects.get(id=pk)
        if article.user == request.user:
            data = request.data
            article.title = data.get('title')
            article.content = data.get('content')
            article.tags = data.get('tags')
            article.save()
            serializer = ArticleSerializer(article, many=False)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'details': f"{e}"},status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_article(request,pk):
    try:
        article = Article.objects.get(id=pk)
        if article.user == request.user:
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'details': f"{e}"},status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def articles(request):
    query = request.query_params.get('q')
    if query == None:
        query = ''
    articles = Article.objects.filter(Q(content__icontains=query)|Q(title__icontains=query)).order_by("-created")
    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(articles,request)
    serializer = ArticleSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def edit_article_comment(request,pk):
    try:
        comment = ArticleComment.objects.get(id=pk)
        if comment.user == request.user:
            serializer = ArticleCommentSerializer(comment,many=False)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'details': f"{e}"},status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_article_comment(request,pk):
    try:
        comment = ArticleComment.objects.get(id=pk)
        if comment.user == request.user:
            serializer = ArticleCommentSerializer(comment,many=False)
            comment.delete()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'details': f"{e}"},status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_article(request):
    user = request.user
    data = request.data
    is_comment = data.get('isComment')
    if is_comment:
        article = Article.objects.get(id=data.get('postId'))
        comment = ArticleComment.objects.create(
            user=user,
            article=article,
            content=data.get('content'),
            )
        comment.save()
        serializer = ArticleCommentSerializer(comment,many=False)
        return Response(serializer.data)
    else:
        content = data.get('content')
        tags = data.get('tags')
        title = data.get('title')
        article = Article.objects.create(
            user=user,
            content=content,
            title=title,
            )
        if tags is not None:
            for tag_name in tags:
                tag_instance = TopicTag.objects.filter(name=tag_name).first()
                if not tag_instance:
                    tag_instance = TopicTag.objects.create(name=tag_name)
                article.tags.add(tag_instance)
        article.save()
    serializer = ArticleSerializer(article, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def update_vote(request):
    user = request.user
    data = request.data
    article_id = data.get('postId')
    comment_id = data.get('commentId')

    article = Article.objects.get(id=article_id)

    if comment_id:
        comment = ArticleComment.objects.get(id=comment_id)
        vote, created = ArticleVote.objects.get_or_create(article=article,comment=comment,user=user,value=1)
        if not created:
            vote.delete()
        else:
            vote.save()
    else:
        vote, created = ArticleVote.objects.get_or_create(article=article,user=user,value=1)
        if not created:
            vote.delete()
        else:
            vote.save()

    serializer = ArticleSerializer(article, many=False)
    return Response(serializer.data)
