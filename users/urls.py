from django.urls import path
from . import views

urlpatterns = [
    #api/users/
    path('', views.users, name='users'),
    path('recommended/', views.usersRecommended, name="users-recommended"),

    path('register/', views.registerUser, name='register'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='login'),

    path('profile_update/', views.UserProfileUpdate.as_view(), name="profile_update"),
    path('profile_update/photo/', views.update_profile_pic, name="profile_pic_update"), 
    path('<str:username>/follow/', views.followUser, name="follow-user"),

    path('<str:username>/', views.user, name="user"),
    path('<str:username>/mumbles/', views.userMumbles, name="user-mumbles"),

]