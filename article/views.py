from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.db.models import Q
from .models import Article , ArticleComment , ArticleVote
from .serializers import ArticleSerializer , ArticleCommentSerializer
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
def getArticle(request, pk):
    try:
        article = Article.objects.get(id=pk)
        serializer = ArticleSerializer(article, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def editArticle(request,pk):
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
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
def deleteArticle(request,pk):
    try:
        article = Article.objects.get(id=pk)
        if article.user == request.user:
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def articles(request):
    query = request.query_params.get('q')
    if query == None:
        query = ''
    articles = Article.objects.filter(Q(content__icontains=query)|Q(title__icontains=query))
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
def editArticleComment(request,pk):
    try:
        comment = ArticleComment.objects.get(id=pk)
        if comment.user == request.user:
            serializer = ArticleCommentSerializer(comment,many=False)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
def deleteArticleComment(request,pk):
    try:
        comment = ArticleComment.objects.get(id=pk)
        if comment.user == request.user:
            serializer = ArticleCommentSerializer(comment,many=False)
            comment.delete()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def createArticle(request):
    user = request.user
    data = request.data
    isComment = data.get('isComment')
    if isComment:
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
            tags=tags
            )
        article.save()
    serializer = ArticleSerializer(article, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def updateVote(request):
    user = request.user
    data = request.data
    # lets grab article id
    articleId = data.get('postId')
    # lets grab article comment id if there is else it will ne None 
    commentId = data.get('commentId')

    article = Article.objects.get(id=articleId)

    if commentId:
        comment = ArticleComment.objects.get(id=commentId)
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
