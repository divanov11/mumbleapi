from django.urls import path
from . import views

urlpatterns = [
     path('', views.mumbles, name="mumbles"),
     path('create/', views.createMumble, name="mumble-create"),
     path('remumble/', views.remumble, name="mumble-remumble"),
     path('vote/', views.updateVote, name="posts-vote"),

     path('<str:pk>/comments/', views.mumbleComments, name="mumble-comments"),
]