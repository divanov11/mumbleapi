from django.urls import path
from . import views

app_name = 'mumbles-api'

urlpatterns = [
     path('', views.mumbles, name="mumbles"),
     path('create/', views.create_mumble, name="mumble-create"),
     path('edit/<str:pk>/', views.edit_mumble, name="mumble-edit"),
     path('details/<str:pk>/', views.mumble_details, name="mumble-details"),
     path('remumble/', views.remumble, name="mumble-remumble"),
     path('vote/', views.update_vote, name="posts-vote"),
     path('delete/<str:pk>/', views.delete_mumble, name="delete-mumble"),
     path('<str:pk>/comments/', views.mumble_comments, name="mumble-comments"),
]