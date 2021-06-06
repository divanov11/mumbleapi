from django.urls import path
from . import views

app_name = 'mumbles-api-articles'

urlpatterns = [
    path('',views.articles,name='articles'),
    path('create/',views.create_article,name='create-article'),
    path('vote/',views.update_vote,name='article-vote'),
    path('<str:pk>/', views.get_article, name="get-article"),
    path('edit/<str:pk>/', views.edit_article, name="edit-article"),
    path('delete/<str:pk>/', views.delete_article, name="delete-article"),
    path('edit-comment/<str:pk>/', views.edit_article_comment, name="edit-article-comment"),
    path('delete-comment/<str:pk>/', views.delete_article_comment, name="delete-article-comment"),
]
