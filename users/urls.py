from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


app_name = 'users-api'

urlpatterns = [
    #api/users/
    path('', views.users, name='users'),
    path('recommended/', views.users_recommended, name="users-recommended"),

    path('profile/', views.profile, name='profile'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='login'),
    path('following/', views.following, name='following'),
    path('refresh_token/', TokenRefreshView.as_view(), name='refresh_token'),

    path('profile_update/', views.UserProfileUpdate.as_view(), name="profile_update"), 
    path('profile_update/skills/', views.update_skills, name='update_skills'),
    path('profile_update/interests/', views.update_interests, name='update_interests'),
    path('profile_update/photo/', views.ProfilePictureUpdate.as_view(), name="profile_update_photo"), 
    path('<str:username>/follow/', views.follow_user, name="follow-user"),
    path('delete-profile/', views.delete_user, name="delete-user"),
    path('profile_update/delete/', views.ProfilePictureDelete, name="profile_delete_photo"), 
    path('<str:username>/', views.user, name="user"),
    path('skills/<str:skill>', views.users_by_skill, name="users-by-skill"),
    path('<str:username>/mumbles/', views.user_mumbles, name="user-mumbles"),
    path('<str:username>/articles/', views.user_articles, name="user-articles"),

    # Forget password or reset password
    path('password/change/',views.password_change,name="password-change"),
    # path('password/reset/',views.passwordReset,name="password-reset"),

    # email verification urls
    path('email/send-email-activation',views.send_activation_email,name='send-activation-email'),
    path('verify/<uidb64>/<token>/',views.activate, name='verify'),
]