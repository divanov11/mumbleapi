from django.urls import path
from . import views

app_name = 'mumbles-api'

urlpatterns = [
     path('', views.mumbles, name="mumbles"),
     path('create/', views.createMumble, name="mumble-create"),
     path('remumble/', views.remumble, name="mumble-remumble"),
     path('vote/', views.updateVote, name="posts-vote"),
     path('<str:pk>/', views.deleteMumble, name="delete-mumble"),
     path('<str:pk>/comments/', views.mumbleComments, name="mumble-comments"),
]