from django.urls import path
from . import views

urlpatterns = [
    path('',views.articles,name='articles'),
    path('create/',views.createArticle,name='create-article'),
    path('vote/',views.updateVote,name='vote'),
    path('<str:pk>/', views.getArticle, name="get-article"),
    path('edit/<str:pk>/', views.editArticle, name="edit-article"),
    path('delete/<str:pk>/', views.deleteArticle, name="delete-article"),
    path('edit-comment/<str:pk>/', views.editArticleComment, name="edit-article-comment"),
    path('delete-comment/<str:pk>/', views.deleteArticleComment, name="delete-article-comment"),
]
