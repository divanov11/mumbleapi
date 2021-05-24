from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


app_name = 'users-api'

urlpatterns = [
    #api/users/
    path('', views.users, name='users'),
    path('recommended/', views.usersRecommended, name="users-recommended"),

    path('profile/', views.profile, name='profile'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='login'),
    path('following/', views.following, name='following'),
    path('refresh_token/', TokenRefreshView.as_view(), name='refresh_token'),

    path('profile_update/', views.UserProfileUpdate.as_view(), name="profile_update"), 
    path('profile_update/skills/', views.updateSkills, name='update_skills'),
    path('profile_update/interests/', views.updateInterests, name='update_interests'),
    path('profile_update/photo/', views.ProfilePictureUpdate.as_view(), name="profile_update_photo"), 
    path('<str:username>/follow/', views.followUser, name="follow-user"),

    path('<str:username>/', views.user, name="user"),
    path('<str:username>/mumbles/', views.userMumbles, name="user-mumbles"),
    path('<str:username>/articles/', views.userArticles, name="user-articles"),

    # Forget password or reset password
    path('password/change/',views.passwordChange,name="password-change"),
    # path('password/reset/',views.passwordReset,name="password-reset"),

    # email verification urls
    path('email/send-email-activation',views.sendActivationEmail,name='send-activation-email'),
    path('verify/<uidb64>/<token>/',views.activate, name='verify'),
]