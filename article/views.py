from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Article , ArticleComment , ArticleVote
from .serializers import ArticleSerializer , ArticleCommentSerializer
# Create your views here.

@api_view(['GET'])
def artciles(request):
    article = Article.objects.all()
    serializer = ArticleSerializer(article, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createArtcile(request):
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
        article = Article.objects.create(user=user,content=content,tags=tags)
        article.save()
    serializer = ArticleSerializer(article, many=False)
    return Response(serializer.data)

@api_view(['POST'])
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