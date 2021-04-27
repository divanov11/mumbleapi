from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Article
from .serializers import ArticleSerializer
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
    content = data.get('content')
    tags = data.get('tags')
    article = Article.objects.create(user=user,content=content,tags=tags)
    article.save()
    serializer = ArticleSerializer(article, many=False)
    return Response(serializer.data)
