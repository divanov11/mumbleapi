from django.urls import path
from . import views


urlpatterns = [

    path('', views.routes, name="routes"),
    path('posts/', views.posts, name="posts"),

    path('posts/create/', views.createPost, name="posts-create"),
    path('posts/remumble/', views.remumble, name="posts-remumble"),
    path('posts/vote/', views.updateVote, name="posts-vote"),

    path('posts/<str:pk>/comments/', views.postComments, name="posts-comments"),

    path('users/', views.users, name="users"),
    path('users/recommended/', views.usersRecommended, name="users-recommended"),

    path('users/register/', views.registerUser, name='register'),
    path('users/token/', views.MyTokenObtainPairView.as_view(), name='token'),
    #path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('users/<str:username>/follow/', views.followUser, name="follow-user"),

    path('users/<str:username>/', views.user, name="user"),
    path('users/<str:username>/posts/', views.userPosts, name="user-posts"),
    # path('users/<str:pk>/tags/', views.userTags, name="user-tags"),

    #  path('tags/', views.tags, name="tags"),
]