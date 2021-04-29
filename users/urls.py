from django.urls import path
from . import views

app_name = 'users-api'

urlpatterns = [
    #api/users/
    path('', views.users, name='users'),
    path('recommended/', views.usersRecommended, name="users-recommended"),

    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='login'),

    path('profile_update/', views.UserProfileUpdate.as_view(), name="profile_update"), 
    path('<str:username>/follow/', views.followUser, name="follow-user"),

    path('<str:username>/', views.user, name="user"),
    path('<str:username>/mumbles/', views.userMumbles, name="user-mumbles"),
    path('<str:username>/articles/', views.userArticles, name="user-articles"),

    # email verification urls
    path('send-email-verification',views.SendActivationEmail,name='send-activation-email'),
    path('verify/<uidb64>/<token>/',views.activate, name='verify'),
]