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
