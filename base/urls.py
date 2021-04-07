from django.urls import path
from . import views

urlpatterns = [
    path('', views.routes, name="routes"),
    path('posts/', views.posts, name="posts"),
    path('posts/<str:pk>/comments/', views.postComments, name="posts-comments"),

    path('users/', views.users, name="users"),
    path('users/recommended/', views.usersRecommended, name="users-recommended"),

    path('users/<str:username>/', views.user, name="user"),
    path('users/<str:username>/posts/', views.userPosts, name="user-posts"),
    # path('users/<str:pk>/tags/', views.userTags, name="user-tags"),

    #  path('tags/', views.tags, name="tags"),
]