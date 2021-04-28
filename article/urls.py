from django.urls import path
from . import views

urlpatterns = [
    path('',views.articles,name='articles'),
    path('create/',views.createArticle,name='create-article'),
    path('vote/',views.updateVote,name='vote'),
    path('<str:pk>/', views.getArticle, name="get-article"),
]
